import json

from django.test import Client, TestCase

from network.models import Organization, OrgType


class OrganizationDuplicateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.org_type = OrgType.objects.create(name="Company")
        self.org = Organization.objects.create(
            name="Acme Corp",
            org_type=self.org_type,
        )

    def _get_csrf_token(self):
        resp = self.client.get("/api/health/")
        return resp.cookies["csrftoken"].value

    def test_create_duplicate_organization_returns_409(self):
        token = self._get_csrf_token()
        resp = self.client.post(
            "/api/organizations/",
            data=json.dumps({
                "name": "acme corp",
                "org_type_id": self.org_type.id,
            }),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(resp.status_code, 409)
        data = json.loads(resp.content)
        self.assertIn("already exists", data["detail"])

    def test_create_unique_organization_returns_201(self):
        token = self._get_csrf_token()
        resp = self.client.post(
            "/api/organizations/",
            data=json.dumps({
                "name": "New Corp",
                "org_type_id": self.org_type.id,
            }),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(resp.status_code, 201)
