from __future__ import annotations

import csv
import io
import json
from datetime import date

from django.db import transaction

from tasks.models import List, Section, Tag, Task


def _make_stats() -> dict:
    return {
        "lists_created": 0,
        "sections_created": 0,
        "tags_created": 0,
        "tasks_created": 0,
        "tasks_skipped": 0,
        "parents_linked": 0,
        "errors": 0,
        "error_details": [],
    }


def _get_or_create_list(name: str, emoji: str, position: int, stats: dict) -> List:
    task_list, created = List.objects.get_or_create(
        name=name,
        defaults={"emoji": emoji, "position": position},
    )
    if created:
        stats["lists_created"] += 1
    return task_list


def _get_or_create_section(
    task_list: List, name: str, emoji: str, position: int, stats: dict
) -> Section:
    section, created = Section.objects.get_or_create(
        list=task_list,
        name=name,
        defaults={"emoji": emoji, "position": position},
    )
    if created:
        stats["sections_created"] += 1
    return section


def _attach_tags(task: Task, tag_names: list[str], stats: dict) -> None:
    for tag_name in tag_names:
        if not tag_name:
            continue
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            stats["tags_created"] += 1
        task.tags.add(tag)


def _import_task_tree(
    section: Section,
    task_data: dict,
    parent: Task | None,
    position: int,
    stats: dict,
) -> None:
    """Recursively create a task and its subtasks from JSON export data."""
    title = task_data.get("title", "").strip()
    if not title:
        stats["errors"] += 1
        stats["error_details"].append("Task with empty title skipped")
        return

    # Duplicate detection: title within (list, section)
    existing = Task.objects.filter(
        section=section,
        title=title,
        parent=parent,
    ).first()
    if existing:
        stats["tasks_skipped"] += 1
        # Still recurse into subtasks for skip counting
        for i, sub in enumerate(task_data.get("subtasks", [])):
            _import_task_tree(section, sub, existing, i * 10, stats)
        return

    due_date_raw = task_data.get("due_date")
    due_date = None
    if due_date_raw and due_date_raw != "None":
        try:
            due_date = date.fromisoformat(due_date_raw)
        except (ValueError, TypeError):
            pass

    completed_at_raw = task_data.get("completed_at")
    completed_at = None
    if completed_at_raw and completed_at_raw != "None":
        from django.utils.dateparse import parse_datetime

        completed_at = parse_datetime(completed_at_raw)

    task = Task.objects.create(
        section=section,
        title=title,
        notes=task_data.get("notes", "") or "",
        due_date=due_date,
        is_completed=task_data.get("is_completed", False),
        completed_at=completed_at,
        position=position,
        parent=parent,
    )
    stats["tasks_created"] += 1
    if parent:
        stats["parents_linked"] += 1

    _attach_tags(task, task_data.get("tags", []), stats)

    for i, sub in enumerate(task_data.get("subtasks", [])):
        _import_task_tree(section, sub, task, i * 10, stats)


def import_native_json(file) -> dict:
    """Import tasks from the app's own JSON export format."""
    stats = _make_stats()

    content = file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        stats["errors"] += 1
        stats["error_details"].append(f"Invalid JSON: {e}")
        return stats

    # Normalize: single list object → list of one
    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        stats["errors"] += 1
        stats["error_details"].append("JSON must be a list object or array of list objects")
        return stats

    with transaction.atomic():
        for list_idx, list_data in enumerate(data):
            list_name = list_data.get("name", "").strip()
            if not list_name:
                stats["errors"] += 1
                stats["error_details"].append(f"List at index {list_idx}: missing name")
                continue

            task_list = _get_or_create_list(
                list_name,
                list_data.get("emoji", ""),
                list_data.get("position", list_idx * 10),
                stats,
            )

            for sec_idx, sec_data in enumerate(list_data.get("sections", [])):
                sec_name = sec_data.get("name", "").strip()
                if not sec_name:
                    stats["errors"] += 1
                    stats["error_details"].append(
                        f"Section at index {sec_idx} in list '{list_name}': missing name"
                    )
                    continue

                section = _get_or_create_section(
                    task_list,
                    sec_name,
                    sec_data.get("emoji", ""),
                    sec_data.get("position", sec_idx * 10),
                    stats,
                )

                for task_idx, task_data in enumerate(sec_data.get("tasks", [])):
                    _import_task_tree(
                        section,
                        task_data,
                        None,
                        task_data.get("position", task_idx * 10),
                        stats,
                    )

    return stats


def import_native_csv(file) -> dict:
    """Import tasks from the app's own CSV export format."""
    stats = _make_stats()

    content = file.read()
    if isinstance(content, bytes):
        content = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(content))

    if not reader.fieldnames or "task" not in reader.fieldnames:
        stats["errors"] += 1
        stats["error_details"].append(
            "CSV missing required columns (expected: list, section, task)"
        )
        return stats

    # Track positions and parent resolution
    list_positions: dict[str, int] = {}
    section_positions: dict[tuple[str, str], int] = {}
    # For parent linking: (section_id) -> list of (depth, title, task_pk)
    section_task_stack: dict[int, list[tuple[int, str, int]]] = {}

    with transaction.atomic():
        for row_num, row in enumerate(reader, start=1):
            try:
                title = (row.get("task") or "").strip()
                if not title:
                    stats["errors"] += 1
                    stats["error_details"].append(f"Row {row_num}: missing task title")
                    continue

                list_name = (row.get("list") or "").strip() or "Imported"
                if list_name not in list_positions:
                    list_positions[list_name] = len(list_positions) * 10
                task_list = _get_or_create_list(
                    list_name, "", list_positions[list_name], stats
                )

                section_name = (row.get("section") or "").strip() or "(default)"
                section_key = (list_name, section_name)
                if section_key not in section_positions:
                    section_positions[section_key] = (
                        len([k for k in section_positions if k[0] == list_name]) * 10
                    )
                section = _get_or_create_section(
                    task_list, section_name, "", section_positions[section_key], stats
                )

                # Parse depth and parent
                depth = int(row.get("depth") or "0")
                parent_task_title = (row.get("parent_task") or "").strip()
                parent = None

                if depth > 0 and parent_task_title:
                    stack = section_task_stack.get(section.pk, [])
                    # Walk stack backwards to find parent at depth-1
                    for d, t, pk in reversed(stack):
                        if d == depth - 1 and t == parent_task_title:
                            parent = Task.objects.filter(pk=pk).first()
                            break

                # Duplicate detection
                existing = Task.objects.filter(
                    section=section,
                    title=title,
                    parent=parent,
                ).first()
                if existing:
                    stats["tasks_skipped"] += 1
                    # Still add to stack for child resolution
                    section_task_stack.setdefault(section.pk, []).append(
                        (depth, title, existing.pk)
                    )
                    continue

                # Parse fields
                due_date_raw = (row.get("due_date") or "").strip()
                due_date = None
                if due_date_raw:
                    try:
                        due_date = date.fromisoformat(due_date_raw)
                    except (ValueError, TypeError):
                        pass

                is_completed_raw = (row.get("is_completed") or "").strip()
                is_completed = is_completed_raw.lower() in ("true", "1", "yes")

                notes = row.get("notes") or ""

                task = Task.objects.create(
                    section=section,
                    title=title,
                    notes=notes,
                    due_date=due_date,
                    is_completed=is_completed,
                    position=row_num * 10,
                    parent=parent,
                )
                stats["tasks_created"] += 1
                if parent:
                    stats["parents_linked"] += 1

                # Tags
                tags_raw = (row.get("tags") or "").strip()
                if tags_raw:
                    tag_names = [t.strip() for t in tags_raw.split(",") if t.strip()]
                    _attach_tags(task, tag_names, stats)

                # Add to stack for parent resolution
                section_task_stack.setdefault(section.pk, []).append(
                    (depth, title, task.pk)
                )

            except Exception as e:
                stats["errors"] += 1
                stats["error_details"].append(f"Row {row_num}: {e}")

    return stats


def detect_csv_format(content: str) -> str | None:
    """Detect whether a CSV is native app format or TickTick format.

    Returns 'native', 'ticktick', or None if unrecognized.
    """
    reader = csv.reader(io.StringIO(content))

    # For TickTick CSVs, skip preamble to find the real header
    for row in reader:
        if not row:
            continue
        # TickTick header detection
        if "taskId" in row and "Title" in row:
            return "ticktick"
        # Native header detection
        if "list" in row and "section" in row and "task" in row:
            return "native"
        # If first non-empty row doesn't match either, stop looking
        # (but for TickTick, the preamble rows won't contain either set)
        # Only stop if the row looks like a real header (has multiple columns)
        if len(row) >= 3:
            break

    # If we didn't find a match in the first meaningful row,
    # do a full scan for TickTick (which has a preamble)
    reader = csv.reader(io.StringIO(content))
    for row in reader:
        if "taskId" in row and "Title" in row:
            return "ticktick"

    return None
