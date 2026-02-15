from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from tasks.models import Project


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def projects_index(request):
    """Projects listing page."""
    projects = Project.objects.annotate(
        total_hours=models.Count("time_entries", distinct=True),
        list_count=models.Count("lists", distinct=True),
        total_tasks=models.Count("lists__sections__tasks", distinct=True),
        completed_tasks=models.Count(
            "lists__sections__tasks",
            filter=Q(lists__sections__tasks__is_completed=True),
            distinct=True,
        ),
    )
    context = {"projects": projects}

    if _is_htmx(request):
        return render(request, "tasks/partials/projects_content.html", context)

    return render(request, "tasks/projects.html", context)


@require_http_methods(["POST"])
def create_project(request):
    """Create a new project."""
    name = request.POST.get("name", "").strip()
    if not name:
        return HttpResponse("Name is required", status=400)

    description = request.POST.get("description", "").strip()
    max_pos = Project.objects.aggregate(m=models.Max("position"))["m"] or 0
    Project.objects.create(name=name, description=description, position=max_pos + 10)

    return _render_projects_content(request)


@require_http_methods(["POST"])
def update_project(request, project_id):
    """Update a project's name and description."""
    project = get_object_or_404(Project, pk=project_id)
    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()

    if name:
        project.name = name
    project.description = description
    project.save()

    return _render_projects_content(request)


@require_http_methods(["POST", "DELETE"])
def delete_project(request, project_id):
    """Delete a project."""
    project = get_object_or_404(Project, pk=project_id)
    project.delete()

    return _render_projects_content(request)


@require_http_methods(["POST"])
def toggle_project_active(request, project_id):
    """Toggle a project's active status."""
    project = get_object_or_404(Project, pk=project_id)
    project.is_active = not project.is_active
    project.save()

    return _render_projects_content(request)


def _render_projects_content(request):
    """Helper to re-render the projects content partial."""
    projects = Project.objects.annotate(
        total_hours=models.Count("time_entries", distinct=True),
        list_count=models.Count("lists", distinct=True),
        total_tasks=models.Count("lists__sections__tasks", distinct=True),
        completed_tasks=models.Count(
            "lists__sections__tasks",
            filter=Q(lists__sections__tasks__is_completed=True),
            distinct=True,
        ),
    )
    return render(
        request, "tasks/partials/projects_content.html", {"projects": projects}
    )
