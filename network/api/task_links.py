from django.shortcuts import get_object_or_404
from ninja import Router

from network.api.schemas import (
    InteractionTaskLinkSchema,
    LinkByIdInput,
    TaskOrganizationLinkSchema,
    TaskPersonLinkSchema,
)
from network.models import Interaction, InteractionTask, Organization, Person, TaskOrganization, TaskPerson
from tasks.models import Task

router = Router(tags=["network-task-links"])


def _serialize_task_person(link: TaskPerson) -> TaskPersonLinkSchema:
    return TaskPersonLinkSchema(
        id=link.id,
        task_id=link.task_id,
        person_id=link.person_id,
        created_at=link.created_at,
    )


def _serialize_task_organization(link: TaskOrganization) -> TaskOrganizationLinkSchema:
    return TaskOrganizationLinkSchema(
        id=link.id,
        task_id=link.task_id,
        organization_id=link.organization_id,
        created_at=link.created_at,
    )


def _serialize_interaction_task(link: InteractionTask) -> InteractionTaskLinkSchema:
    return InteractionTaskLinkSchema(
        id=link.id,
        interaction_id=link.interaction_id,
        task_id=link.task_id,
        created_at=link.created_at,
    )


@router.get("/people/{person_id}/tasks/", response=list[TaskPersonLinkSchema])
def list_person_tasks(request, person_id: int):
    Person.objects.only("id").get(pk=person_id)
    links = TaskPerson.objects.filter(person_id=person_id).order_by("id")
    return [_serialize_task_person(link) for link in links]


@router.get("/organizations/{organization_id}/tasks/", response=list[TaskOrganizationLinkSchema])
def list_organization_tasks(request, organization_id: int):
    Organization.objects.only("id").get(pk=organization_id)
    links = TaskOrganization.objects.filter(organization_id=organization_id).order_by("id")
    return [_serialize_task_organization(link) for link in links]


@router.get("/tasks/{task_id}/people/", response=list[TaskPersonLinkSchema])
def list_task_people(request, task_id: int):
    Task.objects.only("id").get(pk=task_id)
    links = TaskPerson.objects.filter(task_id=task_id).order_by("id")
    return [_serialize_task_person(link) for link in links]


@router.post("/tasks/{task_id}/people/", response={200: TaskPersonLinkSchema, 201: TaskPersonLinkSchema})
def link_task_person(request, task_id: int, payload: LinkByIdInput):
    task = get_object_or_404(Task, pk=task_id)
    person = get_object_or_404(Person, pk=payload.id)
    link, created = TaskPerson.objects.get_or_create(task=task, person=person)
    return (201 if created else 200), _serialize_task_person(link)


@router.delete("/tasks/{task_id}/people/{person_id}/", response={204: None})
def unlink_task_person(request, task_id: int, person_id: int):
    link = get_object_or_404(TaskPerson, task_id=task_id, person_id=person_id)
    link.delete()
    return 204, None


@router.get("/tasks/{task_id}/organizations/", response=list[TaskOrganizationLinkSchema])
def list_task_organizations(request, task_id: int):
    Task.objects.only("id").get(pk=task_id)
    links = TaskOrganization.objects.filter(task_id=task_id).order_by("id")
    return [_serialize_task_organization(link) for link in links]


@router.post("/tasks/{task_id}/organizations/", response={200: TaskOrganizationLinkSchema, 201: TaskOrganizationLinkSchema})
def link_task_organization(request, task_id: int, payload: LinkByIdInput):
    task = get_object_or_404(Task, pk=task_id)
    organization = get_object_or_404(Organization, pk=payload.id)
    link, created = TaskOrganization.objects.get_or_create(task=task, organization=organization)
    return (201 if created else 200), _serialize_task_organization(link)


@router.delete("/tasks/{task_id}/organizations/{organization_id}/", response={204: None})
def unlink_task_organization(request, task_id: int, organization_id: int):
    link = get_object_or_404(TaskOrganization, task_id=task_id, organization_id=organization_id)
    link.delete()
    return 204, None


@router.get("/interactions/{interaction_id}/tasks/", response=list[InteractionTaskLinkSchema])
def list_interaction_tasks(request, interaction_id: int):
    Interaction.objects.only("id").get(pk=interaction_id)
    links = InteractionTask.objects.filter(interaction_id=interaction_id).order_by("id")
    return [_serialize_interaction_task(link) for link in links]


@router.post("/interactions/{interaction_id}/tasks/", response={200: InteractionTaskLinkSchema, 201: InteractionTaskLinkSchema})
def link_interaction_task(request, interaction_id: int, payload: LinkByIdInput):
    interaction = get_object_or_404(Interaction, pk=interaction_id)
    task = get_object_or_404(Task, pk=payload.id)
    link, created = InteractionTask.objects.get_or_create(interaction=interaction, task=task)
    return (201 if created else 200), _serialize_interaction_task(link)


@router.delete("/interactions/{interaction_id}/tasks/{task_id}/", response={204: None})
def unlink_interaction_task(request, interaction_id: int, task_id: int):
    link = get_object_or_404(InteractionTask, interaction_id=interaction_id, task_id=task_id)
    link.delete()
    return 204, None
