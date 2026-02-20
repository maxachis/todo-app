from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    InteractionTypeCreateInput,
    InteractionTypeSchema,
    InteractionTypeUpdateInput,
)
from network.models import InteractionType

router = Router(tags=["network-interaction-types"])


def _serialize_interaction_type(interaction_type: InteractionType) -> InteractionTypeSchema:
    return InteractionTypeSchema(id=interaction_type.id, name=interaction_type.name)


@router.get("/interaction-types/", response=list[InteractionTypeSchema])
def list_interaction_types(request):
    interaction_types = InteractionType.objects.order_by("name", "id")
    return [_serialize_interaction_type(interaction_type) for interaction_type in interaction_types]


@router.post("/interaction-types/", response={201: InteractionTypeSchema})
def create_interaction_type(request, payload: InteractionTypeCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})
    interaction_type = InteractionType.objects.create(name=name)
    return 201, _serialize_interaction_type(interaction_type)


@router.put("/interaction-types/{interaction_type_id}/", response=InteractionTypeSchema)
def update_interaction_type(request, interaction_type_id: int, payload: InteractionTypeUpdateInput):
    interaction_type = get_object_or_404(InteractionType, pk=interaction_type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        interaction_type.name = cleaned
    interaction_type.save()
    return _serialize_interaction_type(interaction_type)


@router.delete("/interaction-types/{interaction_type_id}/", response={204: None})
def delete_interaction_type(request, interaction_type_id: int):
    interaction_type = get_object_or_404(InteractionType, pk=interaction_type_id)
    interaction_type.delete()
    return 204, None
