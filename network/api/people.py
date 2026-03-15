from django.db.models import Max, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    PersonCreateInput,
    PersonSchema,
    PersonTagSchema,
    PersonUpdateInput,
)
from network.models import Interaction, InteractionType, Person

router = Router(tags=["network-people"])


def _annotate_people(qs):
    latest_type = (
        Interaction.objects.filter(people=OuterRef("pk"))
        .order_by("-date")
        .values("interaction_type__name")[:1]
    )
    return qs.annotate(
        last_interaction_date=Max("interactions__date"),
        last_interaction_type=Subquery(latest_type),
    )


def _serialize_person(person: Person) -> PersonSchema:
    tags = [
        PersonTagSchema(id=t.id, name=t.name)
        for t in person.tags.all()
    ]
    return PersonSchema(
        id=person.id,
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        email=person.email,
        linkedin_url=person.linkedin_url,
        notes=person.notes,
        follow_up_cadence_days=person.follow_up_cadence_days,
        tags=tags,
        last_interaction_date=getattr(person, "last_interaction_date", None),
        last_interaction_type=getattr(person, "last_interaction_type", None),
        created_at=person.created_at,
        updated_at=person.updated_at,
    )


@router.get("/people/", response=list[PersonSchema])
def list_people(request, tag: str | None = None):
    qs = Person.objects.order_by("last_name", "first_name", "id")
    if tag:
        qs = qs.filter(tags__name=tag)
    people = _annotate_people(qs).prefetch_related("tags")
    return [_serialize_person(person) for person in people]


@router.post("/people/", response={201: PersonSchema})
def create_person(request, payload: PersonCreateInput):
    first_name = payload.first_name.strip()
    last_name = payload.last_name.strip()
    if not first_name:
        raise HttpError(422, "First name may not be blank.")
    if not last_name:
        raise HttpError(422, "Last name may not be blank.")

    if Person.objects.filter(
        first_name__iexact=first_name, last_name__iexact=last_name
    ).exists():
        raise HttpError(
            409, f"A person named {first_name} {last_name} already exists."
        )

    person = Person.objects.create(
        first_name=first_name,
        middle_name=payload.middle_name.strip(),
        last_name=last_name,
        email=payload.email.strip(),
        linkedin_url=payload.linkedin_url.strip(),
        notes=payload.notes,
        follow_up_cadence_days=payload.follow_up_cadence_days,
    )
    return 201, _serialize_person(person)


@router.get("/people/{person_id}/", response=PersonSchema)
def get_person(request, person_id: int):
    try:
        person = _annotate_people(Person.objects.all()).prefetch_related("tags").get(pk=person_id)
    except Person.DoesNotExist:
        raise HttpError(404, "Person not found")
    return _serialize_person(person)


@router.put("/people/{person_id}/", response=PersonSchema)
def update_person(request, person_id: int, payload: PersonUpdateInput):
    person = get_object_or_404(Person, pk=person_id)

    if payload.first_name is not None:
        cleaned = payload.first_name.strip()
        if not cleaned:
            raise HttpError(422, "First name may not be blank.")
        person.first_name = cleaned

    if payload.middle_name is not None:
        person.middle_name = payload.middle_name.strip()

    if payload.last_name is not None:
        cleaned = payload.last_name.strip()
        if not cleaned:
            raise HttpError(422, "Last name may not be blank.")
        person.last_name = cleaned

    if payload.email is not None:
        person.email = payload.email.strip()

    if payload.linkedin_url is not None:
        person.linkedin_url = payload.linkedin_url.strip()

    if payload.notes is not None:
        person.notes = payload.notes

    if payload.follow_up_cadence_days is not None:
        person.follow_up_cadence_days = payload.follow_up_cadence_days

    person.save()
    # Re-fetch with annotations to include last_interaction fields
    person = _annotate_people(Person.objects.all()).prefetch_related("tags").get(pk=person.pk)
    return _serialize_person(person)


@router.delete("/people/{person_id}/", response={204: None})
def delete_person(request, person_id: int):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return 204, None
