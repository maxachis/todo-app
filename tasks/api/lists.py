from __future__ import annotations

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from tasks.api.schemas import (
    ListCreateInput,
    ListSchema,
    ListUpdateInput,
    MoveInput,
    SectionSchema,
    TagSchema,
    TaskSchema,
)
from tasks.models import List, Project, Section, Task
from tasks.views.reorder import reorder_siblings

router = Router(tags=["lists"])


def _serialize_task(task: Task) -> TaskSchema:
    subtasks = [
        _serialize_task(subtask)
        for subtask in task.subtasks.order_by("position").all()
    ]
    return TaskSchema(
        id=task.id,
        section_id=task.section_id,
        parent_id=task.parent_id,
        title=task.title,
        notes=task.notes,
        priority=task.priority,
        due_date=task.due_date,
        due_time=task.due_time,
        is_completed=task.is_completed,
        completed_at=task.completed_at,
        created_at=task.created_at,
        position=task.position,
        external_id=task.external_id,
        is_pinned=task.is_pinned,
        tags=[TagSchema(id=tag.id, name=tag.name) for tag in task.tags.all()],
        subtasks=subtasks,
    )


def _serialize_section(section: Section) -> SectionSchema:
    top_level_tasks = section.tasks.filter(parent__isnull=True).order_by("position")
    return SectionSchema(
        id=section.id,
        list_id=section.list_id,
        name=section.name,
        emoji=section.emoji,
        position=section.position,
        tasks=[_serialize_task(task) for task in top_level_tasks],
    )


def _serialize_list(task_list: List, include_sections: bool = False) -> ListSchema:
    sections: list[SectionSchema] = []
    if include_sections:
        sections = [_serialize_section(section) for section in task_list.sections.order_by("position")]
    return ListSchema(
        id=task_list.id,
        name=task_list.name,
        emoji=task_list.emoji,
        position=task_list.position,
        project_id=task_list.project_id,
        sections=sections,
    )


@router.get("/lists/", response=list[ListSchema])
def get_lists(request):
    lists = List.objects.order_by("position")
    return [_serialize_list(task_list) for task_list in lists]


@router.post("/lists/", response={201: ListSchema})
def create_list(request, payload: ListCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})

    project = None
    if payload.project_id is not None:
        project = get_object_or_404(Project, pk=payload.project_id)

    max_pos = List.objects.aggregate(max_position=models.Max("position"))["max_position"] or 0
    task_list = List.objects.create(
        name=name,
        emoji=payload.emoji.strip(),
        project=project,
        position=max_pos + 10,
    )
    return 201, _serialize_list(task_list)


@router.get("/lists/{list_id}/", response=ListSchema)
def get_list_detail(request, list_id: int):
    task_list = get_object_or_404(List.objects.order_by("position"), pk=list_id)
    return _serialize_list(task_list, include_sections=True)


@router.put("/lists/{list_id}/", response=ListSchema)
def update_list(request, list_id: int, payload: ListUpdateInput):
    task_list = get_object_or_404(List, pk=list_id)

    if payload.name is not None:
        cleaned_name = payload.name.strip()
        if not cleaned_name:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        task_list.name = cleaned_name

    if payload.emoji is not None:
        task_list.emoji = payload.emoji.strip()

    if payload.project_id is not None:
        task_list.project = get_object_or_404(Project, pk=payload.project_id)

    task_list.save()
    return _serialize_list(task_list)


@router.delete("/lists/{list_id}/", response={204: None})
def delete_list(request, list_id: int):
    task_list = get_object_or_404(List, pk=list_id)
    task_list.delete()
    return 204, None


@router.patch("/lists/{list_id}/move/", response=ListSchema)
def move_list(request, list_id: int, payload: MoveInput):
    task_list = get_object_or_404(List, pk=list_id)
    reorder_siblings(task_list, List.objects.all(), payload.position)
    task_list.refresh_from_db()
    return _serialize_list(task_list)
