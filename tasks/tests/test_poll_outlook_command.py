from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase, override_settings

from tasks.models import List, Section, Task


@override_settings(
    OUTLOOK_CLIENT_ID="test-client-id",
    OUTLOOK_TOKEN_CACHE_FILE=Path("/tmp/test_outlook_token_cache.json"),
    OUTLOOK_POLL_STATUS_FILE=Path("/tmp/test_outlook_poll_status.json"),
    OUTLOOK_SOURCE_CATEGORY="ToDo",
    OUTLOOK_PROCESSED_CATEGORY="ToDo-Imported",
    OUTLOOK_INBOX_LIST_NAME="Email Inbox",
)
class TestPollOutlookCommand(TestCase):
    def setUp(self):
        # Create a fake token cache file
        Path("/tmp/test_outlook_token_cache.json").write_text("{}")
        # Clean up status file
        Path("/tmp/test_outlook_poll_status.json").unlink(missing_ok=True)

    def tearDown(self):
        Path("/tmp/test_outlook_token_cache.json").unlink(missing_ok=True)
        Path("/tmp/test_outlook_poll_status.json").unlink(missing_ok=True)

    @patch("tasks.services.outlook_client.requests.patch")
    @patch("tasks.services.outlook_client.requests.get")
    @patch("tasks.services.outlook_auth.acquire_token_silent")
    def test_creates_tasks_from_emails(self, mock_token, mock_get, mock_patch):
        mock_token.return_value = "fake-access-token"

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "value": [
                {
                    "id": "graph-1",
                    "subject": "Review budget",
                    "sender": {
                        "emailAddress": {
                            "name": "Jane",
                            "address": "jane@example.com",
                        }
                    },
                    "internetMessageId": "<cmd-test-1@example.com>",
                    "body": {"contentType": "text", "content": "Please review."},
                    "categories": ["ToDo"],
                },
                {
                    "id": "graph-2",
                    "subject": "Update docs",
                    "sender": {
                        "emailAddress": {
                            "name": "Bob",
                            "address": "bob@example.com",
                        }
                    },
                    "internetMessageId": "<cmd-test-2@example.com>",
                    "body": {"contentType": "text", "content": "Docs need updating."},
                    "categories": ["ToDo"],
                },
            ]
        }
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        mock_patch.return_value = patch_resp

        call_command("poll_outlook")

        # Verify tasks created
        self.assertEqual(Task.objects.count(), 2)
        self.assertTrue(Task.objects.filter(external_id="<cmd-test-1@example.com>").exists())
        self.assertTrue(Task.objects.filter(external_id="<cmd-test-2@example.com>").exists())

        # Verify list and section created
        self.assertTrue(List.objects.filter(name="Email Inbox").exists())
        self.assertTrue(Section.objects.filter(name="Incoming").exists())

        # Verify categories were swapped (2 emails = 2 PATCH calls)
        self.assertEqual(mock_patch.call_count, 2)

        # Verify status file written
        status_path = Path("/tmp/test_outlook_poll_status.json")
        self.assertTrue(status_path.exists())
        status = json.loads(status_path.read_text())
        self.assertEqual(status["status"], "success")
        self.assertEqual(status["tasks_created"], 2)
        self.assertEqual(status["tasks_skipped"], 0)

    @patch("tasks.services.outlook_client.requests.get")
    @patch("tasks.services.outlook_auth.acquire_token_silent")
    def test_skips_duplicates(self, mock_token, mock_get):
        mock_token.return_value = "fake-access-token"

        # Pre-create a task with the same external_id
        task_list = List.objects.create(name="Email Inbox", position=0)
        section = Section.objects.create(list=task_list, name="Incoming", position=0)
        Task.objects.create(
            title="Already imported",
            section=section,
            external_id="<dup-test@example.com>",
            position=1,
        )

        mock_resp = MagicMock()
        mock_resp.json.return_value = {"value": []}
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        call_command("poll_outlook")

        # Only the pre-existing task
        self.assertEqual(Task.objects.count(), 1)

    @patch("tasks.services.outlook_auth.acquire_token_silent")
    def test_no_token_raises_error(self, mock_token):
        mock_token.return_value = None

        with self.assertRaises(Exception):
            call_command("poll_outlook")

        # Status file should indicate error
        status_path = Path("/tmp/test_outlook_poll_status.json")
        self.assertTrue(status_path.exists())
        status = json.loads(status_path.read_text())
        self.assertEqual(status["status"], "error")


class TestOutlookStatusEndpoint(TestCase):
    def test_no_status_file(self):
        with override_settings(
            OUTLOOK_POLL_STATUS_FILE=Path("/tmp/nonexistent_status.json")
        ):
            from django.test import Client

            client = Client()
            resp = client.get("/api/import/outlook/status/")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertEqual(data["status"], "no_data")

    def test_status_file_present(self):
        status_path = Path("/tmp/test_api_outlook_status.json")
        status_path.write_text(
            json.dumps(
                {
                    "timestamp": "2026-01-01T00:00:00Z",
                    "status": "error",
                    "error": "Token expired",
                }
            )
        )
        try:
            with override_settings(OUTLOOK_POLL_STATUS_FILE=status_path):
                from django.test import Client

                client = Client()
                resp = client.get("/api/import/outlook/status/")
                self.assertEqual(resp.status_code, 200)
                data = resp.json()
                self.assertEqual(data["status"], "error")
                self.assertEqual(data["error"], "Token expired")
        finally:
            status_path.unlink(missing_ok=True)
