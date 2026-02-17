from __future__ import annotations

from django.db import models
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from tasks.api.lists import _serialize_section
from tasks.api.schemas import MoveInput, SectionCreateInput, SectionSchema, SectionUpdateInput
from tasks.models import List, Section
from tasks.views.reorder import reorder_siblings

router = Router(tags=["sections"])


@router.post("/lists/{list_id}/sections/", response={201: SectionSchema})
def create_section(request, list_id: int, payload: SectionCreateInput):
    task_list = get_object_or_404(List, pk=list_id)
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})

    max_position = task_list.sections.aggregate(max_position=models.Max("position"))["max_position"] or 0
    section = Section.objects.create(
        list=task_list,
        name=name,
        emoji=payload.emoji.strip(),
        position=max_position + 10,
    )
    return 201, _serialize_section(section)


@router.put("/sections/{section_id}/", response=SectionSchema)
def update_section(request, section_id: int, payload: SectionUpdateInput):
    section = get_object_or_404(Section, pk=section_id)

    if payload.name is not None:
        cleaned_name = payload.name.strip()
        if not cleaned_name:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        section.name = cleaned_name
    if payload.emoji is not None:
        section.emoji = payload.emoji.strip()

    section.save()
    return _serialize_section(section)


@router.delete("/sections/{section_id}/", response={204: None})
def delete_section(request, section_id: int):
    section = get_object_or_404(Section, pk=section_id)
    section.delete()
    return 204, None


@router.patch("/sections/{section_id}/move/", response=SectionSchema)
def move_section(request, section_id: int, payload: MoveInput):
    section = get_object_or_404(Section, pk=section_id)
    reorder_siblings(section, section.list.sections.all(), payload.position)
    section.refresh_from_db()
    return _serialize_section(section)
