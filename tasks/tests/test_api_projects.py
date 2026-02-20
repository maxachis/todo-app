import json
from datetime import date

from django.test import Client, TestCase

from tasks.models import List, Project, Section, Task, TimeEntry


class ProjectAndTimesheetAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_projects_crud_toggle_and_metrics(self):
        create_response = self.client.post(
            "/api/projects/",
            data=json.dumps({"name": "Q1 Sprint", "description": "First quarter"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(create_response.status_code, 201)
        project_id = create_response.json()["id"]

        project = Project.objects.get(pk=project_id)
        task_list = List.objects.create(name="Work", emoji="", position=10, project=project)
        section = Section.objects.create(list=task_list, name="Todo", emoji="", position=10)
        done = Task.objects.create(section=section, title="Done", position=10, is_completed=True)
        Task.objects.create(section=section, title="Open", position=20, is_completed=False)
        entry = TimeEntry.objects.create(project=project, date=date(2026, 2, 17), description="Work")
        entry.tasks.add(done)

        list_response = self.client.get("/api/projects/")
        self.assertEqual(list_response.status_code, 200)
        project_data = list_response.json()[0]
        self.assertEqual(project_data["linked_lists_count"], 1)
        self.assertEqual(project_data["total_tasks"], 2)
        self.assertEqual(project_data["completed_tasks"], 1)
        self.assertEqual(project_data["total_hours"], 1.0)

        update_response = self.client.put(
            f"/api/projects/{project_id}/",
            data=json.dumps({"name": "Q1 Updated", "description": "Updated"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["name"], "Q1 Updated")

        toggle_response = self.client.post(
            f"/api/projects/{project_id}/toggle/",
            data="{}",
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(toggle_response.status_code, 200)
        self.assertFalse(toggle_response.json()["is_active"])

        delete_response = self.client.delete(f"/api/projects/{project_id}/", **self._headers())
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(Project.objects.filter(pk=project_id).exists())

    def test_get_project_tasks_returns_incomplete_only(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        task_list = List.objects.create(name="Work", emoji="", position=10, project=project)
        section = Section.objects.create(list=task_list, name="Todo", emoji="", position=10)
        open_task = Task.objects.create(section=section, title="Open", position=10, is_completed=False)
        Task.objects.create(section=section, title="Done", position=20, is_completed=True)

        response = self.client.get(f"/api/projects/{project.id}/tasks/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], open_task.id)

    def test_timesheet_get_post_delete(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        task_list = List.objects.create(name="Work", emoji="", position=10, project=project)
        section = Section.objects.create(list=task_list, name="Todo", emoji="", position=10)
        task = Task.objects.create(section=section, title="Task A", position=10)

        create_response = self.client.post(
            "/api/timesheet/",
            data=json.dumps(
                {
                    "project_id": project.id,
                    "date": "2026-02-17",
                    "description": "API design",
                    "task_ids": [task.id],
                }
            ),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        get_response = self.client.get("/api/timesheet/?week=2026-02-16")
        self.assertEqual(get_response.status_code, 200)
        payload = get_response.json()
        self.assertEqual(payload["summary"]["total_hours"], 1)
        self.assertIn("2026-02-17", payload["entries_by_date"])

        delete_response = self.client.delete(f"/api/timesheet/{entry_id}/", **self._headers())
        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(TimeEntry.objects.filter(pk=entry_id).exists())

    def test_timesheet_week_starts_sunday_and_includes_created_at(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        entry = TimeEntry.objects.create(project=project, date=date(2026, 2, 17), description="Planning")

        response = self.client.get("/api/timesheet/?week=2026-02-16")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["week_start"], "2026-02-15")
        self.assertEqual(payload["week_end"], "2026-02-21")
        self.assertIn("2026-02-17", payload["entries_by_date"])
        self.assertEqual(payload["entries_by_date"]["2026-02-17"][0]["id"], entry.id)
        self.assertIn("created_at", payload["entries_by_date"]["2026-02-17"][0])
