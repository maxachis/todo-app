import json
from datetime import date

from django.test import Client, TestCase

from tasks.models import List, Project, ProjectLink, Section, Task, TimeEntry


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

    def test_project_links_crud(self):
        project = Project.objects.create(name="Proj", description="", position=10)

        # List empty
        resp = self.client.get(f"/api/projects/{project.id}/links/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

        # Create
        resp = self.client.post(
            f"/api/projects/{project.id}/links/",
            data=json.dumps({"url": "https://github.com/org/repo", "descriptor": "GitHub Repo"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 201)
        link_id = resp.json()["id"]
        self.assertEqual(resp.json()["url"], "https://github.com/org/repo")
        self.assertEqual(resp.json()["descriptor"], "GitHub Repo")
        self.assertEqual(resp.json()["project_id"], project.id)

        # List with link
        resp = self.client.get(f"/api/projects/{project.id}/links/")
        self.assertEqual(len(resp.json()), 1)

        # Update descriptor
        resp = self.client.put(
            f"/api/projects/{project.id}/links/{link_id}/",
            data=json.dumps({"descriptor": "Main Repo"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["descriptor"], "Main Repo")

        # Update url
        resp = self.client.put(
            f"/api/projects/{project.id}/links/{link_id}/",
            data=json.dumps({"url": "https://github.com/org/repo2"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["url"], "https://github.com/org/repo2")

        # Delete
        resp = self.client.delete(
            f"/api/projects/{project.id}/links/{link_id}/",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(ProjectLink.objects.filter(pk=link_id).exists())

    def test_project_links_blank_url_rejected(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        resp = self.client.post(
            f"/api/projects/{project.id}/links/",
            data=json.dumps({"url": "", "descriptor": "Something"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 422)

    def test_project_links_blank_descriptor_rejected(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        resp = self.client.post(
            f"/api/projects/{project.id}/links/",
            data=json.dumps({"url": "https://example.com", "descriptor": ""}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 422)

    def test_project_links_update_blank_url_rejected(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        link = ProjectLink.objects.create(project=project, url="https://a.com", descriptor="A")
        resp = self.client.put(
            f"/api/projects/{project.id}/links/{link.id}/",
            data=json.dumps({"url": ""}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 422)

    def test_project_links_delete_nonexistent(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        resp = self.client.delete(
            f"/api/projects/{project.id}/links/99999/",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 404)

    def test_project_links_cascade_on_project_delete(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        link = ProjectLink.objects.create(project=project, url="https://a.com", descriptor="A")
        link_id = link.id
        project.delete()
        self.assertFalse(ProjectLink.objects.filter(pk=link_id).exists())

    def test_project_list_includes_links(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        ProjectLink.objects.create(project=project, url="https://a.com", descriptor="A")

        resp = self.client.get("/api/projects/")
        self.assertEqual(resp.status_code, 200)
        project_data = resp.json()[0]
        self.assertIn("links", project_data)
        self.assertEqual(len(project_data["links"]), 1)
        self.assertEqual(project_data["links"][0]["url"], "https://a.com")

    def test_project_list_includes_empty_links(self):
        Project.objects.create(name="Proj", description="", position=10)
        resp = self.client.get("/api/projects/")
        project_data = resp.json()[0]
        self.assertEqual(project_data["links"], [])

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

    def test_timesheet_task_details_with_hierarchy(self):
        project = Project.objects.create(name="Proj", description="", position=10)
        task_list = List.objects.create(name="Work", emoji="", position=10, project=project)
        section = Section.objects.create(list=task_list, name="Todo", emoji="", position=10)

        # Create a 3-level hierarchy: parent > child > grandchild
        parent = Task.objects.create(section=section, title="Feature A", position=10)
        child = Task.objects.create(section=section, title="Design", position=20, parent=parent)
        grandchild = Task.objects.create(
            section=section, title="Mock up screens", position=30, parent=child
        )

        # Entry with top-level task
        entry1 = TimeEntry.objects.create(
            project=project, date=date(2026, 2, 17), description="Top level"
        )
        entry1.tasks.add(parent)

        # Entry with nested tasks
        entry2 = TimeEntry.objects.create(
            project=project, date=date(2026, 2, 17), description="Nested work"
        )
        entry2.tasks.add(child, grandchild)

        # Entry with no tasks
        TimeEntry.objects.create(
            project=project, date=date(2026, 2, 17), description="No tasks"
        )

        response = self.client.get("/api/timesheet/?week=2026-02-16")
        self.assertEqual(response.status_code, 200)
        entries = response.json()["entries_by_date"]["2026-02-17"]

        # Entries are ordered by -created_at, so last created first
        no_tasks_entry = entries[0]
        self.assertEqual(no_tasks_entry["task_details"], [])

        nested_entry = entries[1]
        details_by_id = {d["id"]: d for d in nested_entry["task_details"]}
        self.assertIn(child.id, details_by_id)
        self.assertEqual(details_by_id[child.id]["title"], "Design")
        self.assertEqual(details_by_id[child.id]["parent_titles"], ["Feature A"])
        self.assertIn(grandchild.id, details_by_id)
        self.assertEqual(details_by_id[grandchild.id]["title"], "Mock up screens")
        self.assertEqual(
            details_by_id[grandchild.id]["parent_titles"], ["Feature A", "Design"]
        )

        top_entry = entries[2]
        self.assertEqual(len(top_entry["task_details"]), 1)
        self.assertEqual(top_entry["task_details"][0]["title"], "Feature A")
        self.assertEqual(top_entry["task_details"][0]["parent_titles"], [])

    def test_timesheet_summary_includes_overall_hours(self):
        project = Project.objects.create(name="Alpha", description="", position=10)
        # 3 entries in the target week (Feb 15-21)
        for day in [17, 18, 19]:
            TimeEntry.objects.create(project=project, date=date(2026, 2, day))
        # 2 entries in a different week
        TimeEntry.objects.create(project=project, date=date(2026, 2, 10))
        TimeEntry.objects.create(project=project, date=date(2026, 2, 11))

        response = self.client.get("/api/timesheet/?week=2026-02-16")
        self.assertEqual(response.status_code, 200)
        summary = response.json()["summary"]
        self.assertEqual(summary["total_hours"], 3)
        self.assertEqual(summary["overall_total_hours"], 5)
        self.assertEqual(len(summary["per_project"]), 1)
        self.assertEqual(summary["per_project"][0]["hours"], 3)
        self.assertEqual(summary["per_project"][0]["overall_hours"], 5)

    def test_timesheet_summary_includes_zero_weekly_projects(self):
        active = Project.objects.create(name="Active", description="", position=10)
        inactive = Project.objects.create(name="Inactive", description="", position=20)
        # Active project: entries in target week and another week
        TimeEntry.objects.create(project=active, date=date(2026, 2, 17))
        TimeEntry.objects.create(project=active, date=date(2026, 2, 10))
        # Inactive project: entries only in another week
        TimeEntry.objects.create(project=inactive, date=date(2026, 2, 10))
        TimeEntry.objects.create(project=inactive, date=date(2026, 2, 11))

        response = self.client.get("/api/timesheet/?week=2026-02-16")
        self.assertEqual(response.status_code, 200)
        summary = response.json()["summary"]
        self.assertEqual(summary["total_hours"], 1)
        self.assertEqual(summary["overall_total_hours"], 4)
        # Active project should be first (1 weekly hour), inactive second (0 weekly hours)
        self.assertEqual(len(summary["per_project"]), 2)
        self.assertEqual(summary["per_project"][0]["project_name"], "Active")
        self.assertEqual(summary["per_project"][0]["hours"], 1)
        self.assertEqual(summary["per_project"][0]["overall_hours"], 2)
        self.assertEqual(summary["per_project"][1]["project_name"], "Inactive")
        self.assertEqual(summary["per_project"][1]["hours"], 0)
        self.assertEqual(summary["per_project"][1]["overall_hours"], 2)

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
