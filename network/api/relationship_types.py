from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    PersonPersonRelationshipTypeCreateInput,
    PersonPersonRelationshipTypeSchema,
    PersonPersonRelationshipTypeUpdateInput,
    OrgPersonRelationshipTypeCreateInput,
    OrgPersonRelationshipTypeSchema,
    OrgPersonRelationshipTypeUpdateInput,
)
from network.models import PersonPersonRelationshipType, OrgPersonRelationshipType

router = Router(tags=["network-relationship-types"])


# --- Person-Person Relationship Types ---


@router.get("/relationship-types/people/", response=list[PersonPersonRelationshipTypeSchema])
def list_person_person_types(request):
    types = PersonPersonRelationshipType.objects.order_by("name", "id")
    return [PersonPersonRelationshipTypeSchema(id=t.id, name=t.name) for t in types]


@router.post("/relationship-types/people/", response={201: PersonPersonRelationshipTypeSchema})
def create_person_person_type(request, payload: PersonPersonRelationshipTypeCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})
    t = PersonPersonRelationshipType.objects.create(name=name)
    return 201, PersonPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.put("/relationship-types/people/{type_id}/", response=PersonPersonRelationshipTypeSchema)
def update_person_person_type(request, type_id: int, payload: PersonPersonRelationshipTypeUpdateInput):
    t = get_object_or_404(PersonPersonRelationshipType, pk=type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        t.name = cleaned
    t.save()
    return PersonPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.delete("/relationship-types/people/{type_id}/", response={204: None})
def delete_person_person_type(request, type_id: int):
    t = get_object_or_404(PersonPersonRelationshipType, pk=type_id)
    t.delete()
    return 204, None


# --- Org-Person Relationship Types ---


@router.get("/relationship-types/organizations/", response=list[OrgPersonRelationshipTypeSchema])
def list_org_person_types(request):
    types = OrgPersonRelationshipType.objects.order_by("name", "id")
    return [OrgPersonRelationshipTypeSchema(id=t.id, name=t.name) for t in types]


@router.post("/relationship-types/organizations/", response={201: OrgPersonRelationshipTypeSchema})
def create_org_person_type(request, payload: OrgPersonRelationshipTypeCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})
    t = OrgPersonRelationshipType.objects.create(name=name)
    return 201, OrgPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.put("/relationship-types/organizations/{type_id}/", response=OrgPersonRelationshipTypeSchema)
def update_org_person_type(request, type_id: int, payload: OrgPersonRelationshipTypeUpdateInput):
    t = get_object_or_404(OrgPersonRelationshipType, pk=type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        t.name = cleaned
    t.save()
    return OrgPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.delete("/relationship-types/organizations/{type_id}/", response={204: None})
def delete_org_person_type(request, type_id: int):
    t = get_object_or_404(OrgPersonRelationshipType, pk=type_id)
    t.delete()
    return 204, None
