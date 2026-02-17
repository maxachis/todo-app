from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError

from tasks.api.schemas import ProjectCreateInput, ProjectSchema, ProjectUpdateInput, TaskSchema
from tasks.api.tasks import _serialize_task
from tasks.models import Project, Task

router = Router(tags=["projects"])


def _project_queryset():
    return Project.objects.annotate(
        total_hours=models.Count("time_entries", distinct=True),
        linked_lists_count=models.Count("lists", distinct=True),
        total_tasks=models.Count("lists__sections__tasks", distinct=True),
        completed_tasks=models.Count(
            "lists__sections__tasks",
            filter=Q(lists__sections__tasks__is_completed=True),
            distinct=True,
        ),
    ).order_by("position")


def _serialize_project(project: Project) -> ProjectSchema:
    return ProjectSchema(
        id=project.id,
        name=project.name,
        description=project.description,
        is_active=project.is_active,
        position=project.position,
        total_hours=float(getattr(project, "total_hours", 0)),
        linked_lists_count=getattr(project, "linked_lists_count", 0),
        total_tasks=getattr(project, "total_tasks", 0),
        completed_tasks=getattr(project, "completed_tasks", 0),
    )


@router.get("/projects/", response=list[ProjectSchema])
def get_projects(request):
    return [_serialize_project(project) for project in _project_queryset()]


@router.post("/projects/", response={201: ProjectSchema})
def create_project(request, payload: ProjectCreateInput):
    name = payload.name.strip()
    if not name:
        raise HttpError(422, "Project name may not be blank.")

    max_position = Project.objects.aggregate(max_position=models.Max("position"))["max_position"] or 0
    project = Project.objects.create(
        name=name,
        description=payload.description.strip(),
        position=max_position + 10,
    )
    project = _project_queryset().get(pk=project.id)
    return 201, _serialize_project(project)


@router.put("/projects/{project_id}/", response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectUpdateInput):
    project = get_object_or_404(Project, pk=project_id)

    if payload.name is not None:
        cleaned_name = payload.name.strip()
        if not cleaned_name:
            raise HttpError(422, "Project name may not be blank.")
        project.name = cleaned_name
    if payload.description is not None:
        project.description = payload.description
    if payload.is_active is not None:
        project.is_active = payload.is_active

    project.save()
    project = _project_queryset().get(pk=project.id)
    return _serialize_project(project)


@router.delete("/projects/{project_id}/", response={204: None})
def delete_project(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return 204, None


@router.post("/projects/{project_id}/toggle/", response=ProjectSchema)
def toggle_project(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    project.is_active = not project.is_active
    project.save(update_fields=["is_active"])
    project = _project_queryset().get(pk=project.id)
    return _serialize_project(project)


@router.get("/projects/{project_id}/tasks/", response=list[TaskSchema])
def get_project_tasks(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    tasks = (
        Task.objects.filter(section__list__project=project, is_completed=False)
        .select_related("section")
        .prefetch_related("tags", "subtasks")
        .order_by("section__position", "position")
    )
    return [_serialize_task(task) for task in tasks]
