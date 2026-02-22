from __future__ import annotations

import os

from django.db import transaction
from ninja import Router
from ninja.errors import HttpError

from tasks.services.native_import import (
    detect_csv_format,
    import_native_csv,
    import_native_json,
)
from tasks.services.ticktick_import import import_ticktick_csv

router = Router(tags=["import"])


@router.post("/import/")
def import_tasks(request):
    uploaded = request.FILES.get("file") or request.FILES.get("csv_file")
    if not uploaded:
        raise HttpError(400, "Please provide a file upload.")

    ext = os.path.splitext(uploaded.name)[1].lower()

    if ext == ".json":
        stats = import_native_json(uploaded)
        return stats

    if ext == ".csv":
        content = uploaded.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8-sig")

        fmt = detect_csv_format(content)
        if fmt == "native":
            import io
            stats = import_native_csv(io.BytesIO(content.encode("utf-8")))
            return stats
        elif fmt == "ticktick":
            import io
            uploaded = io.BytesIO(content.encode("utf-8-sig"))
            uploaded.name = "reimport.csv"
            with transaction.atomic():
                stats = import_ticktick_csv(uploaded)
            return stats
        else:
            raise HttpError(
                400,
                "Unrecognized CSV format. Expected either the app's native export "
                "columns (list, section, task) or TickTick columns (taskId, Title).",
            )

    raise HttpError(400, "Unsupported file type. Please upload a .json or .csv file.")
