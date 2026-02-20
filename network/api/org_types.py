from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import OrgTypeCreateInput, OrgTypeSchema, OrgTypeUpdateInput
from network.models import OrgType

router = Router(tags=["network-org-types"])


def _serialize_org_type(org_type: OrgType) -> OrgTypeSchema:
    return OrgTypeSchema(id=org_type.id, name=org_type.name)


@router.get("/org-types/", response=list[OrgTypeSchema])
def list_org_types(request):
    org_types = OrgType.objects.order_by("name", "id")
    return [_serialize_org_type(org_type) for org_type in org_types]


@router.post("/org-types/", response={201: OrgTypeSchema})
def create_org_type(request, payload: OrgTypeCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, {"name": ["This field may not be blank."]})
    org_type = OrgType.objects.create(name=name)
    return 201, _serialize_org_type(org_type)


@router.put("/org-types/{org_type_id}/", response=OrgTypeSchema)
def update_org_type(request, org_type_id: int, payload: OrgTypeUpdateInput):
    org_type = get_object_or_404(OrgType, pk=org_type_id)
    if payload.name is not None:
        cleaned = payload.name.strip()
        if not cleaned:
            raise HttpError(422, {"name": ["This field may not be blank."]})
        org_type.name = cleaned
    org_type.save()
    return _serialize_org_type(org_type)


@router.delete("/org-types/{org_type_id}/", response={204: None})
def delete_org_type(request, org_type_id: int):
    org_type = get_object_or_404(OrgType, pk=org_type_id)
    org_type.delete()
    return 204, None
