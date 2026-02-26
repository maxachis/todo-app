from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from network.api.schemas import (
    LeadCreateInput,
    LeadSchema,
    LeadTaskLinkSchema,
    LeadUpdateInput,
    LinkByIdInput,
)
from network.models import Lead, LeadTask, Organization, Person
from tasks.models import Task

router = Router(tags=["network-leads"])

VALID_STATUSES = {c[0] for c in Lead.STATUS_CHOICES}


def _annotate_leads(qs):
    return qs.annotate(
        person_name=Concat(
            F("person__first_name"), Value(" "), F("person__last_name")
        ),
        organization_name=F("organization__name"),
    )


def _serialize_lead(lead: Lead) -> LeadSchema:
    return LeadSchema(
        id=lead.id,
        title=lead.title,
        status=lead.status,
        notes=lead.notes,
        person_id=lead.person_id,
        organization_id=lead.organization_id,
        person_name=getattr(lead, "person_name", None),
        organization_name=getattr(lead, "organization_name", None),
        created_at=lead.created_at,
        updated_at=lead.updated_at,
    )


def _serialize_lead_task(link: LeadTask) -> LeadTaskLinkSchema:
    return LeadTaskLinkSchema(
        id=link.id,
        lead_id=link.lead_id,
        task_id=link.task_id,
        created_at=link.created_at,
    )


@router.get("/leads/", response=list[LeadSchema])
def list_leads(request):
    leads = _annotate_leads(Lead.objects.order_by("-updated_at"))
    return [_serialize_lead(lead) for lead in leads]


@router.post("/leads/", response={201: LeadSchema})
def create_lead(request, payload: LeadCreateInput):
    title = payload.title.strip()
    if not title:
        raise HttpError(422, "Title may not be blank.")
    if payload.status not in VALID_STATUSES:
        raise HttpError(422, f"Invalid status: {payload.status}")
    if payload.person_id is None and payload.organization_id is None:
        raise HttpError(422, "A lead must have a person or organization.")

    person = None
    if payload.person_id is not None:
        person = get_object_or_404(Person, pk=payload.person_id)
    organization = None
    if payload.organization_id is not None:
        organization = get_object_or_404(Organization, pk=payload.organization_id)

    lead = Lead.objects.create(
        title=title,
        status=payload.status,
        notes=payload.notes,
        person=person,
        organization=organization,
    )
    lead = _annotate_leads(Lead.objects.filter(pk=lead.pk)).get()
    return 201, _serialize_lead(lead)


@router.get("/leads/{lead_id}/", response=LeadSchema)
def get_lead(request, lead_id: int):
    lead = _annotate_leads(Lead.objects.all()).get(pk=lead_id)
    return _serialize_lead(lead)


@router.put("/leads/{lead_id}/", response=LeadSchema)
def update_lead(request, lead_id: int, payload: LeadUpdateInput):
    lead = get_object_or_404(Lead, pk=lead_id)

    if payload.title is not None:
        cleaned = payload.title.strip()
        if not cleaned:
            raise HttpError(422, "Title may not be blank.")
        lead.title = cleaned

    if payload.status is not None:
        if payload.status not in VALID_STATUSES:
            raise HttpError(422, f"Invalid status: {payload.status}")
        lead.status = payload.status

    if payload.notes is not None:
        lead.notes = payload.notes

    if payload.person_id is not None:
        lead.person = get_object_or_404(Person, pk=payload.person_id)

    if payload.organization_id is not None:
        lead.organization = get_object_or_404(Organization, pk=payload.organization_id)

    lead.save()
    lead = _annotate_leads(Lead.objects.filter(pk=lead.pk)).get()
    return _serialize_lead(lead)


@router.delete("/leads/{lead_id}/", response={204: None})
def delete_lead(request, lead_id: int):
    lead = get_object_or_404(Lead, pk=lead_id)
    lead.delete()
    return 204, None


# Lead-task link endpoints


@router.get("/leads/{lead_id}/tasks/", response=list[LeadTaskLinkSchema])
def list_lead_tasks(request, lead_id: int):
    Lead.objects.only("id").get(pk=lead_id)
    links = LeadTask.objects.filter(lead_id=lead_id).order_by("id")
    return [_serialize_lead_task(link) for link in links]


@router.post(
    "/leads/{lead_id}/tasks/",
    response={200: LeadTaskLinkSchema, 201: LeadTaskLinkSchema},
)
def link_lead_task(request, lead_id: int, payload: LinkByIdInput):
    lead = get_object_or_404(Lead, pk=lead_id)
    task = get_object_or_404(Task, pk=payload.id)
    link, created = LeadTask.objects.get_or_create(lead=lead, task=task)
    return (201 if created else 200), _serialize_lead_task(link)


@router.delete("/leads/{lead_id}/tasks/{task_id}/", response={204: None})
def unlink_lead_task(request, lead_id: int, task_id: int):
    link = get_object_or_404(LeadTask, lead_id=lead_id, task_id=task_id)
    link.delete()
    return 204, None
