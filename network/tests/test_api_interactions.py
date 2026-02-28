import json

from django.test import Client, TestCase

from network.models import Interaction, InteractionType, Organization, OrgType, Person


class InteractionOrganizationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(first_name="Jane", last_name="Doe")
        self.interaction_type = InteractionType.objects.create(name="Meeting")
        self.org_type = OrgType.objects.create(name="Company")
        self.org1 = Organization.objects.create(name="Acme Corp", org_type=self.org_type)
        self.org2 = Organization.objects.create(name="Globex", org_type=self.org_type)

    def _get_csrf_token(self):
        resp = self.client.get("/api/health/")
        return resp.cookies["csrftoken"].value

    def _post(self, url, data):
        token = self._get_csrf_token()
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

    def _put(self, url, data):
        token = self._get_csrf_token()
        return self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )

    def test_create_with_organization_ids(self):
        resp = self._post("/api/interactions/", {
            "person_ids": [self.person.id],
            "organization_ids": [self.org1.id, self.org2.id],
            "interaction_type_id": self.interaction_type.id,
            "date": "2026-02-28",
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertCountEqual(data["organization_ids"], [self.org1.id, self.org2.id])
        self.assertEqual(data["person_ids"], [self.person.id])

    def test_create_without_organization_ids(self):
        resp = self._post("/api/interactions/", {
            "person_ids": [self.person.id],
            "interaction_type_id": self.interaction_type.id,
            "date": "2026-02-28",
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["organization_ids"], [])

    def test_update_organization_ids(self):
        resp = self._post("/api/interactions/", {
            "person_ids": [self.person.id],
            "organization_ids": [self.org1.id],
            "interaction_type_id": self.interaction_type.id,
            "date": "2026-02-28",
        })
        interaction_id = resp.json()["id"]

        resp = self._put(f"/api/interactions/{interaction_id}/", {
            "organization_ids": [self.org2.id],
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["organization_ids"], [self.org2.id])

    def test_update_without_organization_ids_preserves_existing(self):
        resp = self._post("/api/interactions/", {
            "person_ids": [self.person.id],
            "organization_ids": [self.org1.id, self.org2.id],
            "interaction_type_id": self.interaction_type.id,
            "date": "2026-02-28",
        })
        interaction_id = resp.json()["id"]

        resp = self._put(f"/api/interactions/{interaction_id}/", {
            "notes": "Updated notes only",
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertCountEqual(data["organization_ids"], [self.org1.id, self.org2.id])
