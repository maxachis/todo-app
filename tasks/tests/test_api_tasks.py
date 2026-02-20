import json
from datetime import date, time

from django.test import Client, TestCase

from tasks.models import List, Section, Task


class TaskAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.list_a = List.objects.create(name="A", emoji="", position=10)
        self.section_a = Section.objects.create(list=self.list_a, name="Todo", emoji="", position=10)

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_create_task_with_optional_parent(self):
        parent = Task.objects.create(section=self.section_a, title="Parent", position=10)

        response = self.client.post(
            f"/api/sections/{self.section_a.id}/tasks/",
            data=json.dumps({"title": "Child", "parent_id": parent.id}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["parent_id"], parent.id)

    def test_get_task_detail(self):
        parent = Task.objects.create(section=self.section_a, title="Parent", notes="n", position=10)
        child = Task.objects.create(section=self.section_a, parent=parent, title="Child", position=10)

        response = self.client.get(f"/api/tasks/{parent.id}/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Parent")
        self.assertEqual(data["subtasks"][0]["id"], child.id)

    def test_update_task_fields(self):
        task = Task.objects.create(section=self.section_a, title="Old", position=10)

        response = self.client.put(
            f"/api/tasks/{task.id}/",
            data=json.dumps(
                {
                    "title": "New",
                    "notes": "Updated",
                    "due_date": str(date(2026, 3, 15)),
                    "due_time": str(time(9, 30)),
                    "priority": 3,
                }
            ),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.title, "New")
        self.assertEqual(task.notes, "Updated")
        self.assertEqual(task.priority, 3)

    def test_delete_task_cascades(self):
        parent = Task.objects.create(section=self.section_a, title="Parent", position=10)
        child = Task.objects.create(section=self.section_a, parent=parent, title="Child", position=10)

        response = self.client.delete(f"/api/tasks/{parent.id}/", **self._headers())

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=parent.id).exists())
        self.assertFalse(Task.objects.filter(pk=child.id).exists())

    def test_complete_task_cascades_to_subtasks(self):
        parent = Task.objects.create(section=self.section_a, title="Parent", position=10)
        child = Task.objects.create(section=self.section_a, parent=parent, title="Child", position=10)

        response = self.client.post(f"/api/tasks/{parent.id}/complete/", data="{}", content_type="application/json", **self._headers())

        self.assertEqual(response.status_code, 200)
        parent.refresh_from_db()
        child.refresh_from_db()
        self.assertTrue(parent.is_completed)
        self.assertTrue(child.is_completed)

    def test_uncomplete_task_only_affects_target(self):
        parent = Task.objects.create(section=self.section_a, title="Parent", position=10, is_completed=True)
        child = Task.objects.create(section=self.section_a, parent=parent, title="Child", position=10, is_completed=True)

        response = self.client.post(
            f"/api/tasks/{parent.id}/uncomplete/",
            data="{}",
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 200)
        parent.refresh_from_db()
        child.refresh_from_db()
        self.assertFalse(parent.is_completed)
        self.assertTrue(child.is_completed)

    def test_move_task_reparent_and_reject_circular_nesting(self):
        parent = Task.objects.create(section=self.section_a, title="Parent", position=10)
        child = Task.objects.create(section=self.section_a, parent=parent, title="Child", position=10)

        circular_response = self.client.patch(
            f"/api/tasks/{parent.id}/move/",
            data=json.dumps({"parent_id": child.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(circular_response.status_code, 409)

        response = self.client.patch(
            f"/api/tasks/{child.id}/move/",
            data=json.dumps({"parent_id": None, "position": 0}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(response.status_code, 200)
        child.refresh_from_db()
        self.assertIsNone(child.parent_id)

    def test_move_task_across_sections_and_lists(self):
        section_b = Section.objects.create(list=self.list_a, name="Doing", emoji="", position=20)
        list_b = List.objects.create(name="B", emoji="", position=20)
        section_c = Section.objects.create(list=list_b, name="Inbox", emoji="", position=10)
        task = Task.objects.create(section=self.section_a, title="Move me", position=10)

        to_section_response = self.client.patch(
            f"/api/tasks/{task.id}/move/",
            data=json.dumps({"section_id": section_b.id, "position": 0}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(to_section_response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.section_id, section_b.id)

        to_list_response = self.client.patch(
            f"/api/tasks/{task.id}/move/",
            data=json.dumps({"list_id": list_b.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(to_list_response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.section_id, section_c.id)

    def test_pin_toggle_and_limit(self):
        one = Task.objects.create(section=self.section_a, title="1", position=10)
        two = Task.objects.create(section=self.section_a, title="2", position=20)
        three = Task.objects.create(section=self.section_a, title="3", position=30)
        four = Task.objects.create(section=self.section_a, title="4", position=40)

        for task in [one, two, three]:
            response = self.client.post(
                f"/api/tasks/{task.id}/pin/",
                data="{}",
                content_type="application/json",
                **self._headers(),
            )
            self.assertEqual(response.status_code, 200)

        over_limit_response = self.client.post(
            f"/api/tasks/{four.id}/pin/",
            data="{}",
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(over_limit_response.status_code, 409)

        unpin_response = self.client.post(
            f"/api/tasks/{one.id}/pin/",
            data="{}",
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(unpin_response.status_code, 200)
        one.refresh_from_db()
        self.assertFalse(one.is_pinned)
