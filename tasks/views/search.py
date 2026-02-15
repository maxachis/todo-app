from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from tasks.models import Task


def search_tasks(request):
    """Search tasks across all lists by title, notes, and tag names."""
    query = request.GET.get("q", "").strip()

    if not query:
        return HttpResponse("")

    search_filter = (
        Q(title__icontains=query)
        | Q(notes__icontains=query)
        | Q(tags__name__icontains=query)
    )
    tasks = (
        Task.objects.filter(search_filter)
        .select_related("section__list")
        .prefetch_related("tags")
        .distinct()
        .order_by("section__list__position", "section__position", "position")
    )

    # Group results by list for display
    grouped_results = {}
    for task in tasks:
        task_list = task.section.list
        if task_list.id not in grouped_results:
            grouped_results[task_list.id] = {
                "list": task_list,
                "tasks": [],
            }
        grouped_results[task_list.id]["tasks"].append(
            {
                "task": task,
                "section_name": task.section.name,
            }
        )

    context = {
        "query": query,
        "grouped_results": grouped_results.values(),
        "total_count": tasks.count(),
    }

    return render(request, "tasks/partials/search_results.html", context)
