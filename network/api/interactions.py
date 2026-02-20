from django.shortcuts import get_object_or_404
from ninja import Router

from network.api.schemas import (
    InteractionCreateInput,
    InteractionSchema,
    InteractionUpdateInput,
)
from network.models import Interaction, InteractionType, Person

router = Router(tags=["network-interactions"])


def _serialize_interaction(interaction: Interaction) -> InteractionSchema:
    return InteractionSchema(
        id=interaction.id,
        person_id=interaction.person_id,
        interaction_type_id=interaction.interaction_type_id,
        date=interaction.date,
        notes=interaction.notes,
        created_at=interaction.created_at,
        updated_at=interaction.updated_at,
    )


@router.get("/interactions/", response=list[InteractionSchema])
def list_interactions(request):
    interactions = Interaction.objects.order_by("-date", "-id")
    return [_serialize_interaction(interaction) for interaction in interactions]


@router.post("/interactions/", response={201: InteractionSchema})
def create_interaction(request, payload: InteractionCreateInput):
    person = get_object_or_404(Person, pk=payload.person_id)
    interaction_type = get_object_or_404(InteractionType, pk=payload.interaction_type_id)
    interaction = Interaction.objects.create(
        person=person,
        interaction_type=interaction_type,
        date=payload.date,
        notes=payload.notes,
    )
    return 201, _serialize_interaction(interaction)


@router.get("/interactions/{interaction_id}/", response=InteractionSchema)
def get_interaction(request, interaction_id: int):
    interaction = get_object_or_404(Interaction, pk=interaction_id)
    return _serialize_interaction(interaction)


@router.put("/interactions/{interaction_id}/", response=InteractionSchema)
def update_interaction(request, interaction_id: int, payload: InteractionUpdateInput):
    interaction = get_object_or_404(Interaction, pk=interaction_id)

    if payload.person_id is not None:
        interaction.person = get_object_or_404(Person, pk=payload.person_id)

    if payload.interaction_type_id is not None:
        interaction.interaction_type = get_object_or_404(InteractionType, pk=payload.interaction_type_id)

    if payload.date is not None:
        interaction.date = payload.date

    if payload.notes is not None:
        interaction.notes = payload.notes

    interaction.save()
    return _serialize_interaction(interaction)


@router.delete("/interactions/{interaction_id}/", response={204: None})
def delete_interaction(request, interaction_id: int):
    interaction = get_object_or_404(Interaction, pk=interaction_id)
    interaction.delete()
    return 204, None
