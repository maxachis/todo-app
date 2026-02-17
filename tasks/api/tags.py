from __future__ import annotations

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from tasks.api.schemas import TagInput, TagSchema
from tasks.models import Tag, Task

router = Router(tags=["tags"])


@router.post("/tasks/{task_id}/tags/", response=list[TagSchema])
def add_tag(request, task_id: int, payload: TagInput):
    task = get_object_or_404(Task, pk=task_id)
    name = payload.name.strip()
    if not name:
        raise HttpError(422, "Tag name may not be blank.")

    tag, _ = Tag.objects.get_or_create(name=name)
    task.tags.add(tag)
    return [TagSchema(id=t.id, name=t.name) for t in task.tags.order_by("name")]


@router.delete("/tasks/{task_id}/tags/{tag_id}/", response={204: None})
def remove_tag(request, task_id: int, tag_id: int):
    task = get_object_or_404(Task, pk=task_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    task.tags.remove(tag)
    return 204, None


@router.get("/tags/", response=list[TagSchema])
def list_tags(request, exclude_task: int | None = None):
    tags = Tag.objects.all()
    if exclude_task is not None:
        task = get_object_or_404(Task, pk=exclude_task)
        tags = tags.exclude(pk__in=task.tags.values_list("id", flat=True))
    return [TagSchema(id=tag.id, name=tag.name) for tag in tags.order_by("name")]
