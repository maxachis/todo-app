import json
from datetime import date

from django.test import Client, TestCase

from network.models import Interaction, InteractionType, Person


class PeopleLastInteractionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            follow_up_cadence_days=14,
        )
        self.dm_type = InteractionType.objects.create(name="DM")
        self.email_type = InteractionType.objects.create(name="Email")

    def _get_person(self, person_id):
        resp = self.client.get(f"/api/people/{person_id}/")
        self.assertEqual(resp.status_code, 200)
        return json.loads(resp.content)

    def _list_people(self):
        resp = self.client.get("/api/people/")
        self.assertEqual(resp.status_code, 200)
        return json.loads(resp.content)

    def test_person_with_no_interactions_returns_null(self):
        data = self._get_person(self.person.id)
        self.assertIsNone(data["last_interaction_date"])
        self.assertIsNone(data["last_interaction_type"])

    def test_person_with_interactions_returns_most_recent(self):
        Interaction.objects.create(
            person=self.person,
            interaction_type=self.email_type,
            date=date(2026, 1, 10),
        )
        Interaction.objects.create(
            person=self.person,
            interaction_type=self.dm_type,
            date=date(2026, 1, 20),
        )
        data = self._get_person(self.person.id)
        self.assertEqual(data["last_interaction_date"], "2026-01-20")
        self.assertEqual(data["last_interaction_type"], "DM")

    def test_list_includes_last_interaction_fields(self):
        Interaction.objects.create(
            person=self.person,
            interaction_type=self.dm_type,
            date=date(2026, 1, 15),
        )
        people = self._list_people()
        alice = next(p for p in people if p["id"] == self.person.id)
        self.assertEqual(alice["last_interaction_date"], "2026-01-15")
        self.assertEqual(alice["last_interaction_type"], "DM")

    def test_list_person_with_no_interactions(self):
        other = Person.objects.create(first_name="Bob", last_name="Jones")
        people = self._list_people()
        bob = next(p for p in people if p["id"] == other.id)
        self.assertIsNone(bob["last_interaction_date"])
        self.assertIsNone(bob["last_interaction_type"])

    def test_create_person_returns_null_interaction_fields(self):
        resp = self.client.get("/api/health/")
        token = resp.cookies["csrftoken"].value
        resp = self.client.post(
            "/api/people/",
            data=json.dumps({"first_name": "New", "last_name": "Person"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertIsNone(data["last_interaction_date"])
        self.assertIsNone(data["last_interaction_type"])

    def test_create_duplicate_person_returns_409(self):
        resp = self.client.get("/api/health/")
        token = resp.cookies["csrftoken"].value
        resp = self.client.post(
            "/api/people/",
            data=json.dumps({"first_name": "alice", "last_name": "SMITH"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.content)
        self.assertIn("already exists", data["detail"])

    def test_create_unique_person_returns_201(self):
        resp = self.client.get("/api/health/")
        token = resp.cookies["csrftoken"].value
        resp = self.client.post(
            "/api/people/",
            data=json.dumps({"first_name": "Bob", "last_name": "Jones"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(resp.status_code, 201)

    def test_update_person_returns_interaction_fields(self):
        Interaction.objects.create(
            person=self.person,
            interaction_type=self.dm_type,
            date=date(2026, 2, 1),
        )
        resp = self.client.get("/api/health/")
        token = resp.cookies["csrftoken"].value
        resp = self.client.put(
            f"/api/people/{self.person.id}/",
            data=json.dumps({"notes": "updated"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data["last_interaction_date"], "2026-02-01")
        self.assertEqual(data["last_interaction_type"], "DM")
