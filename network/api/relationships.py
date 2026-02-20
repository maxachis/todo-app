from django.shortcuts import get_object_or_404
from ninja import Router

from network.api.schemas import (
    RelationshipOrganizationPersonCreateInput,
    RelationshipOrganizationPersonSchema,
    RelationshipOrganizationPersonUpdateInput,
    RelationshipPersonPersonCreateInput,
    RelationshipPersonPersonSchema,
    RelationshipPersonPersonUpdateInput,
)
from network.models import (
    Organization,
    Person,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
)

router = Router(tags=["network-relationships"])


def _serialize_person_relationship(rel: RelationshipPersonPerson) -> RelationshipPersonPersonSchema:
    return RelationshipPersonPersonSchema(
        id=rel.id,
        person_1_id=rel.person_1_id,
        person_2_id=rel.person_2_id,
        notes=rel.notes,
        created_at=rel.created_at,
        updated_at=rel.updated_at,
    )


def _serialize_org_relationship(rel: RelationshipOrganizationPerson) -> RelationshipOrganizationPersonSchema:
    return RelationshipOrganizationPersonSchema(
        id=rel.id,
        organization_id=rel.organization_id,
        person_id=rel.person_id,
        notes=rel.notes,
        created_at=rel.created_at,
        updated_at=rel.updated_at,
    )


@router.get("/relationships/people/", response=list[RelationshipPersonPersonSchema])
def list_person_relationships(request):
    relationships = RelationshipPersonPerson.objects.order_by("id")
    return [_serialize_person_relationship(rel) for rel in relationships]


@router.post("/relationships/people/", response={201: RelationshipPersonPersonSchema})
def create_person_relationship(request, payload: RelationshipPersonPersonCreateInput):
    person_1 = get_object_or_404(Person, pk=payload.person_1_id)
    person_2 = get_object_or_404(Person, pk=payload.person_2_id)
    relationship = RelationshipPersonPerson.objects.create(
        person_1=person_1,
        person_2=person_2,
        notes=payload.notes,
    )
    return 201, _serialize_person_relationship(relationship)


@router.put("/relationships/people/{relationship_id}/", response=RelationshipPersonPersonSchema)
def update_person_relationship(
    request, relationship_id: int, payload: RelationshipPersonPersonUpdateInput
):
    relationship = get_object_or_404(RelationshipPersonPerson, pk=relationship_id)
    if payload.notes is not None:
        relationship.notes = payload.notes
    relationship.save()
    return _serialize_person_relationship(relationship)


@router.delete("/relationships/people/{relationship_id}/", response={204: None})
def delete_person_relationship(request, relationship_id: int):
    relationship = get_object_or_404(RelationshipPersonPerson, pk=relationship_id)
    relationship.delete()
    return 204, None


@router.get("/relationships/organizations/", response=list[RelationshipOrganizationPersonSchema])
def list_org_relationships(request):
    relationships = RelationshipOrganizationPerson.objects.order_by("id")
    return [_serialize_org_relationship(rel) for rel in relationships]


@router.post("/relationships/organizations/", response={201: RelationshipOrganizationPersonSchema})
def create_org_relationship(request, payload: RelationshipOrganizationPersonCreateInput):
    organization = get_object_or_404(Organization, pk=payload.organization_id)
    person = get_object_or_404(Person, pk=payload.person_id)
    relationship = RelationshipOrganizationPerson.objects.create(
        organization=organization,
        person=person,
        notes=payload.notes,
    )
    return 201, _serialize_org_relationship(relationship)


@router.put("/relationships/organizations/{relationship_id}/", response=RelationshipOrganizationPersonSchema)
def update_org_relationship(
    request, relationship_id: int, payload: RelationshipOrganizationPersonUpdateInput
):
    relationship = get_object_or_404(RelationshipOrganizationPerson, pk=relationship_id)
    if payload.notes is not None:
        relationship.notes = payload.notes
    relationship.save()
    return _serialize_org_relationship(relationship)


@router.delete("/relationships/organizations/{relationship_id}/", response={204: None})
def delete_org_relationship(request, relationship_id: int):
    relationship = get_object_or_404(RelationshipOrganizationPerson, pk=relationship_id)
    relationship.delete()
    return 204, None
