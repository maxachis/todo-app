from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from tasks.models import Tag, Task


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _task_detail_context(task):
    """Build context for task detail rendering, including available tags."""
    available_tags = Tag.objects.exclude(pk__in=task.tags.all())
    return {"task": task, "available_tags": available_tags}


def _render_detail_with_oob_task(request, task):
    """Render the detail panel plus an OOB swap for the task row in center panel."""
    response = render(
        request, "tasks/partials/task_detail.html", _task_detail_context(task)
    )

    # Compute nesting depth
    depth = 0
    ancestor = task.parent
    while ancestor:
        depth += 1
        ancestor = ancestor.parent

    oob_html = render_to_string(
        "tasks/partials/task_item.html",
        {"task": task, "depth": depth},
        request=request,
    )
    response.write(
        f'<div hx-swap-oob="outerHTML:#task-{task.id}">{oob_html}</div>'
    )
    return response


@require_http_methods(["POST"])
def add_tag(request, task_id):
    """Add a tag to a task."""
    task = get_object_or_404(Task, pk=task_id)
    tag_name = request.POST.get("name", "").strip()

    if not tag_name:
        return HttpResponse("Tag name is required", status=400)

    tag, _ = Tag.objects.get_or_create(name=tag_name)
    task.tags.add(tag)

    if _is_htmx(request):
        return _render_detail_with_oob_task(request, task)

    from django.shortcuts import redirect
    return redirect("task_detail", task_id=task.pk)


@require_http_methods(["DELETE", "POST"])
def remove_tag(request, task_id, tag_id):
    """Remove a tag from a task."""
    task = get_object_or_404(Task, pk=task_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    task.tags.remove(tag)

    if _is_htmx(request):
        return _render_detail_with_oob_task(request, task)

    from django.shortcuts import redirect
    return redirect("task_detail", task_id=task.pk)
