import re

from notebook.models import PageEntityMention, PageLink

# @[person:7|John Smith]
PERSON_MENTION_RE = re.compile(r"@\[person:(\d+)\|[^\]]+\]")

# [[type:ID|Label]] where type is page, task, org, project
BRACKET_MENTION_RE = re.compile(r"\[\[(page|task|org|project):(\d+)\|[^\]]+\]\]")

# - [ ] <text> where text does NOT already contain [[task:
CHECKBOX_RE = re.compile(r"^(- \[ \] )(.+)$", re.MULTILINE)

# Normalize "org" to "organization" for storage
ENTITY_TYPE_MAP = {
    "task": "task",
    "org": "organization",
    "project": "project",
}


def get_inbox_section():
    """Return the Inbox list's section for task creation."""
    from tasks.models import Section

    return Section.objects.filter(list__is_system=True).first()


def parse_mentions(content: str):
    """Extract entity mentions and page links from content.

    Returns:
        (entity_mentions, page_ids) where:
        - entity_mentions is a set of (entity_type, entity_id) tuples
        - page_ids is a set of target page IDs
    """
    entity_mentions = set()
    page_ids = set()

    for match in PERSON_MENTION_RE.finditer(content):
        entity_mentions.add(("person", int(match.group(1))))

    for match in BRACKET_MENTION_RE.finditer(content):
        mention_type = match.group(1)
        mention_id = int(match.group(2))
        if mention_type == "page":
            page_ids.add(mention_id)
        else:
            entity_type = ENTITY_TYPE_MAP[mention_type]
            entity_mentions.add((entity_type, mention_id))

    return entity_mentions, page_ids


def create_tasks_from_checkboxes(page):
    """Detect - [ ] lines and create tasks in the Inbox for new ones.

    Rewrites page.content in place with [[task:ID|Title]] links.
    Returns True if content was modified.
    """
    from tasks.models import Task

    inbox_section = get_inbox_section()
    if not inbox_section:
        return False

    modified = False
    content = page.content

    def replace_checkbox(match):
        nonlocal modified
        prefix = match.group(1)  # "- [ ] "
        text = match.group(2)

        # Skip if already linked to a task
        if "[[task:" in text:
            return match.group(0)

        # Skip if text is whitespace-only
        title = text.strip()
        if not title:
            return match.group(0)

        # Create the task in the Inbox section
        max_pos = (
            Task.objects.filter(section=inbox_section, parent__isnull=True)
            .order_by("-position")
            .values_list("position", flat=True)
            .first()
        ) or 0
        task = Task.objects.create(
            section=inbox_section,
            title=title,
            position=max_pos + 10,
        )
        modified = True
        return f"{prefix}[[task:{task.id}|{title}]]"

    new_content = CHECKBOX_RE.sub(replace_checkbox, content)
    if modified:
        page.content = new_content
        page.save(update_fields=["content"])

    return modified


def reconcile_mentions(page):
    """Parse page content and sync join tables to match.

    Also creates tasks from checkbox syntax before reconciling.
    """
    # First, create tasks from any new checkboxes (modifies page.content)
    create_tasks_from_checkboxes(page)

    # Now reconcile mentions based on the (possibly updated) content
    entity_mentions, page_ids = parse_mentions(page.content)

    # Reconcile entity mentions
    existing = set(
        PageEntityMention.objects.filter(page=page).values_list("entity_type", "entity_id")
    )
    to_add = entity_mentions - existing
    to_remove = existing - entity_mentions

    if to_remove:
        for entity_type, entity_id in to_remove:
            PageEntityMention.objects.filter(
                page=page, entity_type=entity_type, entity_id=entity_id
            ).delete()

    if to_add:
        PageEntityMention.objects.bulk_create(
            [
                PageEntityMention(page=page, entity_type=et, entity_id=eid)
                for et, eid in to_add
            ]
        )

    # Reconcile page links
    existing_links = set(
        PageLink.objects.filter(source_page=page).values_list("target_page_id", flat=True)
    )
    links_to_add = page_ids - existing_links
    links_to_remove = existing_links - page_ids

    if links_to_remove:
        PageLink.objects.filter(source_page=page, target_page_id__in=links_to_remove).delete()

    if links_to_add:
        PageLink.objects.bulk_create(
            [PageLink(source_page=page, target_page_id=tid) for tid in links_to_add]
        )
