import json

from django.test import Client, TestCase

from tasks.models import List, Section, Task


class SectionAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.task_list = List.objects.create(name="Main", emoji="", position=10)

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_create_section(self):
        response = self.client.post(
            f"/api/lists/{self.task_list.id}/sections/",
            data=json.dumps({"name": "Todo", "emoji": "T"}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], "Todo")
        self.assertTrue(Section.objects.filter(list=self.task_list, name="Todo").exists())

    def test_update_section(self):
        section = Section.objects.create(list=self.task_list, name="Old", emoji="", position=10)

        response = self.client.put(
            f"/api/sections/{section.id}/",
            data=json.dumps({"name": "New", "emoji": "N"}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 200)
        section.refresh_from_db()
        self.assertEqual(section.name, "New")
        self.assertEqual(section.emoji, "N")

    def test_delete_section_cascades_tasks(self):
        section = Section.objects.create(list=self.task_list, name="Todo", emoji="", position=10)
        task = Task.objects.create(section=section, title="Task", position=10)

        response = self.client.delete(
            f"/api/sections/{section.id}/",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Section.objects.filter(pk=section.id).exists())
        self.assertFalse(Task.objects.filter(pk=task.id).exists())

    def test_move_section_reorders_within_list(self):
        first = Section.objects.create(list=self.task_list, name="A", emoji="", position=10)
        second = Section.objects.create(list=self.task_list, name="B", emoji="", position=20)
        third = Section.objects.create(list=self.task_list, name="C", emoji="", position=30)

        response = self.client.patch(
            f"/api/sections/{third.id}/move/",
            data=json.dumps({"position": 0}),
            content_type="application/json",
            **self._headers(),
        )

        self.assertEqual(response.status_code, 200)
        ids = list(self.task_list.sections.order_by("position").values_list("id", flat=True))
        self.assertEqual(ids, [third.id, first.id, second.id])
