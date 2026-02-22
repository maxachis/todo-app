from __future__ import annotations

from django.test import TestCase

from tasks.models import List, Section, Task
from tasks.services.outlook_import import (
    BODY_MAX_LENGTH,
    TRUNCATION_INDICATOR,
    create_task_from_email,
    parse_graph_message,
)


class TestParseGraphMessage(TestCase):
    def test_html_email(self):
        msg = {
            "id": "graph-id-1",
            "subject": "Review Q3 budget",
            "sender": {
                "emailAddress": {"name": "Jane Doe", "address": "jane@example.com"}
            },
            "internetMessageId": "<msg001@example.com>",
            "body": {
                "contentType": "html",
                "content": "<html><body><p>Please review the attached budget.</p></body></html>",
            },
            "categories": ["ToDo"],
        }
        result = parse_graph_message(msg)
        self.assertEqual(result["subject"], "Review Q3 budget")
        self.assertEqual(result["sender"], "Jane Doe <jane@example.com>")
        self.assertEqual(result["internet_message_id"], "<msg001@example.com>")
        self.assertIn("From: Jane Doe <jane@example.com>", result["notes"])
        self.assertIn("Please review the attached budget", result["notes"])
        # HTML tags should be stripped
        self.assertNotIn("<p>", result["notes"])

    def test_plain_text_email(self):
        msg = {
            "id": "graph-id-2",
            "subject": "Quick note",
            "sender": {
                "emailAddress": {"name": "Bob", "address": "bob@example.com"}
            },
            "internetMessageId": "<msg002@example.com>",
            "body": {
                "contentType": "text",
                "content": "Just a plain text message.",
            },
            "categories": [],
        }
        result = parse_graph_message(msg)
        self.assertIn("Just a plain text message", result["notes"])

    def test_truncation(self):
        long_body = "x" * (BODY_MAX_LENGTH + 500)
        msg = {
            "id": "graph-id-3",
            "subject": "Long email",
            "sender": {"emailAddress": {"name": "", "address": ""}},
            "internetMessageId": "<msg003@example.com>",
            "body": {"contentType": "text", "content": long_body},
            "categories": [],
        }
        result = parse_graph_message(msg)
        # Notes should be truncated (body + no sender line)
        self.assertTrue(result["notes"].endswith(TRUNCATION_INDICATOR))
        self.assertLessEqual(
            len(result["notes"]), BODY_MAX_LENGTH + len(TRUNCATION_INDICATOR)
        )

    def test_missing_body(self):
        msg = {
            "id": "graph-id-4",
            "subject": "No body",
            "sender": {
                "emailAddress": {"name": "Alice", "address": "alice@example.com"}
            },
            "internetMessageId": "<msg004@example.com>",
            "body": {"contentType": "text", "content": ""},
            "categories": [],
        }
        result = parse_graph_message(msg)
        self.assertIn("From: Alice <alice@example.com>", result["notes"])

    def test_sender_extraction_name_only(self):
        msg = {
            "id": "graph-id-5",
            "subject": "Test",
            "sender": {"emailAddress": {"name": "OnlyName", "address": ""}},
            "internetMessageId": "<msg005@example.com>",
            "body": {"contentType": "text", "content": "body"},
            "categories": [],
        }
        result = parse_graph_message(msg)
        self.assertEqual(result["sender"], "OnlyName")

    def test_no_subject(self):
        msg = {
            "id": "graph-id-6",
            "sender": {"emailAddress": {"name": "", "address": ""}},
            "internetMessageId": "<msg006@example.com>",
            "body": {"contentType": "text", "content": ""},
            "categories": [],
        }
        result = parse_graph_message(msg)
        self.assertEqual(result["subject"], "(no subject)")


class TestCreateTaskFromEmail(TestCase):
    def setUp(self):
        self.task_list = List.objects.create(name="Email Inbox", position=0)
        self.section = Section.objects.create(
            list=self.task_list, name="Incoming", position=0
        )

    def test_creates_task(self):
        parsed = {
            "subject": "Review budget",
            "notes": "From: Jane\n\nPlease review.",
            "internet_message_id": "<unique-id-1@example.com>",
        }
        task = create_task_from_email(parsed, self.section)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Review budget")
        self.assertEqual(task.external_id, "<unique-id-1@example.com>")
        self.assertEqual(task.section, self.section)

    def test_deduplication_by_external_id(self):
        parsed = {
            "subject": "Review budget",
            "notes": "From: Jane\n\nPlease review.",
            "internet_message_id": "<unique-id-2@example.com>",
        }
        # First call creates
        task1 = create_task_from_email(parsed, self.section)
        self.assertIsNotNone(task1)

        # Second call skips
        task2 = create_task_from_email(parsed, self.section)
        self.assertIsNone(task2)

        # Only one task exists
        self.assertEqual(Task.objects.filter(external_id="<unique-id-2@example.com>").count(), 1)

    def test_skips_empty_message_id(self):
        parsed = {
            "subject": "No ID",
            "notes": "body",
            "internet_message_id": "",
        }
        task = create_task_from_email(parsed, self.section)
        self.assertIsNone(task)

    def test_position_increments(self):
        for i in range(3):
            parsed = {
                "subject": f"Task {i}",
                "notes": "body",
                "internet_message_id": f"<pos-test-{i}@example.com>",
            }
            create_task_from_email(parsed, self.section)

        tasks = Task.objects.filter(section=self.section).order_by("position")
        positions = [t.position for t in tasks]
        self.assertEqual(positions, [1, 2, 3])
