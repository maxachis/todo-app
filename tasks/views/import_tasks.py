import os

from django.db import transaction
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from tasks.services.ticktick_import import import_ticktick_csv


@require_http_methods(["GET", "POST"])
def import_page(request):
    """Upload form (GET) or process a TickTick CSV import (POST)."""
    if request.method == "GET":
        return render(request, "tasks/import.html")

    csv_file = request.FILES.get("csv_file")
    if not csv_file:
        return render(
            request, "tasks/import.html", {"error": "Please select a CSV file."}
        )

    ext = os.path.splitext(csv_file.name)[1].lower()
    if ext != ".csv":
        return render(
            request,
            "tasks/import.html",
            {"error": "Only .csv files are supported."},
        )

    with transaction.atomic():
        stats = import_ticktick_csv(csv_file)

    return render(request, "tasks/import.html", {"stats": stats})
