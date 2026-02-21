import csv
import io
import json

from django.http import HttpResponse, HttpResponseBadRequest

from tasks.models import List, Task


def _get_task_depth(task):
    """Calculate nesting depth of a task."""
    depth = 0
    current = task
    while current.parent is not None:
        depth += 1
        current = current.parent
    return depth


def _build_task_tree(task):
    """Recursively build a dict for a task and its subtasks."""
    return {
        "title": task.title,
        "notes": task.notes,
        "due_date": str(task.due_date) if task.due_date else None,
        "is_completed": task.is_completed,
        "completed_at": str(task.completed_at) if task.completed_at else None,
        "position": task.position,
        "tags": list(task.tags.values_list("name", flat=True)),
        "recurrence_type": task.recurrence_type,
        "recurrence_rule": task.recurrence_rule,
        "subtasks": [
            _build_task_tree(sub)
            for sub in task.subtasks.all().order_by("position")
        ],
    }


def serialize_list_to_json(task_list):
    """Build nested dict: list > sections > tasks > subtasks."""
    return {
        "name": task_list.name,
        "emoji": task_list.emoji,
        "position": task_list.position,
        "sections": [
            {
                "name": section.name,
                "emoji": section.emoji,
                "position": section.position,
                "tasks": [
                    _build_task_tree(task)
                    for task in section.tasks.filter(parent=None).order_by("position")
                ],
            }
            for section in task_list.sections.all().order_by("position")
        ],
    }


def _flatten_tasks(task_list, section, task, rows):
    """Recursively flatten a task and its subtasks into CSV rows."""
    depth = _get_task_depth(task)
    recurrence = ""
    if task.recurrence_type and task.recurrence_type != "none":
        recurrence = task.recurrence_type
    rows.append({
        "list": task_list.name,
        "section": section.name,
        "task": task.title,
        "parent_task": task.parent.title if task.parent else "",
        "depth": str(depth),
        "notes": task.notes,
        "due_date": str(task.due_date) if task.due_date else "",
        "tags": ",".join(task.tags.values_list("name", flat=True)),
        "is_completed": str(task.is_completed),
        "recurrence": recurrence,
    })
    for sub in task.subtasks.all().order_by("position"):
        _flatten_tasks(task_list, section, sub, rows)


def serialize_list_to_csv(task_list):
    """Flatten tasks to rows with specified columns."""
    output = io.StringIO()
    fieldnames = [
        "list", "section", "task", "parent_task", "depth",
        "notes", "due_date", "tags", "is_completed", "recurrence",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for section in task_list.sections.all().order_by("position"):
        for task in section.tasks.filter(parent=None).order_by("position"):
            _flatten_tasks(task_list, section, task, [])

    # Rebuild properly with all rows
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    rows = []
    for section in task_list.sections.all().order_by("position"):
        for task in section.tasks.filter(parent=None).order_by("position"):
            _flatten_tasks(task_list, section, task, rows)

    for row in rows:
        writer.writerow(row)

    return output.getvalue()


def _render_task_markdown(task, depth=0):
    """Render a task as markdown with indentation."""
    indent = "  " * depth
    checkbox = "[x]" if task.is_completed else "[ ]"
    lines = [f"{indent}- {checkbox} {task.title}"]

    if task.notes:
        for line in task.notes.split("\n"):
            lines.append(f"{indent}  {line}")

    if task.due_date:
        lines.append(f"{indent}  Due: {task.due_date}")

    tag_names = list(task.tags.values_list("name", flat=True))
    if tag_names:
        lines.append(f"{indent}  Tags: {', '.join(tag_names)}")

    for sub in task.subtasks.all().order_by("position"):
        lines.extend(_render_task_markdown(sub, depth + 1))

    return lines


def serialize_list_to_markdown(task_list):
    """Render list as markdown document."""
    lines = [f"# {task_list.name}", ""]

    for section in task_list.sections.all().order_by("position"):
        lines.append(f"## {section.name}")
        lines.append("")

        for task in section.tasks.filter(parent=None).order_by("position"):
            lines.extend(_render_task_markdown(task))

        lines.append("")

    return "\n".join(lines)


def export_list_view(request, list_id, fmt):
    """Export a single list in the given format."""
    try:
        task_list = List.objects.get(pk=list_id)
    except List.DoesNotExist:
        from django.http import Http404
        raise Http404("List not found")

    return _export_response(task_list.name, fmt, [task_list])


def export_all_view(request, fmt):
    """Export all lists in the given format."""
    lists = List.objects.all().order_by("position")
    return _export_response("all-lists", fmt, lists)


def _export_response(filename_base, fmt, lists):
    """Build the HTTP response for an export."""
    if fmt == "json":
        if len(lists) == 1:
            data = serialize_list_to_json(lists[0])
        else:
            data = [serialize_list_to_json(lst) for lst in lists]
        content = json.dumps(data, indent=2)
        content_type = "application/json"
        ext = "json"
    elif fmt == "csv":
        parts = []
        for lst in lists:
            parts.append(serialize_list_to_csv(lst))
        content = "".join(parts)
        # If multiple lists concatenated, only keep headers from first
        if len(parts) > 1:
            lines = []
            header_seen = False
            for part in parts:
                for i, line in enumerate(part.split("\n")):
                    if i == 0 and header_seen:
                        continue
                    lines.append(line)
                header_seen = True
            content = "\n".join(lines)
        content_type = "text/csv"
        ext = "csv"
    elif fmt == "md":
        parts = [serialize_list_to_markdown(lst) for lst in lists]
        content = "\n".join(parts)
        content_type = "text/markdown"
        ext = "md"
    else:
        return HttpResponseBadRequest(f"Unsupported export format: {fmt}")

    response = HttpResponse(content, content_type=content_type)
    safe_name = filename_base.replace(" ", "-").lower()
    response["Content-Disposition"] = f'attachment; filename="{safe_name}.{ext}"'
    return response
