from django.db import models
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from tasks.models import List, Project, Section, Task
from tasks.views.reorder import reorder_siblings


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _get_lists_with_counts():
    """Return all lists annotated with their incomplete task count."""
    return List.objects.annotate(
        incomplete_task_count=Count(
            "sections__tasks",
            filter=Q(sections__tasks__is_completed=False),
        )
    )


def _get_pinned_tasks(task_list):
    """Return pinned, non-completed tasks for a list."""
    return Task.objects.filter(
        section__list=task_list, is_pinned=True, is_completed=False
    )


def index(request):
    """Main page — renders base with sidebar + default list."""
    lists = _get_lists_with_counts()
    first_list = lists.first()
    context = {"lists": lists, "active_list": first_list}
    if first_list:
        context["sections"] = first_list.sections.all()
        context["projects"] = Project.objects.filter(is_active=True)
        context["pinned_tasks"] = _get_pinned_tasks(first_list)

    if _is_htmx(request):
        # If targeted at #page-body (navbar click), return the full 3-panel layout
        if request.headers.get("HX-Target") == "page-body":
            return render(request, "tasks/partials/todo_page_body.html", context)
        return render(request, "tasks/partials/full_content.html", context)

    return render(request, "tasks/index.html", context)


@require_http_methods(["POST"])
def create_list(request):
    """Create a new list."""
    name = request.POST.get("name", "").strip()
    emoji = request.POST.get("emoji", "").strip()
    if not name:
        return HttpResponse("Name is required", status=400)

    max_pos = List.objects.aggregate(m=models.Max("position"))["m"] or 0
    task_list = List.objects.create(name=name, emoji=emoji, position=max_pos + 10)

    if _is_htmx(request):
        from django.template.loader import render_to_string

        lists = _get_lists_with_counts()
        context = {
            "lists": lists,
            "active_list": task_list,
            "sections": task_list.sections.all(),
            "pinned_tasks": _get_pinned_tasks(task_list),
        }
        center_html = render_to_string(
            "tasks/partials/list_detail.html", context, request=request
        )
        sidebar_html = render_to_string(
            "tasks/partials/sidebar_oob.html", context, request=request
        )
        oob_center = (
            f'<div id="center-panel-oob" hx-swap-oob="innerHTML:#center-panel">'
            f"{center_html}</div>"
        )
        return HttpResponse(oob_center + sidebar_html)

    return redirect_to_list(task_list)


def list_detail(request, list_id):
    """GET list detail — returns sections + tasks."""
    task_list = get_object_or_404(List, pk=list_id)
    sections = task_list.sections.all()
    context = {
        "active_list": task_list,
        "sections": sections,
        "lists": _get_lists_with_counts(),
        "projects": Project.objects.filter(is_active=True),
        "pinned_tasks": _get_pinned_tasks(task_list),
    }

    if _is_htmx(request):
        from django.template.loader import render_to_string

        center_html = render_to_string(
            "tasks/partials/list_detail.html", context, request=request
        )
        sidebar_html = render_to_string(
            "tasks/partials/sidebar_oob.html", context, request=request
        )
        return HttpResponse(center_html + sidebar_html)

    return render(request, "tasks/index.html", context)


@require_http_methods(["POST"])
def update_list(request, list_id):
    """Update (rename) a list."""
    task_list = get_object_or_404(List, pk=list_id)
    name = request.POST.get("name", "").strip()
    emoji = request.POST.get("emoji")
    project_id = request.POST.get("project")

    if name:
        task_list.name = name
    if emoji is not None:
        task_list.emoji = emoji.strip()
    if project_id is not None:
        if project_id == "" or project_id == "0":
            task_list.project = None
        else:
            try:
                task_list.project = Project.objects.get(pk=int(project_id))
            except (Project.DoesNotExist, ValueError):
                pass

    task_list.save()

    if _is_htmx(request):
        from django.template.loader import render_to_string

        lists = _get_lists_with_counts()
        context = {
            "lists": lists,
            "active_list": task_list,
            "sections": task_list.sections.all(),
            "projects": Project.objects.filter(is_active=True),
            "pinned_tasks": _get_pinned_tasks(task_list),
        }
        center_html = render_to_string(
            "tasks/partials/list_detail.html", context, request=request
        )
        sidebar_html = render_to_string(
            "tasks/partials/sidebar_oob.html", context, request=request
        )
        oob_center = (
            f'<div id="center-panel-oob" hx-swap-oob="innerHTML:#center-panel">'
            f"{center_html}</div>"
        )
        return HttpResponse(oob_center + sidebar_html)

    return redirect_to_list(task_list)


@require_http_methods(["DELETE", "POST"])
def delete_list(request, list_id):
    """Delete a list."""
    task_list = get_object_or_404(List, pk=list_id)
    task_list.delete()

    if _is_htmx(request):
        from django.template.loader import render_to_string

        lists = _get_lists_with_counts()
        first_list = lists.first()
        context = {"lists": lists, "active_list": first_list}
        if first_list:
            context["sections"] = first_list.sections.all()
            context["projects"] = Project.objects.filter(is_active=True)
            context["pinned_tasks"] = _get_pinned_tasks(first_list)
        center_html = render_to_string(
            "tasks/partials/list_detail.html", context, request=request
        )
        sidebar_html = render_to_string(
            "tasks/partials/sidebar_oob.html", context, request=request
        )
        oob_center = (
            f'<div id="center-panel-oob" hx-swap-oob="innerHTML:#center-panel">'
            f"{center_html}</div>"
        )
        return HttpResponse(oob_center + sidebar_html)

    from django.shortcuts import redirect
    return redirect("index")


@require_http_methods(["POST"])
def move_list(request, list_id):
    """Reorder a list in the sidebar via drag-and-drop."""
    task_list = get_object_or_404(List, pk=list_id)
    position = request.POST.get("position")

    if position is None:
        return HttpResponse("Position is required", status=400)

    new_index = int(position) // 10
    reorder_siblings(task_list, List.objects.all(), new_index)

    return HttpResponse(status=204)


def redirect_to_list(task_list):
    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task_list.pk)
