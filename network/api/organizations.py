from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    OrganizationCreateInput,
    OrganizationSchema,
    OrganizationUpdateInput,
)
from network.models import Organization, OrgType

router = Router(tags=["network-organizations"])


def _serialize_organization(org: Organization) -> OrganizationSchema:
    return OrganizationSchema(
        id=org.id,
        name=org.name,
        org_type_id=org.org_type_id,
        notes=org.notes,
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


@router.get("/organizations/", response=list[OrganizationSchema])
def list_organizations(request):
    organizations = Organization.objects.order_by("name", "id")
    return [_serialize_organization(org) for org in organizations]


@router.post("/organizations/", response={201: OrganizationSchema})
def create_organization(request, payload: OrganizationCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})

    org_type = get_object_or_404(OrgType, pk=payload.org_type_id)
    organization = Organization.objects.create(
        name=name,
        org_type=org_type,
        notes=payload.notes,
    )
    return 201, _serialize_organization(organization)


@router.get("/organizations/{organization_id}/", response=OrganizationSchema)
def get_organization(request, organization_id: int):
    organization = get_object_or_404(Organization, pk=organization_id)
    return _serialize_organization(organization)


@router.put("/organizations/{organization_id}/", response=OrganizationSchema)
def update_organization(request, organization_id: int, payload: OrganizationUpdateInput):
    organization = get_object_or_404(Organization, pk=organization_id)

    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        organization.name = cleaned

    if payload.org_type_id is not None:
        organization.org_type = get_object_or_404(OrgType, pk=payload.org_type_id)

    if payload.notes is not None:
        organization.notes = payload.notes

    organization.save()
    return _serialize_organization(organization)


@router.delete("/organizations/{organization_id}/", response={204: None})
def delete_organization(request, organization_id: int):
    organization = get_object_or_404(Organization, pk=organization_id)
    organization.delete()
    return 204, None
