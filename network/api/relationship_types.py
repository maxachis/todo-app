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
    OrgOrgRelationshipTypeCreateInput,
    OrgOrgRelationshipTypeSchema,
    OrgOrgRelationshipTypeUpdateInput,
)
from network.models import PersonPersonRelationshipType, OrgPersonRelationshipType, OrgOrgRelationshipType

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
        raise HttpError(422, "Name may not be blank.")
    t = PersonPersonRelationshipType.objects.create(name=name)
    return 201, PersonPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.put("/relationship-types/people/{type_id}/", response=PersonPersonRelationshipTypeSchema)
def update_person_person_type(request, type_id: int, payload: PersonPersonRelationshipTypeUpdateInput):
    t = get_object_or_404(PersonPersonRelationshipType, pk=type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, "Name may not be blank.")
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
        raise HttpError(422, "Name may not be blank.")
    t = OrgPersonRelationshipType.objects.create(name=name)
    return 201, OrgPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.put("/relationship-types/organizations/{type_id}/", response=OrgPersonRelationshipTypeSchema)
def update_org_person_type(request, type_id: int, payload: OrgPersonRelationshipTypeUpdateInput):
    t = get_object_or_404(OrgPersonRelationshipType, pk=type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, "Name may not be blank.")
        t.name = cleaned
    t.save()
    return OrgPersonRelationshipTypeSchema(id=t.id, name=t.name)


@router.delete("/relationship-types/organizations/{type_id}/", response={204: None})
def delete_org_person_type(request, type_id: int):
    t = get_object_or_404(OrgPersonRelationshipType, pk=type_id)
    t.delete()
    return 204, None


# --- Org-Org Relationship Types ---


@router.get("/relationship-types/org-org/", response=list[OrgOrgRelationshipTypeSchema])
def list_org_org_types(request):
    types = OrgOrgRelationshipType.objects.order_by("name", "id")
    return [OrgOrgRelationshipTypeSchema(id=t.id, name=t.name) for t in types]


@router.post("/relationship-types/org-org/", response={201: OrgOrgRelationshipTypeSchema})
def create_org_org_type(request, payload: OrgOrgRelationshipTypeCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, "Name may not be blank.")
    t = OrgOrgRelationshipType.objects.create(name=name)
    return 201, OrgOrgRelationshipTypeSchema(id=t.id, name=t.name)


@router.put("/relationship-types/org-org/{type_id}/", response=OrgOrgRelationshipTypeSchema)
def update_org_org_type(request, type_id: int, payload: OrgOrgRelationshipTypeUpdateInput):
    t = get_object_or_404(OrgOrgRelationshipType, pk=type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, "Name may not be blank.")
        t.name = cleaned
    t.save()
    return OrgOrgRelationshipTypeSchema(id=t.id, name=t.name)


@router.delete("/relationship-types/org-org/{type_id}/", response={204: None})
def delete_org_org_type(request, type_id: int):
    t = get_object_or_404(OrgOrgRelationshipType, pk=type_id)
    t.delete()
    return 204, None
