from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    InteractionCreateInput,
    InteractionSchema,
    InteractionUpdateInput,
)
from network.models import Interaction, InteractionMedium, InteractionType, Organization, Person

router = Router(tags=["network-interactions"])


def _serialize_interaction(interaction: Interaction) -> InteractionSchema:
    return InteractionSchema(
        id=interaction.id,
        person_ids=list(interaction.people.values_list("id", flat=True)),
        organization_ids=list(interaction.organizations.values_list("id", flat=True)),
        interaction_type_id=interaction.interaction_type_id,
        interaction_medium_id=interaction.medium_id,
        date=interaction.date,
        notes=interaction.notes,
        created_at=interaction.created_at,
        updated_at=interaction.updated_at,
    )


@router.get("/interactions/", response=list[InteractionSchema])
def list_interactions(request):
    interactions = Interaction.objects.prefetch_related("people", "organizations").order_by("-date", "-id")
    return [_serialize_interaction(interaction) for interaction in interactions]


@router.post("/interactions/", response={201: InteractionSchema})
def create_interaction(request, payload: InteractionCreateInput):
    if not payload.person_ids:
        raise HttpError(422, "person_ids must contain at least one person")
    people = list(Person.objects.filter(pk__in=payload.person_ids))
    if len(people) != len(payload.person_ids):
        raise HttpError(422, "One or more person IDs are invalid")
    interaction_type = get_object_or_404(InteractionType, pk=payload.interaction_type_id)
    medium = None
    if payload.interaction_medium_id is not None:
        medium = get_object_or_404(InteractionMedium, pk=payload.interaction_medium_id)
    interaction = Interaction.objects.create(
        interaction_type=interaction_type,
        medium=medium,
        date=payload.date,
        notes=payload.notes,
    )
    interaction.people.set(people)
    if payload.organization_ids:
        orgs = list(Organization.objects.filter(pk__in=payload.organization_ids))
        if len(orgs) != len(payload.organization_ids):
            raise HttpError(422, "One or more organization IDs are invalid")
        interaction.organizations.set(orgs)
    return 201, _serialize_interaction(interaction)


@router.get("/interactions/{interaction_id}/", response=InteractionSchema)
def get_interaction(request, interaction_id: int):
    interaction = get_object_or_404(Interaction.objects.prefetch_related("people", "organizations"), pk=interaction_id)
    return _serialize_interaction(interaction)


@router.put("/interactions/{interaction_id}/", response=InteractionSchema)
def update_interaction(request, interaction_id: int, payload: InteractionUpdateInput):
    interaction = get_object_or_404(Interaction.objects.prefetch_related("people", "organizations"), pk=interaction_id)

    if payload.person_ids is not None:
        people = list(Person.objects.filter(pk__in=payload.person_ids))
        if len(people) != len(payload.person_ids):
            raise HttpError(422, "One or more person IDs are invalid")
        interaction.people.set(people)

    if payload.organization_ids is not None:
        orgs = list(Organization.objects.filter(pk__in=payload.organization_ids))
        if len(orgs) != len(payload.organization_ids):
            raise HttpError(422, "One or more organization IDs are invalid")
        interaction.organizations.set(orgs)

    if payload.interaction_type_id is not None:
        interaction.interaction_type = get_object_or_404(InteractionType, pk=payload.interaction_type_id)

    if payload.interaction_medium_id is not None:
        interaction.medium = get_object_or_404(InteractionMedium, pk=payload.interaction_medium_id)

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
