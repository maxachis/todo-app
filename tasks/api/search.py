from __future__ import annotations

from django.db.models import Q
from ninja import Router

from tasks.models import Task

router = Router(tags=["search"])


@router.get("/search/")
def search_tasks(request, q: str = ""):
    query = q.strip()
    if not query:
        return {"query": "", "total_count": 0, "results": []}

    matched_tasks = (
        Task.objects.filter(
            Q(title__icontains=query)
            | Q(notes__icontains=query)
            | Q(tags__name__icontains=query)
        )
        .select_related("section__list")
        .prefetch_related("tags")
        .distinct()
        .order_by("section__list__position", "section__position", "position")
    )

    grouped: dict[int, dict] = {}
    for task in matched_tasks:
        list_obj = task.section.list
        if list_obj.id not in grouped:
            grouped[list_obj.id] = {
                "list": {"id": list_obj.id, "name": list_obj.name, "emoji": list_obj.emoji},
                "tasks": [],
            }
        grouped[list_obj.id]["tasks"].append(
            {
                "id": task.id,
                "title": task.title,
                "section_name": task.section.name,
                "tags": [tag.name for tag in task.tags.all()],
            }
        )

    return {
        "query": query,
        "total_count": matched_tasks.count(),
        "results": list(grouped.values()),
    }
