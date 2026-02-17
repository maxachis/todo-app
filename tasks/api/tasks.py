from __future__ import annotations

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from tasks.api.lists import _serialize_task
from tasks.api.schemas import TaskCreateInput, TaskMoveInput, TaskSchema, TaskUpdateInput
from tasks.models import List, Section, Task
from tasks.views.reorder import reorder_siblings

router = Router(tags=["tasks"])

MAX_PINNED_PER_LIST = 3


def _descendants(task: Task):
    for child in task.subtasks.all():
        yield child
        yield from _descendants(child)


def _update_subtask_sections(task: Task, section: Section):
    for subtask in task.subtasks.all():
        subtask.section = section
        subtask.save(update_fields=["section"])
        _update_subtask_sections(subtask, section)


@router.post("/sections/{section_id}/tasks/", response={201: TaskSchema})
def create_task(request, section_id: int, payload: TaskCreateInput):
    section = get_object_or_404(Section, pk=section_id)
    title = payload.title.strip()
    if not title:
        raise HttpError(422, {"title": ["This field may not be blank."]})

    parent = None
    if payload.parent_id is not None:
        parent = get_object_or_404(Task, pk=payload.parent_id)
        if parent.section_id != section.id:
            raise HttpError(422, "Parent task must belong to the same section.")

    max_position = (
        Task.objects.filter(section=section, parent=parent).aggregate(max_position=models.Max("position"))[
            "max_position"
        ]
        or 0
    )
    task = Task.objects.create(
        section=section,
        parent=parent,
        title=title,
        position=max_position + 10,
    )
    return 201, _serialize_task(task)


@router.get("/tasks/{task_id}/", response=TaskSchema)
def get_task_detail(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    return _serialize_task(task)


@router.put("/tasks/{task_id}/", response=TaskSchema)
def update_task(request, task_id: int, payload: TaskUpdateInput):
    task = get_object_or_404(Task, pk=task_id)

    if payload.title is not None:
        cleaned_title = payload.title.strip()
        if not cleaned_title:
            raise HttpError(422, {"title": ["This field may not be blank."]})
        task.title = cleaned_title
    if payload.notes is not None:
        task.notes = payload.notes
    if payload.due_date is not None:
        task.due_date = payload.due_date
    if payload.due_time is not None:
        task.due_time = payload.due_time
    if payload.priority is not None:
        task.priority = payload.priority

    task.save()
    task.refresh_from_db()
    return _serialize_task(task)


@router.delete("/tasks/{task_id}/", response={204: None})
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return 204, None


@router.post("/tasks/{task_id}/complete/", response=TaskSchema)
def complete_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.complete()
    task.refresh_from_db()
    return _serialize_task(task)


@router.post("/tasks/{task_id}/uncomplete/", response=TaskSchema)
def uncomplete_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.uncomplete()
    task.refresh_from_db()
    return _serialize_task(task)


@router.patch("/tasks/{task_id}/move/", response=TaskSchema)
def move_task(request, task_id: int, payload: TaskMoveInput):
    task = get_object_or_404(Task, pk=task_id)
    fields_set = payload.model_fields_set

    if "list_id" in fields_set and payload.list_id is not None:
        target_list = get_object_or_404(List, pk=payload.list_id)
        target_section = target_list.sections.order_by("position").first()
        if target_section is None:
            raise HttpError(400, "Target list has no sections.")
        task.section = target_section
        task.parent = None
        _update_subtask_sections(task, target_section)

    if "section_id" in fields_set and payload.section_id is not None:
        section = get_object_or_404(Section, pk=payload.section_id)
        task.section = section
        _update_subtask_sections(task, section)

    if "parent_id" in fields_set:
        if payload.parent_id is None:
            task.parent = None
        else:
            new_parent = get_object_or_404(Task, pk=payload.parent_id)
            descendant_ids = {descendant.id for descendant in _descendants(task)}
            if new_parent.id in descendant_ids:
                raise HttpError(409, "Cannot nest a task under its own descendant.")
            task.parent = new_parent
            task.section = new_parent.section
            _update_subtask_sections(task, new_parent.section)

    task.save()

    if "position" in fields_set and payload.position is not None:
        siblings = Task.objects.filter(section=task.section, parent=task.parent)
        reorder_siblings(task, siblings, payload.position)
        task.refresh_from_db()

    return _serialize_task(task)


@router.post("/tasks/{task_id}/pin/", response=TaskSchema)
def pin_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task_list = task.section.list

    if task.is_pinned:
        task.is_pinned = False
        task.save(update_fields=["is_pinned"])
        return _serialize_task(task)

    pinned_count = Task.objects.filter(
        section__list=task_list, is_pinned=True, is_completed=False
    ).count()
    if pinned_count >= MAX_PINNED_PER_LIST:
        raise HttpError(409, "Maximum pinned task limit reached for this list.")

    task.is_pinned = True
    task.save(update_fields=["is_pinned"])
    return _serialize_task(task)
