from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from tasks.models import List, Section, Task


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def index(request):
    """Main page — renders base with sidebar + default list."""
    lists = List.objects.all()
    first_list = lists.first()
    context = {"lists": lists, "active_list": first_list}
    if first_list:
        context["sections"] = first_list.sections.all()
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
        lists = List.objects.all()
        return render(request, "tasks/partials/sidebar_lists.html", {"lists": lists, "active_list": task_list})

    return redirect_to_list(task_list)


def list_detail(request, list_id):
    """GET list detail — returns sections + tasks."""
    task_list = get_object_or_404(List, pk=list_id)
    sections = task_list.sections.all()
    context = {
        "active_list": task_list,
        "sections": sections,
        "lists": List.objects.all(),
    }

    if _is_htmx(request):
        return render(request, "tasks/partials/list_detail.html", context)

    return render(request, "tasks/index.html", context)


@require_http_methods(["POST"])
def update_list(request, list_id):
    """Update (rename) a list."""
    task_list = get_object_or_404(List, pk=list_id)
    name = request.POST.get("name", "").strip()
    emoji = request.POST.get("emoji")

    if name:
        task_list.name = name
    if emoji is not None:
        task_list.emoji = emoji.strip()

    task_list.save()

    if _is_htmx(request):
        lists = List.objects.all()
        return render(request, "tasks/partials/sidebar_lists.html", {"lists": lists, "active_list": task_list})

    return redirect_to_list(task_list)


@require_http_methods(["DELETE", "POST"])
def delete_list(request, list_id):
    """Delete a list."""
    task_list = get_object_or_404(List, pk=list_id)
    task_list.delete()

    if _is_htmx(request):
        lists = List.objects.all()
        first_list = lists.first()
        context = {"lists": lists, "active_list": first_list}
        if first_list:
            context["sections"] = first_list.sections.all()
        return render(request, "tasks/partials/full_content.html", context)

    from django.shortcuts import redirect
    return redirect("index")


def redirect_to_list(task_list):
    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task_list.pk)


# Need the import for Max
from django.db import models
