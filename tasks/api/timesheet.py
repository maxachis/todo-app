from __future__ import annotations

import datetime

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Router

from tasks.api.schemas import TimeEntryCreateInput, TimeEntrySchema, TimeEntryUpdateInput
from tasks.models import Project, Task, TimeEntry

router = Router(tags=["timesheet"])


def _week_bounds(reference_date: datetime.date):
    days_since_sunday = (reference_date.weekday() + 1) % 7
    sunday = reference_date - datetime.timedelta(days=days_since_sunday)
    saturday = sunday + datetime.timedelta(days=6)
    return sunday, saturday


def _serialize_entry(entry: TimeEntry) -> TimeEntrySchema:
    return TimeEntrySchema(
        id=entry.id,
        project_id=entry.project_id,
        task_ids=list(entry.tasks.values_list("id", flat=True)),
        description=entry.description,
        date=entry.date,
        created_at=entry.created_at,
    )


@router.get("/timesheet/")
def get_timesheet(request, week: str | None = None):
    if week:
        try:
            week_date = datetime.date.fromisoformat(week)
        except ValueError:
            week_date = datetime.date.today()
    else:
        week_date = datetime.date.today()

    week_start, week_end = _week_bounds(week_date)
    entries = (
        TimeEntry.objects.filter(date__gte=week_start, date__lte=week_end)
        .select_related("project")
        .prefetch_related("tasks")
        .order_by("-date", "-created_at")
    )

    # Collect all task IDs across entries and build a lookup for task details
    all_task_ids: set[int] = set()
    for entry in entries:
        all_task_ids.update(entry.tasks.values_list("id", flat=True))

    # Fetch all referenced tasks and their parents in bulk
    task_lookup: dict[int, Task] = {}
    if all_task_ids:
        referenced_tasks = Task.objects.filter(id__in=all_task_ids).select_related(
            "parent", "parent__parent", "parent__parent__parent"
        )
        for t in referenced_tasks:
            task_lookup[t.id] = t

    def _get_parent_titles(task: Task) -> list[str]:
        titles: list[str] = []
        current = task.parent
        while current is not None:
            titles.append(current.title)
            current = current.parent
        titles.reverse()
        return titles

    grouped: dict[str, list[dict]] = {}
    for entry in entries:
        key = entry.date.isoformat()
        task_ids = list(entry.tasks.values_list("id", flat=True))
        task_details = []
        for tid in task_ids:
            task = task_lookup.get(tid)
            if task:
                task_details.append(
                    {
                        "id": task.id,
                        "title": task.title,
                        "parent_titles": _get_parent_titles(task),
                    }
                )
        grouped.setdefault(key, []).append(
            {
                "id": entry.id,
                "project_id": entry.project_id,
                "project_name": entry.project.name,
                "description": entry.description,
                "task_ids": task_ids,
                "task_details": task_details,
                "created_at": entry.created_at.isoformat(),
            }
        )

    weekly_project_hours = (
        entries.values("project_id", "project__name")
        .annotate(hours=models.Count("id"))
        .order_by("-hours")
    )

    # All-time hours per project and overall total
    overall_project_hours = (
        TimeEntry.objects.values("project_id", "project__name")
        .annotate(overall_hours=models.Count("id"))
    )
    overall_lookup: dict[int, dict] = {
        row["project_id"]: {"project_name": row["project__name"], "overall_hours": row["overall_hours"]}
        for row in overall_project_hours
    }
    overall_total_hours = TimeEntry.objects.count()

    # Build per_project: start with weekly-active projects, then add overall-only
    weekly_ids: set[int] = set()
    per_project: list[dict] = []
    for row in weekly_project_hours:
        pid = row["project_id"]
        weekly_ids.add(pid)
        per_project.append({
            "project_id": pid,
            "project_name": row["project__name"],
            "hours": row["hours"],
            "overall_hours": overall_lookup.get(pid, {}).get("overall_hours", 0),
        })

    # Include projects with zero weekly hours but nonzero overall hours
    for pid, info in overall_lookup.items():
        if pid not in weekly_ids:
            per_project.append({
                "project_id": pid,
                "project_name": info["project_name"],
                "hours": 0,
                "overall_hours": info["overall_hours"],
            })

    # Sort: descending weekly hours, then descending overall hours
    per_project.sort(key=lambda p: (-p["hours"], -p["overall_hours"]))

    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "entries_by_date": grouped,
        "summary": {
            "total_hours": entries.count(),
            "overall_total_hours": overall_total_hours,
            "per_project": per_project,
        },
    }


@router.post("/timesheet/", response={201: TimeEntrySchema})
def create_time_entry(request, payload: TimeEntryCreateInput):
    project = get_object_or_404(Project, pk=payload.project_id)
    entry = TimeEntry.objects.create(
        project=project,
        date=payload.date,
        description=payload.description,
    )
    if payload.task_ids:
        entry.tasks.set(payload.task_ids)
    entry.refresh_from_db()
    return 201, _serialize_entry(entry)


@router.put("/timesheet/{entry_id}/", response=TimeEntrySchema)
def update_time_entry(request, entry_id: int, payload: TimeEntryUpdateInput):
    entry = get_object_or_404(TimeEntry, pk=entry_id)
    if payload.description is not None:
        entry.description = payload.description
    entry.save()
    return _serialize_entry(entry)


@router.delete("/timesheet/{entry_id}/", response={204: None})
def delete_time_entry(request, entry_id: int):
    entry = get_object_or_404(TimeEntry, pk=entry_id)
    entry.delete()
    return 204, None
