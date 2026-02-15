from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from tasks.models import List, Project, Section
from tasks.views.lists import _get_lists_with_counts, _get_pinned_tasks
from tasks.views.reorder import reorder_siblings


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _oob_response(request, task_list):
    """Build OOB swap fragments for center panel + sidebar."""
    context = {
        "active_list": task_list,
        "sections": task_list.sections.all(),
        "lists": _get_lists_with_counts(),
        "projects": Project.objects.filter(is_active=True),
        "pinned_tasks": _get_pinned_tasks(task_list),
    }
    center_html = render_to_string(
        "tasks/partials/list_detail.html", context, request=request
    )
    sidebar_ctx = {"lists": context["lists"], "active_list": task_list}
    sidebar_html = render_to_string(
        "tasks/partials/sidebar_oob.html", sidebar_ctx, request=request
    )
    oob_center = (
        f'<div id="center-panel-oob" hx-swap-oob="innerHTML:#center-panel">'
        f"{center_html}</div>"
    )
    return HttpResponse(oob_center + sidebar_html)


@require_http_methods(["POST"])
def create_section(request, list_id):
    """Create a section within a list."""
    task_list = get_object_or_404(List, pk=list_id)
    name = request.POST.get("name", "").strip()
    emoji = request.POST.get("emoji", "").strip()

    if not name:
        return HttpResponse("Name is required", status=400)

    max_pos = task_list.sections.aggregate(m=models.Max("position"))["m"] or 0
    section = Section.objects.create(
        list=task_list, name=name, emoji=emoji, position=max_pos + 10
    )

    if _is_htmx(request):
        return _oob_response(request, task_list)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task_list.pk)


@require_http_methods(["POST"])
def update_section(request, section_id):
    """Update a section."""
    section = get_object_or_404(Section, pk=section_id)
    name = request.POST.get("name", "").strip()
    emoji = request.POST.get("emoji")

    if name:
        section.name = name
    if emoji is not None:
        section.emoji = emoji.strip()

    section.save()

    if _is_htmx(request):
        return _oob_response(request, section.list)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=section.list.pk)


@require_http_methods(["DELETE", "POST"])
def delete_section(request, section_id):
    """Delete a section."""
    section = get_object_or_404(Section, pk=section_id)
    task_list = section.list
    section.delete()

    if _is_htmx(request):
        return _oob_response(request, task_list)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task_list.pk)


@require_http_methods(["POST"])
def move_section(request, section_id):
    """Reorder a section within its list via drag-and-drop."""
    section = get_object_or_404(Section, pk=section_id)
    position = request.POST.get("position")

    if position is None:
        return HttpResponse("Position is required", status=400)

    new_index = int(position) // 10
    reorder_siblings(section, section.list.sections, new_index)

    return HttpResponse(status=204)
