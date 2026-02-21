from datetime import date, time

from django.test import Client, TestCase

from tasks.models import List, Section, Tag, Task


class UpcomingAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_a = List.objects.create(name="Work", emoji="💼", position=10)
        self.section_a = Section.objects.create(
            list=self.list_a, name="Sprint", emoji="", position=10
        )
        self.list_b = List.objects.create(name="Personal", emoji="🏠", position=20)
        self.section_b = Section.objects.create(
            list=self.list_b, name="Errands", emoji="", position=10
        )

    def test_returns_tasks_with_due_dates_sorted(self):
        Task.objects.create(
            section=self.section_a, title="Later", position=10,
            due_date=date(2026, 3, 15),
        )
        Task.objects.create(
            section=self.section_b, title="Sooner", position=10,
            due_date=date(2026, 2, 20),
        )

        response = self.client.get("/api/upcoming/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Sooner")
        self.assertEqual(data[1]["title"], "Later")

    def test_excludes_completed_tasks(self):
        Task.objects.create(
            section=self.section_a, title="Done", position=10,
            due_date=date(2026, 3, 1), is_completed=True,
        )
        Task.objects.create(
            section=self.section_a, title="Open", position=20,
            due_date=date(2026, 3, 2),
        )

        response = self.client.get("/api/upcoming/")

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Open")

    def test_excludes_tasks_without_due_date(self):
        Task.objects.create(
            section=self.section_a, title="No date", position=10,
        )
        Task.objects.create(
            section=self.section_a, title="Has date", position=20,
            due_date=date(2026, 4, 1),
        )

        response = self.client.get("/api/upcoming/")

        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Has date")

    def test_returns_empty_array_when_no_matches(self):
        Task.objects.create(
            section=self.section_a, title="No date", position=10,
        )

        response = self.client.get("/api/upcoming/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_includes_list_and_section_context(self):
        Task.objects.create(
            section=self.section_a, title="Task", position=10,
            due_date=date(2026, 3, 1),
        )

        response = self.client.get("/api/upcoming/")

        data = response.json()[0]
        self.assertEqual(data["list_id"], self.list_a.id)
        self.assertEqual(data["list_name"], "Work")
        self.assertEqual(data["list_emoji"], "💼")
        self.assertEqual(data["section_id"], self.section_a.id)
        self.assertEqual(data["section_name"], "Sprint")

    def test_includes_tags(self):
        task = Task.objects.create(
            section=self.section_a, title="Tagged", position=10,
            due_date=date(2026, 3, 1),
        )
        tag = Tag.objects.create(name="urgent")
        task.tags.add(tag)

        response = self.client.get("/api/upcoming/")

        data = response.json()[0]
        self.assertEqual(data["tags"], ["urgent"])

    def test_null_due_time_sorts_after_non_null(self):
        Task.objects.create(
            section=self.section_a, title="No time", position=10,
            due_date=date(2026, 3, 1),
        )
        Task.objects.create(
            section=self.section_a, title="Has time", position=20,
            due_date=date(2026, 3, 1), due_time=time(9, 0),
        )

        response = self.client.get("/api/upcoming/")

        data = response.json()
        self.assertEqual(data[0]["title"], "Has time")
        self.assertEqual(data[1]["title"], "No time")
