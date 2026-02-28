import json
from datetime import date, timedelta

from django.test import Client, TestCase
from django.utils import timezone

from network.models import InteractionType, Person
from network.models.interaction import Interaction
from tasks.models import List, Section, Task


class DashboardTrendsAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_trends_returns_13_weeks_of_data(self):
        response = self.client.get("/api/dashboard/trends/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["interactions_per_week"]), 13)
        self.assertEqual(len(data["tasks_completed_per_week"]), 13)

    def test_trends_zero_fills_empty_weeks(self):
        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        for entry in data["interactions_per_week"]:
            self.assertEqual(entry["count"], 0)
        for entry in data["tasks_completed_per_week"]:
            self.assertEqual(entry["count"], 0)

    def test_trends_counts_interactions_per_week(self):
        itype = InteractionType.objects.create(name="Call")
        today = timezone.now().date()
        Interaction.objects.create(interaction_type=itype, date=today)
        Interaction.objects.create(interaction_type=itype, date=today - timedelta(days=1))

        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        total = sum(w["count"] for w in data["interactions_per_week"])
        self.assertEqual(total, 2)

    def test_trends_counts_tasks_completed_per_week(self):
        lst = List.objects.create(name="Test")
        sec = Section.objects.create(list=lst, name="Default")
        task = Task.objects.create(section=sec, title="Done task")
        task.complete()

        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        total = sum(w["count"] for w in data["tasks_completed_per_week"])
        self.assertEqual(total, 1)

    def test_trends_compliance_no_people(self):
        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        self.assertEqual(data["follow_up_compliance"]["on_track"], 0)
        self.assertEqual(data["follow_up_compliance"]["total"], 0)
        self.assertEqual(data["follow_up_compliance"]["overdue_count"], 0)

    def test_trends_compliance_on_track(self):
        itype = InteractionType.objects.create(name="DM")
        person = Person.objects.create(
            first_name="Ada", last_name="Lovelace", follow_up_cadence_days=30
        )
        interaction = Interaction.objects.create(
            interaction_type=itype, date=timezone.now().date()
        )
        interaction.people.add(person)

        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        self.assertEqual(data["follow_up_compliance"]["on_track"], 1)
        self.assertEqual(data["follow_up_compliance"]["total"], 1)
        self.assertEqual(data["follow_up_compliance"]["overdue_count"], 0)

    def test_trends_compliance_overdue(self):
        itype = InteractionType.objects.create(name="DM")
        person = Person.objects.create(
            first_name="Ada", last_name="Lovelace", follow_up_cadence_days=7
        )
        old_date = timezone.now().date() - timedelta(days=20)
        interaction = Interaction.objects.create(
            interaction_type=itype, date=old_date
        )
        interaction.people.add(person)

        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        self.assertEqual(data["follow_up_compliance"]["on_track"], 0)
        self.assertEqual(data["follow_up_compliance"]["total"], 1)
        self.assertEqual(data["follow_up_compliance"]["overdue_count"], 1)

    def test_trends_compliance_person_no_interactions(self):
        Person.objects.create(
            first_name="Ada", last_name="Lovelace", follow_up_cadence_days=14
        )

        response = self.client.get("/api/dashboard/trends/")
        data = response.json()
        self.assertEqual(data["follow_up_compliance"]["overdue_count"], 1)
        self.assertEqual(data["follow_up_compliance"]["total"], 1)


class DashboardFollowUpsDueAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_empty_when_no_people(self):
        response = self.client.get("/api/dashboard/follow-ups-due/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_excludes_people_without_cadence(self):
        Person.objects.create(first_name="Ada", last_name="Lovelace")
        response = self.client.get("/api/dashboard/follow-ups-due/")
        self.assertEqual(response.json(), [])

    def test_returns_overdue_person(self):
        itype = InteractionType.objects.create(name="DM")
        person = Person.objects.create(
            first_name="Ada", last_name="Lovelace", follow_up_cadence_days=7
        )
        old_date = timezone.now().date() - timedelta(days=20)
        interaction = Interaction.objects.create(
            interaction_type=itype, date=old_date
        )
        interaction.people.add(person)

        response = self.client.get("/api/dashboard/follow-ups-due/")
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["person_id"], person.id)
        self.assertEqual(data[0]["first_name"], "Ada")
        self.assertEqual(data[0]["days_overdue"], 13)

    def test_excludes_on_track_person(self):
        itype = InteractionType.objects.create(name="DM")
        person = Person.objects.create(
            first_name="Ada", last_name="Lovelace", follow_up_cadence_days=30
        )
        interaction = Interaction.objects.create(
            interaction_type=itype, date=timezone.now().date()
        )
        interaction.people.add(person)

        response = self.client.get("/api/dashboard/follow-ups-due/")
        self.assertEqual(response.json(), [])

    def test_person_no_interactions_is_overdue(self):
        person = Person.objects.create(
            first_name="Ada", last_name="Lovelace", follow_up_cadence_days=1
        )
        # Backdate created_at so the person is past their cadence
        Person.objects.filter(pk=person.pk).update(
            created_at=timezone.now() - timedelta(days=5)
        )

        response = self.client.get("/api/dashboard/follow-ups-due/")
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIsNone(data[0]["last_interaction_date"])

    def test_sorted_by_days_overdue_descending(self):
        itype = InteractionType.objects.create(name="DM")
        p1 = Person.objects.create(
            first_name="Alice", last_name="A", follow_up_cadence_days=7
        )
        p2 = Person.objects.create(
            first_name="Bob", last_name="B", follow_up_cadence_days=7
        )

        i1 = Interaction.objects.create(
            interaction_type=itype, date=timezone.now().date() - timedelta(days=10)
        )
        i1.people.add(p1)

        i2 = Interaction.objects.create(
            interaction_type=itype, date=timezone.now().date() - timedelta(days=20)
        )
        i2.people.add(p2)

        response = self.client.get("/api/dashboard/follow-ups-due/")
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["first_name"], "Bob")  # more overdue
        self.assertEqual(data[1]["first_name"], "Alice")
