from __future__ import annotations

import datetime

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Router

from tasks.api.schemas import TimeEntryCreateInput, TimeEntrySchema
from tasks.models import Project, TimeEntry

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

    grouped: dict[str, list[dict]] = {}
    for entry in entries:
        key = entry.date.isoformat()
        grouped.setdefault(key, []).append(
            {
                "id": entry.id,
                "project_id": entry.project_id,
                "project_name": entry.project.name,
                "description": entry.description,
                "task_ids": list(entry.tasks.values_list("id", flat=True)),
                "created_at": entry.created_at.isoformat(),
            }
        )

    project_hours = (
        entries.values("project_id", "project__name")
        .annotate(hours=models.Count("id"))
        .order_by("-hours")
    )

    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "entries_by_date": grouped,
        "summary": {
            "total_hours": entries.count(),
            "per_project": [
                {
                    "project_id": row["project_id"],
                    "project_name": row["project__name"],
                    "hours": row["hours"],
                }
                for row in project_hours
            ],
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


@router.delete("/timesheet/{entry_id}/", response={204: None})
def delete_time_entry(request, entry_id: int):
    entry = get_object_or_404(TimeEntry, pk=entry_id)
    entry.delete()
    return 204, None
