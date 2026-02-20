import json

from django.test import Client, TestCase

from network.models import (
    Interaction,
    InteractionType,
    OrgType,
    Organization,
    Person,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
    TaskOrganization,
    TaskPerson,
)
from tasks.models import List, Section, Task


class NetworkAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_network_entity_crud(self):
        org_type_response = self.client.post(
            "/api/org-types/",
            data=json.dumps({"name": "Company"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(org_type_response.status_code, 201)
        org_type_id = org_type_response.json()["id"]

        interaction_type_response = self.client.post(
            "/api/interaction-types/",
            data=json.dumps({"name": "Call"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(interaction_type_response.status_code, 201)
        interaction_type_id = interaction_type_response.json()["id"]

        person_response = self.client.post(
            "/api/people/",
            data=json.dumps({"first_name": "Ada", "last_name": "Lovelace"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(person_response.status_code, 201)
        person_id = person_response.json()["id"]

        organization_response = self.client.post(
            "/api/organizations/",
            data=json.dumps({"name": "Analytical Engine", "org_type_id": org_type_id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(organization_response.status_code, 201)
        organization_id = organization_response.json()["id"]

        interaction_response = self.client.post(
            "/api/interactions/",
            data=json.dumps(
                {
                    "person_id": person_id,
                    "interaction_type_id": interaction_type_id,
                    "date": "2026-02-18",
                }
            ),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(interaction_response.status_code, 201)

        list_people = self.client.get("/api/people/")
        self.assertEqual(list_people.status_code, 200)
        self.assertEqual(list_people.json()[0]["id"], person_id)

        list_orgs = self.client.get("/api/organizations/")
        self.assertEqual(list_orgs.status_code, 200)
        self.assertEqual(list_orgs.json()[0]["id"], organization_id)

        self.assertTrue(Person.objects.filter(pk=person_id).exists())
        self.assertTrue(Organization.objects.filter(pk=organization_id).exists())
        self.assertTrue(InteractionType.objects.filter(pk=interaction_type_id).exists())
        self.assertTrue(OrgType.objects.filter(pk=org_type_id).exists())

    def test_relationships_and_task_links(self):
        org_type = OrgType.objects.create(name="Company")
        interaction_type = InteractionType.objects.create(name="Email")
        person_a = Person.objects.create(first_name="Ada", middle_name="", last_name="Lovelace")
        person_b = Person.objects.create(first_name="Alan", middle_name="", last_name="Turing")
        organization = Organization.objects.create(name="Bletchley", org_type=org_type)
        interaction = Interaction.objects.create(
            person=person_a,
            interaction_type=interaction_type,
            date="2026-02-18",
            notes="",
        )

        list_obj = List.objects.create(name="Work", emoji="", position=10)
        section = Section.objects.create(list=list_obj, name="Todo", emoji="", position=10)
        task = Task.objects.create(section=section, title="Follow up", position=10)

        person_rel_response = self.client.post(
            "/api/relationships/people/",
            data=json.dumps({"person_1_id": person_a.id, "person_2_id": person_b.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(person_rel_response.status_code, 201)

        org_rel_response = self.client.post(
            "/api/relationships/organizations/",
            data=json.dumps({"organization_id": organization.id, "person_id": person_a.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(org_rel_response.status_code, 201)

        link_person = self.client.post(
            f"/api/tasks/{task.id}/people/",
            data=json.dumps({"id": person_a.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertIn(link_person.status_code, (200, 201))

        link_org = self.client.post(
            f"/api/tasks/{task.id}/organizations/",
            data=json.dumps({"id": organization.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertIn(link_org.status_code, (200, 201))

        link_interaction = self.client.post(
            f"/api/interactions/{interaction.id}/tasks/",
            data=json.dumps({"id": task.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertIn(link_interaction.status_code, (200, 201))

        self.assertTrue(RelationshipPersonPerson.objects.exists())
        self.assertTrue(RelationshipOrganizationPerson.objects.exists())
        self.assertTrue(TaskPerson.objects.filter(task=task, person=person_a).exists())
        self.assertTrue(TaskOrganization.objects.filter(task=task, organization=organization).exists())
