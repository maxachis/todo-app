from __future__ import annotations

from django.db.models import F, Q
from ninja import Router

from tasks.api.schemas import UpcomingTaskSchema
from tasks.models import Task

router = Router(tags=["upcoming"])


@router.get("/upcoming/", response=list[UpcomingTaskSchema])
def upcoming_tasks(request):
    tasks = (
        Task.objects.filter(
            Q(due_date__isnull=False) | Q(is_pinned=True),
            is_completed=False,
        )
        .select_related("section__list")
        .prefetch_related("tags")
        .order_by(F("due_date").asc(nulls_last=True), F("due_time").asc(nulls_last=True))
    )

    return [
        {
            "id": t.id,
            "title": t.title,
            "due_date": t.due_date,
            "due_time": t.due_time,
            "is_pinned": t.is_pinned,
            "list_id": t.section.list.id,
            "list_name": t.section.list.name,
            "list_emoji": t.section.list.emoji,
            "section_id": t.section.id,
            "section_name": t.section.name,
            "tags": [tag.name for tag in t.tags.all()],
        }
        for t in tasks
    ]
