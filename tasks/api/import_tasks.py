from __future__ import annotations

import os

from django.db import transaction
from ninja import Router
from ninja.errors import HttpError

from tasks.services.ticktick_import import import_ticktick_csv

router = Router(tags=["import"])


@router.post("/import/")
def import_tasks(request):
    csv_file = request.FILES.get("file") or request.FILES.get("csv_file")
    if not csv_file:
        raise HttpError(400, "Please provide a CSV file upload.")

    ext = os.path.splitext(csv_file.name)[1].lower()
    if ext != ".csv":
        raise HttpError(400, "Only .csv files are supported.")

    with transaction.atomic():
        stats = import_ticktick_csv(csv_file)

    return stats
