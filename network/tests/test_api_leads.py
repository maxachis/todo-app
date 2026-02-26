import json

from django.test import Client, TestCase

from network.models import Lead, LeadTask, Organization, OrgType, Person
from tasks.models import List as TaskList, Section, Task


class LeadCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(first_name="Alice", last_name="Smith")
        self.org_type = OrgType.objects.create(name="Company")
        self.org = Organization.objects.create(name="Acme Corp", org_type=self.org_type)
        # Get CSRF token
        resp = self.client.get("/api/health/")
        self.token = resp.cookies["csrftoken"].value

    def _post(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token,
        )

    def _put(self, url, data):
        return self.client.put(
            url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token,
        )

    def _delete(self, url):
        return self.client.delete(url, HTTP_X_CSRFTOKEN=self.token)

    def test_create_lead_with_person(self):
        resp = self._post("/api/leads/", {"title": "New deal", "person_id": self.person.id})
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data["title"], "New deal")
        self.assertEqual(data["status"], "prospect")
        self.assertEqual(data["person_id"], self.person.id)
        self.assertIsNone(data["organization_id"])
        self.assertEqual(data["person_name"], "Alice Smith")
        self.assertIsNone(data["organization_name"])

    def test_create_lead_with_org(self):
        resp = self._post("/api/leads/", {"title": "Org deal", "organization_id": self.org.id})
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data["organization_id"], self.org.id)
        self.assertIsNone(data["person_id"])
        self.assertEqual(data["organization_name"], "Acme Corp")

    def test_create_lead_with_both(self):
        resp = self._post(
            "/api/leads/",
            {"title": "Both deal", "person_id": self.person.id, "organization_id": self.org.id},
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data["person_id"], self.person.id)
        self.assertEqual(data["organization_id"], self.org.id)

    def test_create_lead_without_person_or_org_fails(self):
        resp = self._post("/api/leads/", {"title": "Orphan deal"})
        self.assertEqual(resp.status_code, 422)

    def test_create_lead_blank_title_fails(self):
        resp = self._post("/api/leads/", {"title": "  ", "person_id": self.person.id})
        self.assertEqual(resp.status_code, 422)

    def test_create_lead_default_status(self):
        resp = self._post("/api/leads/", {"title": "Default", "person_id": self.person.id})
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data["status"], "prospect")

    def test_create_lead_with_status(self):
        resp = self._post(
            "/api/leads/",
            {"title": "Committed", "status": "committed", "person_id": self.person.id},
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data["status"], "committed")

    def test_list_leads(self):
        Lead.objects.create(title="Lead 1", person=self.person)
        Lead.objects.create(title="Lead 2", organization=self.org)
        resp = self.client.get("/api/leads/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data), 2)

    def test_get_lead(self):
        lead = Lead.objects.create(title="Detail", person=self.person)
        resp = self.client.get(f"/api/leads/{lead.id}/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data["title"], "Detail")
        self.assertEqual(data["person_name"], "Alice Smith")

    def test_update_lead(self):
        lead = Lead.objects.create(title="Old", person=self.person)
        resp = self._put(f"/api/leads/{lead.id}/", {"title": "New", "status": "fulfilled"})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data["title"], "New")
        self.assertEqual(data["status"], "fulfilled")

    def test_update_lead_partial(self):
        lead = Lead.objects.create(title="Keep", status="interested", person=self.person)
        resp = self._put(f"/api/leads/{lead.id}/", {"notes": "some notes"})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data["title"], "Keep")
        self.assertEqual(data["status"], "interested")
        self.assertEqual(data["notes"], "some notes")

    def test_delete_lead(self):
        lead = Lead.objects.create(title="Bye", person=self.person)
        resp = self._delete(f"/api/leads/{lead.id}/")
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Lead.objects.filter(pk=lead.id).exists())


class LeadTaskLinkTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(first_name="Bob", last_name="Jones")
        self.lead = Lead.objects.create(title="Test Lead", person=self.person)
        task_list = TaskList.objects.create(name="Test List")
        section = Section.objects.create(name="Default", list=task_list)
        self.task = Task.objects.create(title="Task 1", section=section)
        self.task2 = Task.objects.create(title="Task 2", section=section)
        resp = self.client.get("/api/health/")
        self.token = resp.cookies["csrftoken"].value

    def _post(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token,
        )

    def _delete(self, url):
        return self.client.delete(url, HTTP_X_CSRFTOKEN=self.token)

    def test_link_task_to_lead(self):
        resp = self._post(f"/api/leads/{self.lead.id}/tasks/", {"id": self.task.id})
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data["lead_id"], self.lead.id)
        self.assertEqual(data["task_id"], self.task.id)

    def test_list_lead_tasks(self):
        LeadTask.objects.create(lead=self.lead, task=self.task)
        LeadTask.objects.create(lead=self.lead, task=self.task2)
        resp = self.client.get(f"/api/leads/{self.lead.id}/tasks/")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data), 2)

    def test_duplicate_link_returns_200(self):
        LeadTask.objects.create(lead=self.lead, task=self.task)
        resp = self._post(f"/api/leads/{self.lead.id}/tasks/", {"id": self.task.id})
        self.assertEqual(resp.status_code, 200)

    def test_unlink_task_from_lead(self):
        LeadTask.objects.create(lead=self.lead, task=self.task)
        resp = self._delete(f"/api/leads/{self.lead.id}/tasks/{self.task.id}/")
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(LeadTask.objects.filter(lead=self.lead, task=self.task).exists())

    def test_delete_lead_cascades_links(self):
        LeadTask.objects.create(lead=self.lead, task=self.task)
        self.lead.delete()
        self.assertEqual(LeadTask.objects.count(), 0)
