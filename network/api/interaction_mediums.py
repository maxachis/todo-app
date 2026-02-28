from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    InteractionMediumCreateInput,
    InteractionMediumSchema,
    InteractionMediumUpdateInput,
)
from network.models import InteractionMedium

router = Router(tags=["network-interaction-mediums"])


def _serialize_interaction_medium(medium: InteractionMedium) -> InteractionMediumSchema:
    return InteractionMediumSchema(id=medium.id, name=medium.name)


@router.get("/interaction-mediums/", response=list[InteractionMediumSchema])
def list_interaction_mediums(request):
    mediums = InteractionMedium.objects.order_by("name", "id")
    return [_serialize_interaction_medium(m) for m in mediums]


@router.post("/interaction-mediums/", response={201: InteractionMediumSchema})
def create_interaction_medium(request, payload: InteractionMediumCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})
    medium = InteractionMedium.objects.create(name=name)
    return 201, _serialize_interaction_medium(medium)


@router.put("/interaction-mediums/{medium_id}/", response=InteractionMediumSchema)
def update_interaction_medium(request, medium_id: int, payload: InteractionMediumUpdateInput):
    medium = get_object_or_404(InteractionMedium, pk=medium_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        medium.name = cleaned
    medium.save()
    return _serialize_interaction_medium(medium)


@router.delete("/interaction-mediums/{medium_id}/", response={204: None})
def delete_interaction_medium(request, medium_id: int):
    medium = get_object_or_404(InteractionMedium, pk=medium_id)
    medium.delete()
    return 204, None
