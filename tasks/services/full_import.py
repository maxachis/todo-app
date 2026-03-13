from __future__ import annotations

from datetime import date, time

from django.db import transaction
from django.utils.dateparse import parse_date, parse_datetime, parse_time

from network.models import (
    Interaction,
    InteractionTask,
    InteractionType,
    Lead,
    LeadTask,
    Organization,
    OrgType,
    Person,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
    TaskOrganization,
    TaskPerson,
)
from notebook.models import Page, PageLink
from tasks.models import List, Project, ProjectLink, Section, Tag, Task, TimeEntry


def _make_stats():
    return {
        "tags_created": 0, "tags_skipped": 0,
        "org_types_created": 0, "org_types_skipped": 0,
        "interaction_types_created": 0, "interaction_types_skipped": 0,
        "projects_created": 0, "projects_skipped": 0,
        "project_links_created": 0, "project_links_skipped": 0,
        "people_created": 0, "people_skipped": 0,
        "organizations_created": 0, "organizations_skipped": 0,
        "lists_created": 0, "lists_skipped": 0,
        "sections_created": 0, "sections_skipped": 0,
        "tasks_created": 0, "tasks_skipped": 0,
        "time_entries_created": 0, "time_entries_skipped": 0,
        "interactions_created": 0, "interactions_skipped": 0,
        "leads_created": 0, "leads_skipped": 0,
        "lead_tasks_created": 0, "lead_tasks_skipped": 0,
        "relationships_pp_created": 0, "relationships_pp_skipped": 0,
        "relationships_op_created": 0, "relationships_op_skipped": 0,
        "task_persons_created": 0, "task_persons_skipped": 0,
        "task_organizations_created": 0, "task_organizations_skipped": 0,
        "interaction_tasks_created": 0, "interaction_tasks_skipped": 0,
        "notebook_pages_created": 0, "notebook_pages_skipped": 0,
        "page_links_created": 0, "page_links_skipped": 0,
        "errors": 0,
        "error_details": [],
    }


def _parse_date_safe(val):
    if not val or val == "None":
        return None
    if isinstance(val, date):
        return val
    return parse_date(val)


def _parse_datetime_safe(val):
    if not val or val == "None":
        return None
    return parse_datetime(val)


def _parse_time_safe(val):
    if not val or val == "None":
        return None
    if isinstance(val, time):
        return val
    return parse_time(val)


def import_full_database(data: dict) -> dict:
    """Import a full database backup from the nexus-full-backup JSON format."""
    stats = _make_stats()

    # ID mappings: old_id -> new_id
    tag_map: dict[int, int] = {}
    org_type_map: dict[int, int] = {}
    interaction_type_map: dict[int, int] = {}
    project_map: dict[int, int] = {}
    person_map: dict[int, int] = {}
    organization_map: dict[int, int] = {}
    list_map: dict[int, int] = {}
    section_map: dict[int, int] = {}
    task_map: dict[int, int] = {}
    time_entry_map: dict[int, int] = {}
    interaction_map: dict[int, int] = {}
    lead_map: dict[int, int] = {}
    page_map: dict[int, int] = {}

    with transaction.atomic():
        # ── 1. Independent entities ──

        # Tags
        for item in data.get("tags", []):
            existing = Tag.objects.filter(name=item["name"]).first()
            if existing:
                tag_map[item["id"]] = existing.id
                stats["tags_skipped"] += 1
            else:
                obj = Tag.objects.create(name=item["name"])
                tag_map[item["id"]] = obj.id
                stats["tags_created"] += 1

        # OrgTypes
        for item in data.get("org_types", []):
            existing = OrgType.objects.filter(name=item["name"]).first()
            if existing:
                org_type_map[item["id"]] = existing.id
                stats["org_types_skipped"] += 1
            else:
                obj = OrgType.objects.create(name=item["name"])
                org_type_map[item["id"]] = obj.id
                stats["org_types_created"] += 1

        # InteractionTypes
        for item in data.get("interaction_types", []):
            existing = InteractionType.objects.filter(name=item["name"]).first()
            if existing:
                interaction_type_map[item["id"]] = existing.id
                stats["interaction_types_skipped"] += 1
            else:
                obj = InteractionType.objects.create(name=item["name"])
                interaction_type_map[item["id"]] = obj.id
                stats["interaction_types_created"] += 1

        # Projects
        for item in data.get("projects", []):
            existing = Project.objects.filter(name=item["name"]).first()
            if existing:
                project_map[item["id"]] = existing.id
                stats["projects_skipped"] += 1
            else:
                obj = Project.objects.create(
                    name=item["name"],
                    description=item.get("description", ""),
                    is_active=item.get("is_active", True),
                    position=item.get("position", 0),
                )
                project_map[item["id"]] = obj.id
                stats["projects_created"] += 1

        # People
        for item in data.get("people", []):
            existing = Person.objects.filter(
                first_name=item["first_name"],
                last_name=item["last_name"],
            ).first()
            if existing:
                person_map[item["id"]] = existing.id
                stats["people_skipped"] += 1
            else:
                obj = Person.objects.create(
                    first_name=item["first_name"],
                    middle_name=item.get("middle_name", ""),
                    last_name=item["last_name"],
                    email=item.get("email", ""),
                    linkedin_url=item.get("linkedin_url", ""),
                    notes=item.get("notes", ""),
                    follow_up_cadence_days=item.get("follow_up_cadence_days"),
                )
                person_map[item["id"]] = obj.id
                stats["people_created"] += 1

        # ── 2. FK-dependent entities ──

        # Organizations (FK -> OrgType)
        for item in data.get("organizations", []):
            existing = Organization.objects.filter(name=item["name"]).first()
            if existing:
                organization_map[item["id"]] = existing.id
                stats["organizations_skipped"] += 1
            else:
                obj = Organization.objects.create(
                    name=item["name"],
                    org_type_id=org_type_map[item["org_type_id"]],
                    notes=item.get("notes", ""),
                )
                organization_map[item["id"]] = obj.id
                stats["organizations_created"] += 1

        # Lists (FK -> Project, nullable)
        for item in data.get("lists", []):
            existing = List.objects.filter(name=item["name"]).first()
            if existing:
                list_map[item["id"]] = existing.id
                stats["lists_skipped"] += 1
            else:
                project_id = None
                if item.get("project_id") is not None:
                    project_id = project_map.get(item["project_id"])
                obj = List.objects.create(
                    name=item["name"],
                    emoji=item.get("emoji", ""),
                    position=item.get("position", 0),
                    project_id=project_id,
                )
                list_map[item["id"]] = obj.id
                stats["lists_created"] += 1

        # ProjectLinks (FK -> Project)
        for item in data.get("project_links", []):
            new_project_id = project_map.get(item["project_id"])
            if new_project_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"ProjectLink {item['id']}: project_id {item['project_id']} not found"
                )
                continue
            existing = ProjectLink.objects.filter(
                project_id=new_project_id,
                url=item["url"],
                descriptor=item["descriptor"],
            ).first()
            if existing:
                stats["project_links_skipped"] += 1
            else:
                ProjectLink.objects.create(
                    project_id=new_project_id,
                    url=item["url"],
                    descriptor=item["descriptor"],
                )
                stats["project_links_created"] += 1

        # Sections (FK -> List)
        for item in data.get("sections", []):
            new_list_id = list_map.get(item["list_id"])
            if new_list_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"Section {item['id']}: list_id {item['list_id']} not found"
                )
                continue
            existing = Section.objects.filter(
                list_id=new_list_id, name=item["name"]
            ).first()
            if existing:
                section_map[item["id"]] = existing.id
                stats["sections_skipped"] += 1
            else:
                obj = Section.objects.create(
                    list_id=new_list_id,
                    name=item["name"],
                    emoji=item.get("emoji", ""),
                    position=item.get("position", 0),
                )
                section_map[item["id"]] = obj.id
                stats["sections_created"] += 1

        # ── 3. Tasks (tree: root first, then children) ──

        task_items = data.get("tasks", [])
        # Sort: root tasks (parent_id=None) first, then by parent_id
        # Build depth map for proper ordering
        parent_lookup = {t["id"]: t.get("parent_id") for t in task_items}

        def _depth(task_id):
            d = 0
            current = parent_lookup.get(task_id)
            while current is not None:
                d += 1
                current = parent_lookup.get(current)
            return d

        sorted_tasks = sorted(task_items, key=lambda t: _depth(t["id"]))

        for item in sorted_tasks:
            new_section_id = section_map.get(item["section_id"])
            if new_section_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"Task {item['id']}: section_id {item['section_id']} not found"
                )
                continue

            new_parent_id = None
            if item.get("parent_id") is not None:
                new_parent_id = task_map.get(item["parent_id"])

            existing = Task.objects.filter(
                section_id=new_section_id,
                title=item["title"],
                parent_id=new_parent_id,
            ).first()
            if existing:
                task_map[item["id"]] = existing.id
                stats["tasks_skipped"] += 1
            else:
                obj = Task.objects.create(
                    section_id=new_section_id,
                    parent_id=new_parent_id,
                    title=item["title"],
                    notes=item.get("notes", ""),
                    due_date=_parse_date_safe(item.get("due_date")),
                    due_time=_parse_time_safe(item.get("due_time")),
                    is_completed=item.get("is_completed", False),
                    completed_at=_parse_datetime_safe(item.get("completed_at")),
                    created_at=_parse_datetime_safe(item.get("created_at")) or None,
                    position=item.get("position", 0),
                    external_id=item.get("external_id"),
                    is_pinned=item.get("is_pinned", False),
                    recurrence_type=item.get("recurrence_type", "none"),
                    recurrence_rule=item.get("recurrence_rule", {}),
                )
                # M2M: tags
                for old_tag_id in item.get("tag_ids", []):
                    new_tag_id = tag_map.get(old_tag_id)
                    if new_tag_id:
                        obj.tags.add(new_tag_id)
                task_map[item["id"]] = obj.id
                stats["tasks_created"] += 1

        # ── 4. Remaining FK-dependent entities ──

        # TimeEntries (FK -> Project, M2M -> Task)
        for item in data.get("time_entries", []):
            new_project_id = project_map.get(item["project_id"])
            if new_project_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"TimeEntry {item['id']}: project_id {item['project_id']} not found"
                )
                continue
            entry_date = _parse_date_safe(item.get("date"))
            existing = TimeEntry.objects.filter(
                project_id=new_project_id,
                date=entry_date,
                description=item.get("description", ""),
            ).first()
            if existing:
                time_entry_map[item["id"]] = existing.id
                stats["time_entries_skipped"] += 1
            else:
                obj = TimeEntry.objects.create(
                    project_id=new_project_id,
                    description=item.get("description", ""),
                    date=entry_date,
                )
                # M2M: tasks
                for old_task_id in item.get("task_ids", []):
                    new_task_id = task_map.get(old_task_id)
                    if new_task_id:
                        obj.tasks.add(new_task_id)
                time_entry_map[item["id"]] = obj.id
                stats["time_entries_created"] += 1

        # Interactions (M2M -> People, FK -> InteractionType)
        for item in data.get("interactions", []):
            # Support both old format (person_id) and new format (person_ids)
            raw_person_ids = item.get("person_ids", [])
            if not raw_person_ids and item.get("person_id") is not None:
                raw_person_ids = [item["person_id"]]
            new_person_ids = [person_map[pid] for pid in raw_person_ids if pid in person_map]
            new_it_id = interaction_type_map.get(item["interaction_type_id"])
            if not new_person_ids or new_it_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"Interaction {item['id']}: person(s) or type not found"
                )
                continue
            i_date = _parse_date_safe(item.get("date"))
            existing = Interaction.objects.filter(
                people__id=new_person_ids[0],
                interaction_type_id=new_it_id,
                date=i_date,
            ).first()
            if existing:
                interaction_map[item["id"]] = existing.id
                stats["interactions_skipped"] += 1
            else:
                obj = Interaction.objects.create(
                    interaction_type_id=new_it_id,
                    date=i_date,
                    notes=item.get("notes", ""),
                )
                obj.people.set(new_person_ids)
                interaction_map[item["id"]] = obj.id
                stats["interactions_created"] += 1

        # Leads (FK -> Person nullable, Organization nullable)
        for item in data.get("leads", []):
            new_person_id = None
            if item.get("person_id") is not None:
                new_person_id = person_map.get(item["person_id"])
            new_org_id = None
            if item.get("organization_id") is not None:
                new_org_id = organization_map.get(item["organization_id"])
            existing = Lead.objects.filter(title=item["title"]).first()
            if existing:
                lead_map[item["id"]] = existing.id
                stats["leads_skipped"] += 1
            else:
                obj = Lead.objects.create(
                    title=item["title"],
                    status=item.get("status", "prospect"),
                    notes=item.get("notes", ""),
                    person_id=new_person_id,
                    organization_id=new_org_id,
                )
                lead_map[item["id"]] = obj.id
                stats["leads_created"] += 1

        # ── 5. Join/link tables ──

        # LeadTasks
        for item in data.get("lead_tasks", []):
            new_lead_id = lead_map.get(item["lead_id"])
            new_task_id = task_map.get(item["task_id"])
            if new_lead_id is None or new_task_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"LeadTask {item['id']}: lead or task not found"
                )
                continue
            existing = LeadTask.objects.filter(
                lead_id=new_lead_id, task_id=new_task_id
            ).first()
            if existing:
                stats["lead_tasks_skipped"] += 1
            else:
                LeadTask.objects.create(lead_id=new_lead_id, task_id=new_task_id)
                stats["lead_tasks_created"] += 1

        # RelationshipPersonPerson
        for item in data.get("relationships_person_person", []):
            new_p1 = person_map.get(item["person_1_id"])
            new_p2 = person_map.get(item["person_2_id"])
            if new_p1 is None or new_p2 is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"RelationshipPP {item['id']}: person not found"
                )
                continue
            existing = RelationshipPersonPerson.objects.filter(
                person_1_id=min(new_p1, new_p2),
                person_2_id=max(new_p1, new_p2),
            ).first()
            if existing:
                stats["relationships_pp_skipped"] += 1
            else:
                obj = RelationshipPersonPerson(
                    person_1_id=new_p1,
                    person_2_id=new_p2,
                    notes=item.get("notes", ""),
                )
                obj.save()  # save() normalizes ordering
                stats["relationships_pp_created"] += 1

        # RelationshipOrganizationPerson
        for item in data.get("relationships_organization_person", []):
            new_org_id = organization_map.get(item["organization_id"])
            new_person_id = person_map.get(item["person_id"])
            if new_org_id is None or new_person_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"RelationshipOP {item['id']}: org or person not found"
                )
                continue
            existing = RelationshipOrganizationPerson.objects.filter(
                organization_id=new_org_id, person_id=new_person_id
            ).first()
            if existing:
                stats["relationships_op_skipped"] += 1
            else:
                RelationshipOrganizationPerson.objects.create(
                    organization_id=new_org_id,
                    person_id=new_person_id,
                    notes=item.get("notes", ""),
                )
                stats["relationships_op_created"] += 1

        # TaskPerson
        for item in data.get("task_persons", []):
            new_task_id = task_map.get(item["task_id"])
            new_person_id = person_map.get(item["person_id"])
            if new_task_id is None or new_person_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"TaskPerson {item['id']}: task or person not found"
                )
                continue
            existing = TaskPerson.objects.filter(
                task_id=new_task_id, person_id=new_person_id
            ).first()
            if existing:
                stats["task_persons_skipped"] += 1
            else:
                TaskPerson.objects.create(
                    task_id=new_task_id, person_id=new_person_id
                )
                stats["task_persons_created"] += 1

        # TaskOrganization
        for item in data.get("task_organizations", []):
            new_task_id = task_map.get(item["task_id"])
            new_org_id = organization_map.get(item["organization_id"])
            if new_task_id is None or new_org_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"TaskOrganization {item['id']}: task or org not found"
                )
                continue
            existing = TaskOrganization.objects.filter(
                task_id=new_task_id, organization_id=new_org_id
            ).first()
            if existing:
                stats["task_organizations_skipped"] += 1
            else:
                TaskOrganization.objects.create(
                    task_id=new_task_id, organization_id=new_org_id
                )
                stats["task_organizations_created"] += 1

        # InteractionTask
        for item in data.get("interaction_tasks", []):
            new_interaction_id = interaction_map.get(item["interaction_id"])
            new_task_id = task_map.get(item["task_id"])
            if new_interaction_id is None or new_task_id is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"InteractionTask {item['id']}: interaction or task not found"
                )
                continue
            existing = InteractionTask.objects.filter(
                interaction_id=new_interaction_id, task_id=new_task_id
            ).first()
            if existing:
                stats["interaction_tasks_skipped"] += 1
            else:
                InteractionTask.objects.create(
                    interaction_id=new_interaction_id, task_id=new_task_id
                )
                stats["interaction_tasks_created"] += 1

        # ── 6. Notebook ──

        # Pages (independent — no FK to other apps)
        for item in data.get("notebook_pages", []):
            existing = Page.objects.filter(slug=item["slug"]).first()
            if existing:
                page_map[item["id"]] = existing.id
                stats["notebook_pages_skipped"] += 1
            else:
                obj = Page(
                    title=item["title"],
                    slug=item["slug"],
                    content=item.get("content", ""),
                    page_type=item.get("page_type", "wiki"),
                    date=_parse_date_safe(item.get("date")),
                )
                obj.save()
                page_map[item["id"]] = obj.id
                stats["notebook_pages_created"] += 1

        # Reconcile entity mentions from content (rebuilds from parsed text)
        if data.get("notebook_pages"):
            from notebook.mentions import reconcile_mentions

            for page in Page.objects.filter(id__in=page_map.values()):
                reconcile_mentions(page)

        # PageLinks (FK -> Page, FK -> Page)
        for item in data.get("page_links", []):
            new_source = page_map.get(item["source_page_id"])
            new_target = page_map.get(item["target_page_id"])
            if new_source is None or new_target is None:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"PageLink {item['id']}: source or target page not found"
                )
                continue
            existing = PageLink.objects.filter(
                source_page_id=new_source, target_page_id=new_target
            ).first()
            if existing:
                stats["page_links_skipped"] += 1
            else:
                PageLink.objects.create(
                    source_page_id=new_source, target_page_id=new_target
                )
                stats["page_links_created"] += 1

    return stats
