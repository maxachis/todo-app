import json

from django.test import Client, TestCase

from network.models import Interaction, InteractionPageLink, InteractionType, Person
from notebook.mentions import parse_mentions, reconcile_mentions
from notebook.models import Page, PageEntityMention


class InteractionPageLinkTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(first_name="Jane", last_name="Doe")
        self.interaction_type = InteractionType.objects.create(name="Meeting")
        self.interaction = Interaction.objects.create(
            interaction_type=self.interaction_type,
            date="2026-03-13",
        )
        self.interaction.people.add(self.person)
        self.page = Page.objects.create(
            title="Meeting Notes",
            content="Some notes here",
            page_type="wiki",
        )

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

    def _delete(self, url):
        token = self._get_csrf_token()
        return self.client.delete(url, HTTP_X_CSRFTOKEN=token)

    def test_list_empty(self):
        resp = self.client.get(f"/api/interactions/{self.interaction.id}/pages/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_add_page_link(self):
        resp = self._post(
            f"/api/interactions/{self.interaction.id}/pages/",
            {"id": self.page.id},
        )
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["id"], self.page.id)
        self.assertEqual(data["title"], "Meeting Notes")
        self.assertEqual(data["slug"], self.page.slug)

    def test_add_duplicate_returns_200(self):
        InteractionPageLink.objects.create(
            interaction=self.interaction, page=self.page
        )
        resp = self._post(
            f"/api/interactions/{self.interaction.id}/pages/",
            {"id": self.page.id},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(InteractionPageLink.objects.count(), 1)

    def test_list_after_add(self):
        InteractionPageLink.objects.create(
            interaction=self.interaction, page=self.page
        )
        resp = self.client.get(f"/api/interactions/{self.interaction.id}/pages/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Meeting Notes")

    def test_delete_link(self):
        InteractionPageLink.objects.create(
            interaction=self.interaction, page=self.page
        )
        resp = self._delete(
            f"/api/interactions/{self.interaction.id}/pages/{self.page.id}/"
        )
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(InteractionPageLink.objects.count(), 0)

    def test_cascade_delete_interaction(self):
        InteractionPageLink.objects.create(
            interaction=self.interaction, page=self.page
        )
        self.interaction.delete()
        self.assertEqual(InteractionPageLink.objects.count(), 0)

    def test_cascade_delete_page(self):
        InteractionPageLink.objects.create(
            interaction=self.interaction, page=self.page
        )
        self.page.delete()
        self.assertEqual(InteractionPageLink.objects.count(), 0)


class PageInteractionsEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(first_name="Jane", last_name="Doe")
        self.interaction_type = InteractionType.objects.create(name="Call")
        self.interaction = Interaction.objects.create(
            interaction_type=self.interaction_type,
            date="2026-03-13",
        )
        self.interaction.people.add(self.person)
        self.page = Page.objects.create(
            title="Test Page",
            content="test",
            page_type="wiki",
        )

    def test_page_interactions_empty(self):
        resp = self.client.get(f"/api/notebook/pages/{self.page.slug}/interactions/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_page_interactions_returns_linked(self):
        InteractionPageLink.objects.create(
            interaction=self.interaction, page=self.page
        )
        resp = self.client.get(f"/api/notebook/pages/{self.page.slug}/interactions/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.interaction.id)
        self.assertEqual(data[0]["interaction_type_name"], "Call")
        self.assertEqual(data[0]["date"], "2026-03-13")
        self.assertEqual(data[0]["person_names"], ["Jane Doe"])


class InteractionMentionParserTests(TestCase):
    def test_parse_interaction_mention(self):
        content = "Discussed in [[interaction:42|Meeting with John (2026-03-13)]]"
        mentions, page_ids = parse_mentions(content)
        self.assertIn(("interaction", 42), mentions)
        self.assertEqual(page_ids, set())

    def test_reconcile_creates_mention_record(self):
        page = Page.objects.create(
            title="Test",
            content="See [[interaction:99|Call with Jane]]",
            page_type="wiki",
        )
        reconcile_mentions(page, process_checkboxes=False)
        self.assertTrue(
            PageEntityMention.objects.filter(
                page=page, entity_type="interaction", entity_id=99
            ).exists()
        )

    def test_reconcile_removes_stale_mention(self):
        page = Page.objects.create(
            title="Test",
            content="See [[interaction:99|Call]]",
            page_type="wiki",
        )
        reconcile_mentions(page, process_checkboxes=False)
        # Now update content to remove the mention
        page.content = "No mentions here"
        page.save()
        reconcile_mentions(page, process_checkboxes=False)
        self.assertFalse(
            PageEntityMention.objects.filter(
                page=page, entity_type="interaction"
            ).exists()
        )
