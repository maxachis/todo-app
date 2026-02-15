import csv
import io
from datetime import datetime, date, time

from django.utils import timezone

from tasks.models import List, Section, Tag, Task


def parse_ticktick_datetime(value):
    """Parse a TickTick datetime string into a timezone-aware datetime."""
    if not value or not value.strip():
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = timezone.make_aware(dt)
            return dt
        except ValueError:
            continue
    # Try date-only
    try:
        d = datetime.strptime(value, "%Y-%m-%d")
        return timezone.make_aware(d)
    except ValueError:
        return None


def parse_due_date(due_date_str, is_all_day_str):
    """Parse TickTick due date into (date, time) tuple."""
    if not due_date_str or not due_date_str.strip():
        return None, None
    dt = parse_ticktick_datetime(due_date_str)
    if dt is None:
        return None, None
    is_all_day = is_all_day_str.strip().lower() in ("true", "1", "yes") if is_all_day_str else True
    if is_all_day:
        return dt.date(), None
    return dt.date(), dt.timetz().replace(tzinfo=None)


def parse_tags(tags_str):
    """Parse comma or semicolon separated tags string into a list of names."""
    if not tags_str or not tags_str.strip():
        return []
    # TickTick uses comma separation, but handle semicolons too
    tags_str = tags_str.replace(";", ",")
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def import_ticktick_csv(csv_file):
    """Import tasks from a TickTick CSV backup file.

    Returns a stats dict with counts of created/skipped items.
    """
    stats = {
        "lists_created": 0,
        "sections_created": 0,
        "tags_created": 0,
        "tasks_created": 0,
        "tasks_skipped": 0,
        "parents_linked": 0,
        "errors": 0,
        "error_details": [],
    }

    content = csv_file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8-sig")

    # TickTick CSVs have a metadata preamble (date, version, status legend)
    # before the real header row. Scan to find the header containing "Title".
    raw_reader = csv.reader(io.StringIO(content))
    fieldnames = None
    preamble_rows = 0
    for row in raw_reader:
        preamble_rows += 1
        if "Title" in row and "taskId" in row:
            fieldnames = row
            break

    if not fieldnames:
        stats["errors"] += 1
        stats["error_details"].append(
            "Could not find CSV header row (expected columns: Title, taskId)"
        )
        return stats

    # Continue reading from where raw_reader left off — remaining rows are data
    reader = csv.DictReader(io.StringIO(content), fieldnames=fieldnames)
    # Skip the preamble + header rows we already consumed
    for _ in range(preamble_rows):
        next(reader)

    # Track first-seen order for position assignment
    list_positions = {}  # name -> position
    section_positions = {}  # (list_name, section_name) -> position
    task_group_counters = {}  # (section_id, parent_external_id) -> counter

    # Maps for parent linking
    external_id_to_pk = {}  # taskId -> django pk
    rows_with_parents = []  # (child_pk, parent_external_id)

    for row_num, row in enumerate(reader, start=1):
        try:
            title = row.get("Title", "").strip()
            if not title:
                stats["errors"] += 1
                stats["error_details"].append(f"Row {row_num}: missing title, skipped")
                continue

            task_id = row.get("taskId", "").strip()
            if not task_id:
                stats["errors"] += 1
                stats["error_details"].append(
                    f"Row {row_num}: missing taskId, skipped"
                )
                continue

            # Idempotency: skip if already imported
            existing = Task.objects.filter(external_id=task_id).first()
            if existing:
                external_id_to_pk[task_id] = existing.pk
                parent_id = row.get("parentId", "").strip()
                if parent_id:
                    rows_with_parents.append((existing.pk, parent_id))
                stats["tasks_skipped"] += 1
                continue

            # Get or create List
            list_name = row.get("List Name", "").strip() or "Imported"
            if list_name not in list_positions:
                list_positions[list_name] = len(list_positions) * 10
            task_list, list_created = List.objects.get_or_create(
                name=list_name,
                defaults={"position": list_positions[list_name]},
            )
            if list_created:
                stats["lists_created"] += 1

            # Get or create Section
            section_name = row.get("Column Name", "").strip() or "(default)"
            section_key = (list_name, section_name)
            if section_key not in section_positions:
                section_positions[section_key] = len(
                    [k for k in section_positions if k[0] == list_name]
                ) * 10
            section, section_created = Section.objects.get_or_create(
                list=task_list,
                name=section_name,
                defaults={"position": section_positions[section_key]},
            )
            if section_created:
                stats["sections_created"] += 1

            # Position within (section, parent) group
            parent_external_id = row.get("parentId", "").strip() or None
            group_key = (section.pk, parent_external_id)
            if group_key not in task_group_counters:
                task_group_counters[group_key] = 0
            task_group_counters[group_key] += 1
            position = task_group_counters[group_key] * 10

            # Parse fields
            notes = row.get("Content", "").strip()
            priority = int(row.get("Priority", "0") or "0")
            if priority not in (0, 1, 3, 5):
                priority = 0

            status = int(row.get("Status", "0") or "0")
            is_completed = status in (1, 2)  # 0=Normal, 1=Completed, 2=Archived

            due_d, due_t = parse_due_date(
                row.get("Due Date", ""), row.get("Is All Day", "")
            )
            created_at = parse_ticktick_datetime(row.get("Created Time", ""))
            completed_at = parse_ticktick_datetime(row.get("Completed Time", ""))

            task = Task.objects.create(
                section=section,
                title=title,
                notes=notes,
                priority=priority,
                due_date=due_d,
                due_time=due_t,
                is_completed=is_completed,
                completed_at=completed_at,
                created_at=created_at or timezone.now(),
                position=position,
                external_id=task_id,
            )

            external_id_to_pk[task_id] = task.pk
            stats["tasks_created"] += 1

            # Queue parent linking
            if parent_external_id:
                rows_with_parents.append((task.pk, parent_external_id))

            # Parse and attach tags
            tag_names = parse_tags(row.get("Tags", ""))
            for tag_name in tag_names:
                tag, tag_created = Tag.objects.get_or_create(name=tag_name)
                if tag_created:
                    stats["tags_created"] += 1
                task.tags.add(tag)

        except Exception as e:
            stats["errors"] += 1
            stats["error_details"].append(f"Row {row_num}: {e}")

    # Pass 2: Link parents
    for child_pk, parent_external_id in rows_with_parents:
        parent_pk = external_id_to_pk.get(parent_external_id)
        if parent_pk:
            Task.objects.filter(pk=child_pk).update(parent_id=parent_pk)
            stats["parents_linked"] += 1

    return stats
