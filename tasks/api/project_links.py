from __future__ import annotations

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from tasks.api.schemas import ProjectLinkCreateInput, ProjectLinkSchema, ProjectLinkUpdateInput
from tasks.models import Project, ProjectLink

router = Router(tags=["project-links"])


def _serialize_link(link: ProjectLink) -> ProjectLinkSchema:
    return ProjectLinkSchema(
        id=link.id,
        project_id=link.project_id,
        url=link.url,
        descriptor=link.descriptor,
        created_at=link.created_at,
    )


@router.get("/projects/{project_id}/links/", response=list[ProjectLinkSchema])
def list_project_links(request, project_id: int):
    get_object_or_404(Project, pk=project_id)
    return [_serialize_link(link) for link in ProjectLink.objects.filter(project_id=project_id)]


@router.post("/projects/{project_id}/links/", response={201: ProjectLinkSchema})
def create_project_link(request, project_id: int, payload: ProjectLinkCreateInput):
    project = get_object_or_404(Project, pk=project_id)

    url = payload.url.strip()
    descriptor = payload.descriptor.strip()

    if not url:
        raise HttpError(422, "URL may not be blank.")
    if not descriptor:
        raise HttpError(422, "Descriptor may not be blank.")

    link = ProjectLink.objects.create(project=project, url=url, descriptor=descriptor)
    return 201, _serialize_link(link)


@router.put("/projects/{project_id}/links/{link_id}/", response=ProjectLinkSchema)
def update_project_link(request, project_id: int, link_id: int, payload: ProjectLinkUpdateInput):
    link = get_object_or_404(ProjectLink, pk=link_id, project_id=project_id)

    if payload.url is not None:
        url = payload.url.strip()
        if not url:
            raise HttpError(422, "URL may not be blank.")
        link.url = url

    if payload.descriptor is not None:
        descriptor = payload.descriptor.strip()
        if not descriptor:
            raise HttpError(422, "Descriptor may not be blank.")
        link.descriptor = descriptor

    link.save()
    return _serialize_link(link)


@router.delete("/projects/{project_id}/links/{link_id}/", response={204: None})
def delete_project_link(request, project_id: int, link_id: int):
    link = get_object_or_404(ProjectLink, pk=link_id, project_id=project_id)
    link.delete()
    return 204, None
