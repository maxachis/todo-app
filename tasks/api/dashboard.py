from __future__ import annotations

from datetime import date, timedelta

from django.db.models import Count, Max, Q
from django.utils import timezone
from ninja import Router

from tasks.api.schemas import (
    FollowUpCompliance,
    FollowUpDueItem,
    TrendsResponse,
    WeeklyCount,
)
from network.models.interaction import Interaction
from network.models.person import Person
from tasks.models import Task

router = Router(tags=["dashboard"])


def _monday_of(d: date) -> date:
    return d - timedelta(days=d.weekday())


@router.get("/dashboard/trends/", response=TrendsResponse)
def dashboard_trends(request):
    today = timezone.now().date()
    current_monday = _monday_of(today)
    start_monday = current_monday - timedelta(weeks=12)

    # Build list of all week-start Mondays (13 entries: 12 past + current)
    week_starts = [start_monday + timedelta(weeks=i) for i in range(13)]

    # Interactions per week
    interactions_qs = (
        Interaction.objects.filter(date__gte=start_monday)
        .extra(select={"week_start": "date(date, 'weekday 0', '-6 days')"})
        .values("week_start")
        .annotate(count=Count("id"))
    )
    interaction_counts = {row["week_start"]: row["count"] for row in interactions_qs}

    interactions_per_week = [
        {"week_start": ws.isoformat(), "count": interaction_counts.get(ws.isoformat(), 0)}
        for ws in week_starts
    ]

    # Tasks completed per week
    tasks_qs = (
        Task.objects.filter(completed_at__isnull=False, completed_at__date__gte=start_monday)
        .extra(select={"week_start": "date(completed_at, 'weekday 0', '-6 days')"})
        .values("week_start")
        .annotate(count=Count("id"))
    )
    task_counts = {row["week_start"]: row["count"] for row in tasks_qs}

    tasks_completed_per_week = [
        {"week_start": ws.isoformat(), "count": task_counts.get(ws.isoformat(), 0)}
        for ws in week_starts
    ]

    # Follow-up compliance
    people_with_cadence = Person.objects.filter(
        follow_up_cadence_days__isnull=False
    ).annotate(
        last_interaction=Max("interactions__date")
    )

    total = 0
    on_track = 0
    overdue_count = 0
    for person in people_with_cadence:
        total += 1
        if person.last_interaction is None:
            overdue_count += 1
        else:
            days_since = (today - person.last_interaction).days
            if days_since > person.follow_up_cadence_days:
                overdue_count += 1
            else:
                on_track += 1

    return {
        "interactions_per_week": interactions_per_week,
        "tasks_completed_per_week": tasks_completed_per_week,
        "follow_up_compliance": {
            "on_track": on_track,
            "total": total,
            "overdue_count": overdue_count,
        },
    }


@router.get("/dashboard/follow-ups-due/", response=list[FollowUpDueItem])
def follow_ups_due(request):
    today = timezone.now().date()

    people_with_cadence = Person.objects.filter(
        follow_up_cadence_days__isnull=False
    ).annotate(
        last_interaction=Max("interactions__date")
    )

    results = []
    for person in people_with_cadence:
        if person.last_interaction is None:
            days_since = (today - person.created_at.date()).days
            days_overdue = days_since - person.follow_up_cadence_days
        else:
            days_since = (today - person.last_interaction).days
            days_overdue = days_since - person.follow_up_cadence_days

        if days_overdue > 0:
            results.append({
                "person_id": person.id,
                "first_name": person.first_name,
                "last_name": person.last_name,
                "follow_up_cadence_days": person.follow_up_cadence_days,
                "last_interaction_date": person.last_interaction.isoformat() if person.last_interaction else None,
                "days_overdue": days_overdue,
            })

    results.sort(key=lambda x: x["days_overdue"], reverse=True)
    return results
