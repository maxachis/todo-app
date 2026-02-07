import csv
import io
import json

from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import List, Section, Tag, Task


class ViewTestBase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.task_list = List.objects.create(name="Work", emoji="💼", position=10)
        self.section = Section.objects.create(
            list=self.task_list, name="To Do", position=10
        )
        self.task = Task.objects.create(
            section=self.section, title="Write tests", position=10
        )


class ListViewTests(ViewTestBase):
    def test_tv1_create_list(self):
        """T-V-1: POST to create list returns success and list appears."""
        response = self.client.post(
            reverse("create_list"),
            {"name": "Personal", "emoji": "🏠"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(List.objects.filter(name="Personal").exists())
        self.assertIn(b"Personal", response.content)

    def test_tv2_rename_list(self):
        """T-V-2: POST to rename list updates name."""
        response = self.client.post(
            reverse("update_list", args=[self.task_list.pk]),
            {"name": "Work Updated"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task_list.refresh_from_db()
        self.assertEqual(self.task_list.name, "Work Updated")

    def test_tv3_delete_list(self):
        """T-V-3: DELETE list returns success and list is removed."""
        response = self.client.post(
            reverse("delete_list", args=[self.task_list.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(List.objects.filter(pk=self.task_list.pk).exists())

    def test_tv4_list_detail(self):
        """T-V-4: GET list detail returns sections and tasks."""
        response = self.client.get(
            reverse("list_detail", args=[self.task_list.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"To Do", response.content)
        self.assertIn(b"Write tests", response.content)


class SectionViewTests(ViewTestBase):
    def test_tv5_create_section(self):
        """T-V-5: POST to create section within a list succeeds."""
        response = self.client.post(
            reverse("create_section", args=[self.task_list.pk]),
            {"name": "In Progress"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Section.objects.filter(name="In Progress").exists())

    def test_tv6_delete_section(self):
        """T-V-6: DELETE section returns success."""
        response = self.client.post(
            reverse("delete_section", args=[self.section.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Section.objects.filter(pk=self.section.pk).exists())


class TaskViewTests(ViewTestBase):
    def test_tv7_create_task(self):
        """T-V-7: POST to create task within a section succeeds."""
        response = self.client.post(
            reverse("create_task", args=[self.section.pk]),
            {"title": "New task"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(title="New task").exists())

    def test_tv8_create_subtask(self):
        """T-V-8: POST to create subtask with parent ID succeeds."""
        response = self.client.post(
            reverse("create_task", args=[self.section.pk]),
            {"title": "Subtask", "parent": self.task.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        subtask = Task.objects.get(title="Subtask")
        self.assertEqual(subtask.parent, self.task)

    def test_tv9_update_task_title(self):
        """T-V-9: POST to update task title succeeds."""
        response = self.client.post(
            reverse("update_task", args=[self.task.pk]),
            {"title": "Updated title"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated title")

    def test_tv10_delete_task(self):
        """T-V-10: DELETE task removes it and its subtasks."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
        response = self.client.post(
            reverse("delete_task", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assertFalse(Task.objects.filter(pk=sub.pk).exists())

    def test_tv11_update_task_notes(self):
        """T-V-11: POST to update task notes saves Markdown content."""
        response = self.client.post(
            reverse("update_task", args=[self.task.pk]),
            {"notes": "# Hello\n\nSome **bold** text"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.notes, "# Hello\n\nSome **bold** text")

    def test_tv12_set_clear_due_date(self):
        """T-V-12: POST to set/clear due date succeeds."""
        # Set due date
        response = self.client.post(
            reverse("update_task", args=[self.task.pk]),
            {"due_date": "2026-03-15"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(str(self.task.due_date), "2026-03-15")

        # Clear due date
        response = self.client.post(
            reverse("update_task", args=[self.task.pk]),
            {"due_date": ""},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertIsNone(self.task.due_date)

    def test_tv13_rendered_notes_contain_links(self):
        """T-V-13: Rendered notes contain clickable <a> tags for URLs."""
        self.task.notes = "Visit https://example.com for details"
        self.task.save()

        response = self.client.get(
            reverse("task_detail", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("<a", content)
        self.assertIn("https://example.com", content)
        self.assertIn('target="_blank"', content)


class TaskCompletionViewTests(ViewTestBase):
    def test_tv14_complete_task(self):
        """T-V-14: POST to complete task returns updated task."""
        response = self.client.post(
            reverse("complete_task", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        # Completed tasks should appear under "Completed" heading
        self.assertIn(b"Completed", response.content)

    def test_tv15_complete_includes_toast(self):
        """T-V-15: Complete task response includes undo toast HTML fragment."""
        response = self.client.post(
            reverse("complete_task", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("undo-toast", content)
        self.assertIn("Undo", content)

    def test_tv16_undo_completion(self):
        """T-V-16: POST to undo completion reverts task status."""
        self.task.complete()
        response = self.client.post(
            reverse("uncomplete_task", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

    def test_tv17_uncomplete_task(self):
        """T-V-17: POST to un-complete a task at any time succeeds."""
        self.task.complete()
        response = self.client.post(
            reverse("uncomplete_task", args=[self.task.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
        self.assertIsNone(self.task.completed_at)


class TaskMoveViewTests(ViewTestBase):
    def test_tv18_reorder_within_section(self):
        """T-V-18: POST to reorder task within section updates positions."""
        task2 = Task.objects.create(
            section=self.section, title="Task 2", position=20
        )
        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"position": "30"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.position, 30)

    def test_tv19_move_to_different_section(self):
        """T-V-19: POST to move task to different section updates section FK."""
        new_section = Section.objects.create(
            list=self.task_list, name="Done", position=20
        )
        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"section": new_section.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.section, new_section)

    def test_tv20_nest_under_parent(self):
        """T-V-20: POST to nest task under a parent sets parent FK."""
        parent = Task.objects.create(
            section=self.section, title="Parent", position=20
        )
        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"parent": parent.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.parent, parent)

    def test_tv21_promote_subtask(self):
        """T-V-21: POST to promote subtask clears parent FK."""
        parent = Task.objects.create(
            section=self.section, title="Parent", position=5
        )
        self.task.parent = parent
        self.task.save()

        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"parent": ""},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertIsNone(self.task.parent)

    def test_tv22_move_to_different_list(self):
        """T-V-22: POST to move task to different list updates section."""
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
        self.assertEqual(self.task.section, other_section)

    def test_tv23_move_to_list_no_sections(self):
        """T-V-23: Moving task to a list with no sections returns error."""
        empty_list = List.objects.create(name="Empty", position=30)

        response = self.client.post(
            reverse("move_task", args=[self.task.pk]),
            {"list": empty_list.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 400)

    def test_tv24_move_parent_subtasks_follow(self):
        """T-V-24: Moving a parent task — subtasks remain attached."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
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
        sub.refresh_from_db()
        self.assertEqual(self.task.section, other_section)
        self.assertEqual(sub.section, other_section)
        self.assertEqual(sub.parent, self.task)


class ExportViewTests(ViewTestBase):
    def test_tv25_export_single_list(self):
        """T-V-25: GET export for a single list returns a downloadable file."""
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "json"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])

    def test_tv26_export_all_lists(self):
        """T-V-26: GET export for all lists returns a downloadable file."""
        response = self.client.get(reverse("export_all", args=["json"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])

    def test_tv27_json_export_nested(self):
        """T-V-27: JSON export contains nested hierarchy."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "json"])
        )
        data = json.loads(response.content)
        self.assertEqual(data["name"], "Work")
        tasks = data["sections"][0]["tasks"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(len(tasks[0]["subtasks"]), 1)
        self.assertEqual(tasks[0]["subtasks"][0]["title"], "Sub")

    def test_tv28_csv_export(self):
        """T-V-28: CSV export has one row per task with correct columns."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "csv"])
        )
        content = response.content.decode()
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["task"], "Write tests")
        self.assertEqual(rows[0]["depth"], "0")
        self.assertEqual(rows[1]["task"], "Sub")
        self.assertEqual(rows[1]["parent_task"], "Write tests")
        self.assertEqual(rows[1]["depth"], "1")

    def test_tv29_markdown_export(self):
        """T-V-29: Markdown export has headings, checkboxes, indented subtasks."""
        self.task.complete()
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "md"])
        )
        content = response.content.decode()
        self.assertIn("# Work", content)
        self.assertIn("## To Do", content)
        self.assertIn("[x]", content)
        self.assertIn("[ ]", content)
        self.assertIn("  - [ ] Sub", content)

    def test_tv30_export_content_disposition(self):
        """T-V-30: Export response has Content-Disposition with correct filename."""
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "json"])
        )
        self.assertIn(
            'attachment; filename="work.json"',
            response["Content-Disposition"],
        )

    def test_tv31_export_empty_list(self):
        """T-V-31: Exporting an empty list returns valid file with headers only."""
        empty_list = List.objects.create(name="Empty", position=20)
        Section.objects.create(list=empty_list, name="Default", position=10)

        # JSON
        response = self.client.get(
            reverse("export_list", args=[empty_list.pk, "json"])
        )
        data = json.loads(response.content)
        self.assertEqual(data["name"], "Empty")
        self.assertEqual(data["sections"][0]["tasks"], [])

        # CSV
        response = self.client.get(
            reverse("export_list", args=[empty_list.pk, "csv"])
        )
        content = response.content.decode()
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        self.assertEqual(len(rows), 0)

        # Markdown
        response = self.client.get(
            reverse("export_list", args=[empty_list.pk, "md"])
        )
        content = response.content.decode()
        self.assertIn("# Empty", content)
        self.assertIn("## Default", content)

    def test_tv32_unsupported_format(self):
        """T-V-32: Requesting an unsupported export format returns 400."""
        response = self.client.get(
            reverse("export_list", args=[self.task_list.pk, "xml"])
        )
        self.assertEqual(response.status_code, 400)
