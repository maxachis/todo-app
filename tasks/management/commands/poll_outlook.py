from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from tasks.models import List, Section
from tasks.services.outlook_auth import acquire_token_silent
from tasks.services.outlook_client import fetch_emails_by_category, update_email_categories
from tasks.services.outlook_import import create_task_from_email, parse_graph_message


class Command(BaseCommand):
    help = "Poll Outlook for emails tagged with the source category and create tasks"

    def handle(self, *args, **options):
        try:
            self._poll()
        except Exception as e:
            self._write_status(status="error", error=str(e))
            raise CommandError(str(e))

    def _poll(self):
        # Validate settings
        if not settings.OUTLOOK_CLIENT_ID:
            raise CommandError(
                "OUTLOOK_CLIENT_ID is not configured. "
                "Set it in your environment or Django settings."
            )

        if not settings.OUTLOOK_TOKEN_CACHE_FILE.exists():
            raise CommandError(
                "Token cache not found. Run 'manage.py outlook_auth' first."
            )

        # Acquire token
        access_token = acquire_token_silent()
        if not access_token:
            raise CommandError(
                "Could not acquire access token. Run 'manage.py outlook_auth' to re-authenticate."
            )

        # Fetch emails
        source_category = settings.OUTLOOK_SOURCE_CATEGORY
        processed_category = settings.OUTLOOK_PROCESSED_CATEGORY
        messages = fetch_emails_by_category(access_token, source_category)

        if not messages:
            self.stdout.write("No emails found with category: " + source_category)
            self._write_status(status="success", tasks_created=0, tasks_skipped=0)
            return

        # Ensure inbox list and section exist
        task_list, _ = List.objects.get_or_create(
            name=settings.OUTLOOK_INBOX_LIST_NAME,
            defaults={"position": List.objects.count()},
        )
        section, _ = Section.objects.get_or_create(
            list=task_list,
            name="Incoming",
            defaults={"position": 0},
        )

        tasks_created = 0
        tasks_skipped = 0

        for msg in messages:
            parsed = parse_graph_message(msg)
            task = create_task_from_email(parsed, section)

            if task:
                tasks_created += 1
            else:
                tasks_skipped += 1

            # Swap category: remove source, add processed
            new_categories = [
                c for c in parsed["categories"] if c != source_category
            ]
            new_categories.append(processed_category)
            update_email_categories(access_token, parsed["graph_id"], new_categories)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done: {tasks_created} created, {tasks_skipped} skipped"
            )
        )
        self._write_status(
            status="success",
            tasks_created=tasks_created,
            tasks_skipped=tasks_skipped,
        )

    def _write_status(self, *, status: str, **kwargs):
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            **kwargs,
        }
        status_path = settings.OUTLOOK_POLL_STATUS_FILE
        # Atomic write: write to temp file then rename
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=status_path.parent,
            suffix=".tmp",
            delete=False,
        ) as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name
        import os

        os.replace(tmp_path, status_path)
