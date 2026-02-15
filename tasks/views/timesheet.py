import datetime

from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from tasks.models import Project, Task, TimeEntry


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _week_bounds(date):
    """Return (monday, sunday) for the week containing `date`."""
    monday = date - datetime.timedelta(days=date.weekday())
    sunday = monday + datetime.timedelta(days=6)
    return monday, sunday


def _build_timesheet_context(request):
    """Build context dict for the timesheet view."""
    today = datetime.date.today()

    week_offset = int(request.GET.get("week", 0))
    ref_date = today + datetime.timedelta(weeks=week_offset)
    monday, sunday = _week_bounds(ref_date)

    entries = (
        TimeEntry.objects.filter(date__gte=monday, date__lte=sunday)
        .select_related("project")
        .prefetch_related("tasks")
    )

    total_hours = entries.count()

    project_hours = (
        entries.values("project__name", "project__id")
        .annotate(hours=models.Count("id"))
        .order_by("-hours")
    )

    entries_by_date = {}
    for entry in entries:
        entries_by_date.setdefault(entry.date, []).append(entry)
    entries_by_date = sorted(entries_by_date.items(), key=lambda x: x[0], reverse=True)

    active_projects = Project.objects.filter(is_active=True)

    return {
        "entries_by_date": entries_by_date,
        "total_hours": total_hours,
        "project_hours": project_hours,
        "monday": monday,
        "sunday": sunday,
        "week_offset": week_offset,
        "prev_week": week_offset - 1,
        "next_week": week_offset + 1,
        "today": today,
        "active_projects": active_projects,
    }


def timesheet_index(request):
    """Timesheet page with weekly view."""
    context = _build_timesheet_context(request)

    if _is_htmx(request):
        return render(request, "tasks/partials/timesheet_content.html", context)

    return render(request, "tasks/timesheet.html", context)


@require_http_methods(["POST"])
def create_time_entry(request):
    """Create a new time entry (1 entry = 1 hour)."""
    project_id = request.POST.get("project")
    if not project_id:
        return HttpResponse("Project is required", status=400)

    project = get_object_or_404(Project, pk=project_id)
    description = request.POST.get("description", "").strip()
    date_str = request.POST.get("date", "")
    task_ids = request.POST.getlist("tasks")

    try:
        date = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
    except ValueError:
        date = datetime.date.today()

    entry = TimeEntry.objects.create(
        project=project,
        description=description,
        date=date,
    )

    if task_ids:
        tasks = Task.objects.filter(pk__in=task_ids)
        entry.tasks.set(tasks)

    context = _build_timesheet_context(request)
    context["last_project_id"] = project.id
    return render(request, "tasks/partials/timesheet_content.html", context)


@require_http_methods(["POST", "DELETE"])
def delete_time_entry(request, entry_id):
    """Delete a time entry."""
    entry = get_object_or_404(TimeEntry, pk=entry_id)
    entry.delete()

    context = _build_timesheet_context(request)
    return render(request, "tasks/partials/timesheet_content.html", context)


def tasks_for_project(request, project_id):
    """Return task checkboxes for lists linked to a given project."""
    project = get_object_or_404(Project, pk=project_id)
    linked_lists = project.lists.all()
    tasks = Task.objects.filter(
        section__list__in=linked_lists, is_completed=False
    ).select_related("section", "section__list")

    return render(
        request,
        "tasks/partials/timesheet_task_selector.html",
        {"tasks": tasks, "project": project},
    )
