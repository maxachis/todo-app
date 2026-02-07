from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from tasks.models import Tag, Task


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


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
        return render(request, "tasks/partials/task_detail.html", {"task": task})

    from django.shortcuts import redirect
    return redirect("task_detail", task_id=task.pk)


@require_http_methods(["DELETE", "POST"])
def remove_tag(request, task_id, tag_id):
    """Remove a tag from a task."""
    task = get_object_or_404(Task, pk=task_id)
    tag = get_object_or_404(Tag, pk=tag_id)
    task.tags.remove(tag)

    if _is_htmx(request):
        return render(request, "tasks/partials/task_detail.html", {"task": task})

    from django.shortcuts import redirect
    return redirect("task_detail", task_id=task.pk)
