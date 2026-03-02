import json

from django.test import Client, TestCase

from network.models import ContactDraft, Organization, OrgType, Person
from notebook.models import Page


class ContactDraftParserTests(TestCase):
    """Tests for @new[Name](notes) parser in reconcile_mentions."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def _create_page(self, title, content):
        return self.client.post(
            "/api/notebook/pages/",
            data=json.dumps({"title": title, "content": content}),
            content_type="application/json",
            **self._headers(),
        )

    def _update_page(self, slug, content):
        return self.client.put(
            f"/api/notebook/pages/{slug}/",
            data=json.dumps({"content": content}),
            content_type="application/json",
            **self._headers(),
        )

    def test_single_new_creates_draft(self):
        self._create_page("Test", "Met @new[Jane Smith](works at Stripe)")
        drafts = ContactDraft.objects.filter(name="Jane Smith")
        self.assertEqual(drafts.count(), 1)
        self.assertEqual(drafts.first().quick_notes, "works at Stripe")

    def test_multiple_new_creates_multiple_drafts(self):
        self._create_page(
            "Multi",
            "@new[Jane Smith](notes1) and @new[Bob Chen](notes2)",
        )
        self.assertEqual(ContactDraft.objects.count(), 2)
        self.assertTrue(ContactDraft.objects.filter(name="Jane Smith").exists())
        self.assertTrue(ContactDraft.objects.filter(name="Bob Chen").exists())

    def test_new_without_notes(self):
        self._create_page("NoNotes", "Talked to @new[Alice Brown]")
        draft = ContactDraft.objects.get(name="Alice Brown")
        self.assertEqual(draft.quick_notes, "")

    def test_idempotent_resave(self):
        self._create_page("Idem", "Met @new[Jane Smith](notes)")
        self.assertEqual(ContactDraft.objects.filter(name="Jane Smith").count(), 1)
        # Re-save same content
        self._update_page("idem", "Met @new[Jane Smith](notes)")
        self.assertEqual(ContactDraft.objects.filter(name="Jane Smith").count(), 1)

    def test_same_name_different_pages(self):
        self._create_page("Page1", "@new[Jane Smith](context A)")
        self._create_page("Page2", "@new[Jane Smith](context B)")
        self.assertEqual(ContactDraft.objects.filter(name="Jane Smith").count(), 2)

    def test_content_not_rewritten_at_capture(self):
        self._create_page("NoRewrite", "@new[Jane Smith](notes)")
        page = Page.objects.get(slug="norewrite")
        self.assertIn("@new[Jane Smith](notes)", page.content)


class ContactDraftAPITests(TestCase):
    """Tests for ContactDraft CRUD and triage endpoints."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.page = Page.objects.create(
            title="Test Page", slug="test-page", content=""
        )
        self.draft = ContactDraft.objects.create(
            name="Jane Smith",
            quick_notes="works at Stripe",
            source_page=self.page,
        )

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_list_pending_drafts(self):
        resp = self.client.get("/api/contact-drafts/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Jane Smith")
        self.assertEqual(data[0]["source_page_slug"], "test-page")

    def test_dismissed_draft_excluded(self):
        self.draft.dismissed = True
        self.draft.save()
        resp = self.client.get("/api/contact-drafts/")
        self.assertEqual(resp.json(), [])

    def test_dismiss_endpoint(self):
        resp = self.client.post(
            f"/api/contact-drafts/{self.draft.id}/dismiss/",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 200)
        self.draft.refresh_from_db()
        self.assertTrue(self.draft.dismissed)

    def test_delete_endpoint(self):
        resp = self.client.delete(
            f"/api/contact-drafts/{self.draft.id}/",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(ContactDraft.objects.filter(pk=self.draft.id).exists())


class PromoteToPersonTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.page = Page.objects.create(
            title="Daily", slug="daily", content="Met @new[Jane Smith](at conf)"
        )
        self.draft = ContactDraft.objects.create(
            name="Jane Smith",
            quick_notes="at conf",
            source_page=self.page,
        )

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_promote_creates_person(self):
        resp = self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/person/",
            data=json.dumps({"first_name": "Jane", "last_name": "Smith"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 201)
        person = Person.objects.get(first_name="Jane", last_name="Smith")
        self.assertEqual(person.notes, "at conf")

    def test_promote_sets_fk(self):
        self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/person/",
            data=json.dumps({"first_name": "Jane", "last_name": "Smith"}),
            content_type="application/json",
            **self._headers(),
        )
        self.draft.refresh_from_db()
        self.assertIsNotNone(self.draft.promoted_to_person_id)

    def test_promote_rewrites_page(self):
        self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/person/",
            data=json.dumps({"first_name": "Jane", "last_name": "Smith"}),
            content_type="application/json",
            **self._headers(),
        )
        self.page.refresh_from_db()
        person = Person.objects.get(first_name="Jane", last_name="Smith")
        self.assertIn(f"@[person:{person.id}|Jane Smith]", self.page.content)
        self.assertNotIn("@new[", self.page.content)

    def test_promote_explicit_notes_override(self):
        resp = self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/person/",
            data=json.dumps({
                "first_name": "Jane",
                "last_name": "Smith",
                "notes": "Custom notes",
            }),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 201)
        person = Person.objects.get(first_name="Jane", last_name="Smith")
        self.assertEqual(person.notes, "Custom notes")

    def test_promote_duplicate_name_409(self):
        Person.objects.create(first_name="Jane", last_name="Smith")
        resp = self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/person/",
            data=json.dumps({"first_name": "Jane", "last_name": "Smith"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 409)


class PromoteToOrgTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.org_type = OrgType.objects.create(name="Company")
        self.page = Page.objects.create(
            title="Notes", slug="notes", content="About @new[Acme Corp](partner)"
        )
        self.draft = ContactDraft.objects.create(
            name="Acme Corp",
            quick_notes="partner",
            source_page=self.page,
        )

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_promote_creates_org(self):
        resp = self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/org/",
            data=json.dumps({"name": "Acme Corp", "org_type_id": self.org_type.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 201)
        org = Organization.objects.get(name="Acme Corp")
        self.assertEqual(org.notes, "partner")

    def test_promote_rewrites_page(self):
        self.client.post(
            f"/api/contact-drafts/{self.draft.id}/promote/org/",
            data=json.dumps({"name": "Acme Corp", "org_type_id": self.org_type.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.page.refresh_from_db()
        org = Organization.objects.get(name="Acme Corp")
        self.assertIn(f"[[org:{org.id}|Acme Corp]]", self.page.content)
        self.assertNotIn("@new[", self.page.content)


class LinkToExistingTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.person = Person.objects.create(
            first_name="Jane", last_name="Smith", notes="Sales lead from 2025"
        )
        self.page = Page.objects.create(
            title="Link", slug="link", content="@new[Jane Smith](met at conf)"
        )
        self.draft = ContactDraft.objects.create(
            name="Jane Smith",
            quick_notes="met at conf",
            source_page=self.page,
        )

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_link_to_person(self):
        resp = self.client.post(
            f"/api/contact-drafts/{self.draft.id}/link/",
            data=json.dumps({"person_id": self.person.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(resp.status_code, 200)
        self.draft.refresh_from_db()
        self.assertEqual(self.draft.promoted_to_person_id, self.person.id)

    def test_link_appends_notes(self):
        self.client.post(
            f"/api/contact-drafts/{self.draft.id}/link/",
            data=json.dumps({"person_id": self.person.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.person.refresh_from_db()
        self.assertIn("Sales lead from 2025", self.person.notes)
        self.assertIn("met at conf", self.person.notes)
        self.assertIn("---", self.person.notes)

    def test_link_rewrites_page(self):
        self.client.post(
            f"/api/contact-drafts/{self.draft.id}/link/",
            data=json.dumps({"person_id": self.person.id}),
            content_type="application/json",
            **self._headers(),
        )
        self.page.refresh_from_db()
        self.assertIn(f"@[person:{self.person.id}|Jane Smith]", self.page.content)


class MatchHintsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(first_name="Jane", last_name="Smith")
        self.org_type = OrgType.objects.create(name="Company")
        self.org = Organization.objects.create(name="Acme Corp", org_type=self.org_type)
        self.draft_person = ContactDraft.objects.create(name="Jane Smith")
        self.draft_org = ContactDraft.objects.create(name="Acme Corp")
        self.draft_no_match = ContactDraft.objects.create(name="Completely Unknown")

    def test_exact_person_match(self):
        resp = self.client.get(f"/api/contact-drafts/{self.draft_person.id}/matches/")
        data = resp.json()
        person_ids = [p["id"] for p in data["people"]]
        self.assertIn(self.person.id, person_ids)

    def test_org_match(self):
        resp = self.client.get(f"/api/contact-drafts/{self.draft_org.id}/matches/")
        data = resp.json()
        org_ids = [o["id"] for o in data["organizations"]]
        self.assertIn(self.org.id, org_ids)

    def test_no_match(self):
        resp = self.client.get(f"/api/contact-drafts/{self.draft_no_match.id}/matches/")
        data = resp.json()
        self.assertEqual(data["people"], [])
        self.assertEqual(data["organizations"], [])


class AutoDismissTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.page1 = Page.objects.create(
            title="P1", slug="p1", content="@new[Jane Smith](ctx1)"
        )
        self.page2 = Page.objects.create(
            title="P2", slug="p2", content="@new[Jane Smith](ctx2)"
        )
        self.draft1 = ContactDraft.objects.create(
            name="Jane Smith", quick_notes="ctx1", source_page=self.page1
        )
        self.draft2 = ContactDraft.objects.create(
            name="Jane Smith", quick_notes="ctx2", source_page=self.page2
        )

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_sibling_dismissed_after_promotion(self):
        self.client.post(
            f"/api/contact-drafts/{self.draft1.id}/promote/person/",
            data=json.dumps({"first_name": "Jane", "last_name": "Smith"}),
            content_type="application/json",
            **self._headers(),
        )
        self.draft2.refresh_from_db()
        self.assertTrue(self.draft2.dismissed)


class NotebookRewriteTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_rewrite_multiple_pages(self):
        page1 = Page.objects.create(
            title="A", slug="a", content="@new[Jane Smith](n1)"
        )
        page2 = Page.objects.create(
            title="B", slug="b", content="Also @new[Jane Smith](n2)"
        )
        draft = ContactDraft.objects.create(
            name="Jane Smith", quick_notes="n1", source_page=page1
        )
        self.client.post(
            f"/api/contact-drafts/{draft.id}/promote/person/",
            data=json.dumps({"first_name": "Jane", "last_name": "Smith"}),
            content_type="application/json",
            **self._headers(),
        )
        page1.refresh_from_db()
        page2.refresh_from_db()
        person = Person.objects.get(first_name="Jane", last_name="Smith")
        self.assertIn(f"@[person:{person.id}|Jane Smith]", page1.content)
        self.assertIn(f"@[person:{person.id}|Jane Smith]", page2.content)

    def test_rewrite_regex_special_chars(self):
        page = Page.objects.create(
            title="Special", slug="special",
            content="@new[O'Brien (Jr.)](notes)"
        )
        draft = ContactDraft.objects.create(
            name="O'Brien (Jr.)", quick_notes="notes", source_page=page
        )
        self.client.post(
            f"/api/contact-drafts/{draft.id}/promote/person/",
            data=json.dumps({"first_name": "O'Brien", "last_name": "(Jr.)"}),
            content_type="application/json",
            **self._headers(),
        )
        page.refresh_from_db()
        person = Person.objects.get(first_name="O'Brien")
        self.assertIn(f"@[person:{person.id}|O'Brien (Jr.)]", page.content)
        self.assertNotIn("@new[", page.content)
