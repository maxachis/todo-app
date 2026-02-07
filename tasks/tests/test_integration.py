import json

from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import List, Section, Tag, Task


class IntegrationTestBase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.task_list = List.objects.create(name="Work", emoji="💼", position=10)
        self.section = Section.objects.create(
            list=self.task_list, name="To Do", position=10
        )
        self.task = Task.objects.create(
            section=self.section, title="Write code", position=10
        )


class HTMXIntegrationTests(IntegrationTestBase):
    def test_ti1_htmx_returns_partial(self):
        """T-I-1: HTMX requests return partial HTML fragments (not full pages)."""
        response = self.client.get(
            reverse("list_detail", args=[self.task_list.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        # Partial should NOT contain <!DOCTYPE html> or <html>
        self.assertNotIn("<!DOCTYPE", content)
        self.assertNotIn("<html", content)
        # But should contain the list content
        self.assertIn("To Do", content)

    def test_ti1_non_htmx_returns_full_page(self):
        """Non-HTMX requests return full pages."""
        response = self.client.get(
            reverse("list_detail", args=[self.task_list.pk])
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn("<html", content)

    def test_ti2_task_detail_right_sidebar(self):
        """T-I-2: Clicking a task returns right-sidebar HTML with task details."""
        self.task.notes = "Some **important** notes"
        self.task.save()

        response = self.client.get(
            reverse("task_detail", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("task-detail-content", content)
        self.assertIn("Write code", content)
        self.assertIn("Some **important** notes", content)

    def test_ti3_completed_tasks_under_completed_heading(self):
        """T-I-3: Completed tasks appear under a 'Completed' heading."""
        self.task.complete()

        response = self.client.get(
            reverse("list_detail", args=[self.task_list.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Completed", content)
        self.assertIn("Write code", content)

    def test_ti4_toast_auto_dismiss(self):
        """T-I-4: Undo toast fragment contains a 5-second auto-dismiss mechanism."""
        response = self.client.post(
            reverse("complete_task", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        content = response.content.decode()
        self.assertIn("undo-toast", content)
        self.assertIn('data-auto-dismiss="5000"', content)

    def test_ti5_markdown_strips_xss(self):
        """T-I-5: Markdown rendering strips dangerous HTML."""
        self.task.notes = '<script>alert("xss")</script>\n<img onerror="alert(1)" src=x>'
        self.task.save()

        response = self.client.get(
            reverse("task_detail", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        content = response.content.decode()

        # Extract just the rendered-notes section
        rendered_start = content.find('class="rendered-notes"')
        rendered_end = content.find("</div>", rendered_start + 1)
        rendered_section = content[rendered_start:rendered_end]

        # Script tags and event handlers should be stripped from rendered output
        self.assertNotIn("<script>", rendered_section)
        self.assertNotIn("onerror", rendered_section)

    def test_ti6_move_returns_updated_partial(self):
        """T-I-6: Drop triggers HTMX request and server returns updated partial."""
        new_section = Section.objects.create(
            list=self.task_list, name="Done", position=20
        )
        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"section": new_section.pk, "position": "10"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        # Should return the list detail partial
        self.assertNotIn("<!DOCTYPE", content)
        self.assertIn("Write code", content)

    def test_ti7_nesting_returns_subtask(self):
        """T-I-7: Nesting a task via move returns indented subtask in response."""
        parent = Task.objects.create(
            section=self.section, title="Parent task", position=5
        )
        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"parent": parent.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.parent, parent)

    def test_ti8_cross_list_move(self):
        """T-I-8: Cross-list move re-renders both source and target lists."""
        other_list = List.objects.create(name="Personal", position=20)
        other_section = Section.objects.create(
            list=other_list, name="Inbox", position=10
        )

        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"list": other_list.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.section.list, other_list)

    def test_ti9_export_triggers_download(self):
        """T-I-9: Export button triggers file download (Content-Disposition header present)."""
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "json"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Disposition", response)
        self.assertIn("attachment", response["Content-Disposition"])

    def test_ti10_json_export_roundtrippable(self):
        """T-I-10: JSON export of list with nested subtasks is valid JSON and round-trippable."""
        sub1 = Task.objects.create(
            section=self.section, title="Sub1", parent=self.task, position=20
        )
        sub2 = Task.objects.create(
            section=self.section, title="Sub2", parent=sub1, position=30
        )
        tag = Tag.objects.create(name="urgent")
        self.task.tags.add(tag)

        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "json"])
        )
        data = json.loads(response.content)

        # Verify structure
        self.assertEqual(data["name"], "Work")
        sections = data["sections"]
        self.assertEqual(len(sections), 1)
        tasks = sections[0]["tasks"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Write code")
        self.assertEqual(tasks[0]["tags"], ["urgent"])
        self.assertEqual(len(tasks[0]["subtasks"]), 1)
        self.assertEqual(tasks[0]["subtasks"][0]["title"], "Sub1")
        self.assertEqual(len(tasks[0]["subtasks"][0]["subtasks"]), 1)
        self.assertEqual(tasks[0]["subtasks"][0]["subtasks"][0]["title"], "Sub2")

        # Round-trip: serialize back and compare
        re_serialized = json.dumps(data)
        re_parsed = json.loads(re_serialized)
        self.assertEqual(data, re_parsed)

    def test_ti11_markdown_export_completed_checkbox(self):
        """T-I-11: Markdown export of completed tasks uses [x] checkbox syntax."""
        self.task.complete()
        uncompleted = Task.objects.create(
            section=self.section, title="Not done", position=20
        )

        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "md"])
        )
        content = response.content.decode()
        self.assertIn("- [x] Write code", content)
        self.assertIn("- [ ] Not done", content)
