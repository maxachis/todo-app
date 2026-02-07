from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from tasks.models import List, Section


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


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
        context = {
            "active_list": task_list,
            "sections": task_list.sections.all(),
            "lists": List.objects.all(),
        }
        return render(request, "tasks/partials/list_detail.html", context)

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
        context = {
            "active_list": section.list,
            "sections": section.list.sections.all(),
            "lists": List.objects.all(),
        }
        return render(request, "tasks/partials/list_detail.html", context)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=section.list.pk)


@require_http_methods(["DELETE", "POST"])
def delete_section(request, section_id):
    """Delete a section."""
    section = get_object_or_404(Section, pk=section_id)
    task_list = section.list
    section.delete()

    if _is_htmx(request):
        context = {
            "active_list": task_list,
            "sections": task_list.sections.all(),
            "lists": List.objects.all(),
        }
        return render(request, "tasks/partials/list_detail.html", context)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task_list.pk)
