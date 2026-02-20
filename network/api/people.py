from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    PersonCreateInput,
    PersonSchema,
    PersonUpdateInput,
)
from network.models import Person

router = Router(tags=["network-people"])


def _serialize_person(person: Person) -> PersonSchema:
    return PersonSchema(
        id=person.id,
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        notes=person.notes,
        follow_up_cadence_days=person.follow_up_cadence_days,
        created_at=person.created_at,
        updated_at=person.updated_at,
    )


@router.get("/people/", response=list[PersonSchema])
def list_people(request):
    people = Person.objects.order_by("last_name", "first_name", "id")
    return [_serialize_person(person) for person in people]


@router.post("/people/", response={201: PersonSchema})
def create_person(request, payload: PersonCreateInput):
    first_name = payload.first_name.strip()
    last_name = payload.last_name.strip()
    if not first_name:
        raise HttpError(422, {"first_name": ["This field may not be blank."]})
    if not last_name:
        raise HttpError(422, {"last_name": ["This field may not be blank."]})

    person = Person.objects.create(
        first_name=first_name,
        middle_name=payload.middle_name.strip(),
        last_name=last_name,
        notes=payload.notes,
        follow_up_cadence_days=payload.follow_up_cadence_days,
    )
    return 201, _serialize_person(person)


@router.get("/people/{person_id}/", response=PersonSchema)
def get_person(request, person_id: int):
    person = get_object_or_404(Person, pk=person_id)
    return _serialize_person(person)


@router.put("/people/{person_id}/", response=PersonSchema)
def update_person(request, person_id: int, payload: PersonUpdateInput):
    person = get_object_or_404(Person, pk=person_id)

    if payload.first_name is not None:
        cleaned = payload.first_name.strip()
        if not cleaned:
            raise HttpError(422, {"first_name": ["This field may not be blank."]})
        person.first_name = cleaned

    if payload.middle_name is not None:
        person.middle_name = payload.middle_name.strip()

    if payload.last_name is not None:
        cleaned = payload.last_name.strip()
        if not cleaned:
            raise HttpError(422, {"last_name": ["This field may not be blank."]})
        person.last_name = cleaned

    if payload.notes is not None:
        person.notes = payload.notes

    if payload.follow_up_cadence_days is not None:
        person.follow_up_cadence_days = payload.follow_up_cadence_days

    person.save()
    return _serialize_person(person)


@router.delete("/people/{person_id}/", response={204: None})
def delete_person(request, person_id: int):
    person = get_object_or_404(Person, pk=person_id)
    person.delete()
    return 204, None
