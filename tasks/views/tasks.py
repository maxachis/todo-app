import json

from django.db import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from tasks.models import List, Project, Section, Tag, Task
from tasks.views.lists import _get_lists_with_counts, _get_pinned_tasks


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


MAX_PINNED_PER_LIST = 3


def _render_list_context(task_list):
    """Build standard context for list rendering."""
    return {
        "active_list": task_list,
        "sections": task_list.sections.all(),
        "lists": _get_lists_with_counts(),
        "pinned_tasks": _get_pinned_tasks(task_list),
    }


def _sidebar_oob_html(request, active_list):
    """Render the sidebar as an OOB swap fragment."""
    ctx = {"lists": _get_lists_with_counts(), "active_list": active_list}
    return render_to_string(
        "tasks/partials/sidebar_oob.html", ctx, request=request
    )


@require_http_methods(["POST"])
def create_task(request, section_id):
    """Create a task in a section, optionally with a parent."""
    section = get_object_or_404(Section, pk=section_id)
    title = request.POST.get("title", "").strip()
    parent_id = request.POST.get("parent")

    if not title:
        return HttpResponse("Title is required", status=400)

    parent = None
    if parent_id:
        parent = get_object_or_404(Task, pk=parent_id)

    # Get max position among siblings
    siblings = Task.objects.filter(section=section, parent=parent)
    max_pos = siblings.aggregate(m=models.Max("position"))["m"] or 0

    task = Task.objects.create(
        section=section,
        parent=parent,
        title=title,
        position=max_pos + 10,
    )

    if _is_htmx(request):
        task_html = render_to_string(
            "tasks/partials/task_item.html",
            {"task": task, "depth": 0},
            request=request,
        )
        sidebar_html = _sidebar_oob_html(request, section.list)
        return HttpResponse(task_html + sidebar_html)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=section.list.pk)


def task_detail(request, task_id):
    """GET task detail — right sidebar content."""
    task = get_object_or_404(Task, pk=task_id)
    available_tags = Tag.objects.exclude(pk__in=task.tags.all())

    if _is_htmx(request):
        return render(
            request,
            "tasks/partials/task_detail.html",
            {"task": task, "available_tags": available_tags},
        )

    context = _render_list_context(task.section.list)
    context["selected_task"] = task
    context["available_tags"] = available_tags
    return render(request, "tasks/index.html", context)


@require_http_methods(["POST"])
def update_task(request, task_id):
    """Update task fields (title, notes, due_date)."""
    task = get_object_or_404(Task, pk=task_id)

    title = request.POST.get("title")
    notes = request.POST.get("notes")
    due_date = request.POST.get("due_date")

    if title is not None:
        title = title.strip()
        if title:
            task.title = title

    if notes is not None:
        task.notes = notes

    if due_date is not None:
        if due_date.strip() == "":
            task.due_date = None
        else:
            task.due_date = due_date

    task.save()
    task.refresh_from_db()

    if _is_htmx(request):
        from tasks.templatetags.markdown_extras import render_markdown

        # OOB swap: update heading in detail panel
        oob_title = (
            f'<h2 id="detail-title" hx-swap-oob="true">'
            f"{task.title}</h2>"
        )

        # OOB swap: update rendered notes preview
        notes_html = ""
        if task.notes:
            notes_html = f"<h3>Preview</h3>{render_markdown(task.notes)}"
        oob_notes = (
            f'<div id="rendered-notes" class="rendered-notes" hx-swap-oob="true">'
            f"{notes_html}</div>"
        )

        # OOB swap: update task row in center panel
        depth = 0
        ancestor = task.parent
        while ancestor:
            depth += 1
            ancestor = ancestor.parent
        task_html = render_to_string(
            "tasks/partials/task_item.html",
            {"task": task, "depth": depth},
            request=request,
        )
        oob_task = (
            f'<div hx-swap-oob="outerHTML:#task-{task.id}">'
            f"{task_html}</div>"
        )
        return HttpResponse(oob_title + oob_notes + oob_task)

    from django.shortcuts import redirect
    return redirect("task_detail", task_id=task.pk)


@require_http_methods(["DELETE", "POST"])
def delete_task(request, task_id):
    """Delete a task and its subtasks."""
    task = get_object_or_404(Task, pk=task_id)
    task_list = task.section.list
    task.delete()

    if _is_htmx(request):
        context = _render_list_context(task_list)
        center_html = render_to_string(
            "tasks/partials/list_detail.html", context, request=request
        )
        sidebar_html = _sidebar_oob_html(request, task_list)
        oob_center = (
            f'<div id="center-panel-oob" hx-swap-oob="innerHTML:#center-panel">'
            f"{center_html}</div>"
        )
        return HttpResponse(oob_center + sidebar_html)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task_list.pk)


@require_http_methods(["POST"])
def complete_task(request, task_id):
    """Mark a task as completed.

    Uses hx-swap="none" on the client. Instead of replacing the whole
    section via OOB swap (which causes flicker), the server returns only
    the toast and sidebar OOB fragments. The client handles DOM changes
    (moving the task to the completed group, updating checkbox state)
    via a custom HX-Trigger event, allowing CSS transitions to finish
    before any DOM mutation.
    """
    task = get_object_or_404(Task, pk=task_id)
    section = task.section
    task.complete()

    if _is_htmx(request):
        sidebar_html = _sidebar_oob_html(request, section.list)
        toast_html = render_to_string(
            "tasks/partials/toast.html",
            {"task": task},
            request=request,
        )
        oob_toast = (
            '<div id="toast-container" hx-swap-oob="innerHTML:#toast-container">'
            f"{toast_html}</div>"
        )
        response = HttpResponse(sidebar_html + oob_toast)
        response["HX-Trigger"] = json.dumps(
            {"taskCompleted": {"taskId": task.pk, "parentId": task.parent_id}}
        )
        return response

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=section.list.pk)


@require_http_methods(["POST"])
def uncomplete_task(request, task_id):
    """Mark a task as not completed.

    Uses hx-swap="none" on the client. The server returns only
    sidebar and toast-clear OOB fragments. The client handles DOM
    changes (moving the task back to the active list, updating
    checkbox state) via a custom HX-Trigger event.
    """
    task = get_object_or_404(Task, pk=task_id)
    section = task.section
    task.uncomplete()

    if _is_htmx(request):
        sidebar_html = _sidebar_oob_html(request, section.list)
        toast_clear = (
            '<div id="toast-container" hx-swap-oob="innerHTML:#toast-container"></div>'
        )
        response = HttpResponse(sidebar_html + toast_clear)
        response["HX-Trigger"] = json.dumps(
            {"taskUncompleted": {"taskId": task.pk, "parentId": task.parent_id}}
        )
        return response

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=section.list.pk)


@require_http_methods(["POST"])
def move_task(request, task_id):
    """Move a task: change section, parent, position, or list."""
    task = get_object_or_404(Task, pk=task_id)
    old_list = task.section.list

    section_id = request.POST.get("section")
    parent_id = request.POST.get("parent")
    position = request.POST.get("position")
    list_id = request.POST.get("list")

    # Move to different list
    if list_id:
        target_list = get_object_or_404(List, pk=list_id)
        first_section = target_list.sections.first()
        if not first_section:
            return HttpResponse(
                "Target list has no sections", status=400
            )
        task.section = first_section
        task.parent = None
        # Update all subtasks' section FK recursively
        _update_subtask_sections(task, first_section)
    elif section_id:
        new_section = get_object_or_404(Section, pk=section_id)
        task.section = new_section
        _update_subtask_sections(task, new_section)

    # Set parent
    if parent_id is not None:
        if parent_id == "" or parent_id == "null":
            task.parent = None
        else:
            new_parent = get_object_or_404(Task, pk=parent_id)
            # Circular reference check: walk up from new_parent
            ancestor = new_parent
            while ancestor is not None:
                if ancestor.pk == task.pk:
                    return HttpResponse(
                        "Cannot nest a task under its own descendant",
                        status=400,
                    )
                ancestor = ancestor.parent
            task.parent = new_parent

    # Set position
    if position is not None:
        task.position = int(position)

    task.save()

    if _is_htmx(request):
        context = _render_list_context(task.section.list)
        center_html = render_to_string(
            "tasks/partials/list_detail.html", context, request=request
        )
        sidebar_html = _sidebar_oob_html(request, task.section.list)
        oob_center = (
            f'<div id="center-panel-oob" hx-swap-oob="innerHTML:#center-panel">'
            f"{center_html}</div>"
        )
        return HttpResponse(oob_center + sidebar_html)

    from django.shortcuts import redirect
    return redirect("list_detail", list_id=task.section.list.pk)


def _update_subtask_sections(task, section):
    """Recursively update section FK for all subtasks."""
    for sub in task.subtasks.all():
        sub.section = section
        sub.save()
        _update_subtask_sections(sub, section)


@require_http_methods(["POST"])
def pin_task(request, task_id):
    """Toggle pin status on a task.

    If pinning, enforce a per-list limit of MAX_PINNED_PER_LIST.
    Returns OOB swap to refresh the center panel so the pinned
    section updates accordingly.
    """
    task = get_object_or_404(Task, pk=task_id)
    task_list = task.section.list

    if task.is_pinned:
        task.is_pinned = False
        task.save()
    else:
        pinned_count = Task.objects.filter(
            section__list=task_list, is_pinned=True, is_completed=False
        ).count()
        if pinned_count >= MAX_PINNED_PER_LIST:
            message = (
                f"You can only pin {MAX_PINNED_PER_LIST} tasks per list. "
                "Unpin one to pin another."
            )
            if _is_htmx(request):
                toast_html = render_to_string(
                    "tasks/partials/toast_message.html",
                    {"message": message},
                    request=request,
                )
                oob_toast = (
                    '<div id="toast-container" hx-swap-oob="innerHTML:#toast-container">'
                    f"{toast_html}</div>"
                )
                return HttpResponse(oob_toast)
            return HttpResponse(message, status=400)
        task.is_pinned = True
        task.save()

    if _is_htmx(request):
        pinned_tasks = Task.objects.filter(
            section__list=task_list, is_pinned=True, is_completed=False
        )
        pinned_html = "".join(
            render_to_string(
                "tasks/partials/pinned_task_item.html",
                {"task": t, "show_parent_context": True},
                request=request,
            )
            for t in pinned_tasks
        )
        if not pinned_tasks:
            pinned_html = '<p class="pinned-empty">Pin up to 3 tasks for quick access.</p>'
        oob_pinned = (
            f'<div id="pinned-items" hx-swap-oob="innerHTML:#pinned-items">'
            f"{pinned_html}</div>"
        )
        trigger = json.dumps(
            {"pinToggled": {"taskId": task_id, "pinned": task.is_pinned}}
        )
        resp = HttpResponse(oob_pinned)
        resp["HX-Trigger"] = trigger
        return resp

    from django.shortcuts import redirect

    return redirect("list_detail", list_id=task_list.pk)
