from __future__ import annotations

from django.http import Http404, HttpResponseBadRequest
from ninja import Router

from tasks.models import List
from tasks.views.export import _export_response

router = Router(tags=["export"])


def _normalize_format(fmt: str) -> str:
    normalized = fmt.lower()
    if normalized == "markdown":
        return "md"
    return normalized


@router.get("/export/{fmt}/")
def export_all(request, fmt: str):
    export_format = _normalize_format(fmt)
    if export_format not in {"json", "csv", "md"}:
        return HttpResponseBadRequest("Unsupported export format")

    lists = List.objects.order_by("position")
    return _export_response("all-lists", export_format, lists)


@router.get("/export/{list_id}/{fmt}/")
def export_single_list(request, list_id: int, fmt: str):
    export_format = _normalize_format(fmt)
    if export_format not in {"json", "csv", "md"}:
        return HttpResponseBadRequest("Unsupported export format")

    try:
        task_list = List.objects.get(pk=list_id)
    except List.DoesNotExist as exc:
        raise Http404("List not found") from exc

    return _export_response(task_list.name, export_format, [task_list])
