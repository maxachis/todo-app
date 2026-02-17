import json

from django.test import Client, TestCase

from tasks.models import List, Section, Tag, Task


class ListAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_get_lists_returns_position_order(self):
        low = List.objects.create(name="Low", emoji="L", position=10)
        high = List.objects.create(name="High", emoji="H", position=20)

        response = self.client.get("/api/lists/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual([item["id"] for item in data], [low.id, high.id])

    def test_create_list(self):
        response = self.client.post(
            "/api/lists/",
            data=json.dumps({"name": "Work", "emoji": "W"}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], "Work")
        self.assertTrue(List.objects.filter(name="Work").exists())

    def test_get_list_detail_with_nested_sections_tasks_subtasks(self):
        task_list = List.objects.create(name="Main", emoji="M", position=10)
        section = Section.objects.create(list=task_list, name="Todo", emoji="", position=10)
        parent = Task.objects.create(section=section, title="Parent", position=10)
        child = Task.objects.create(section=section, parent=parent, title="Child", position=10)
        tag = Tag.objects.create(name="urgent")
        parent.tags.add(tag)

        response = self.client.get(f"/api/lists/{task_list.id}/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["sections"]), 1)
        self.assertEqual(data["sections"][0]["tasks"][0]["title"], "Parent")
        self.assertEqual(data["sections"][0]["tasks"][0]["subtasks"][0]["id"], child.id)
        self.assertEqual(data["sections"][0]["tasks"][0]["tags"][0]["name"], "urgent")

    def test_update_list(self):
        task_list = List.objects.create(name="Old", emoji="O", position=10)

        response = self.client.put(
            f"/api/lists/{task_list.id}/",
            data=json.dumps({"name": "New", "emoji": "N"}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 200)
        task_list.refresh_from_db()
        self.assertEqual(task_list.name, "New")
        self.assertEqual(task_list.emoji, "N")

    def test_delete_list(self):
        task_list = List.objects.create(name="Delete", emoji="", position=10)

        response = self.client.delete(
            f"/api/lists/{task_list.id}/",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(List.objects.filter(pk=task_list.id).exists())

    def test_move_list_reorders_positions(self):
        first = List.objects.create(name="A", emoji="", position=10)
        middle = List.objects.create(name="B", emoji="", position=20)
        last = List.objects.create(name="C", emoji="", position=30)

        response = self.client.patch(
            f"/api/lists/{last.id}/move/",
            data=json.dumps({"position": 0}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 200)
        ids = list(List.objects.order_by("position").values_list("id", flat=True))
        self.assertEqual(ids, [last.id, first.id, middle.id])
