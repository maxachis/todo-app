import json

from django.test import Client, TestCase

from notebook.mentions import parse_mentions
from notebook.models import Page, PageEntityMention, PageLink


class PageCRUDTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def _post(self, data):
        return self.client.post(
            "/api/notebook/pages/",
            data=json.dumps(data),
            content_type="application/json",
            **self._headers(),
        )

    def _put(self, slug, data):
        return self.client.put(
            f"/api/notebook/pages/{slug}/",
            data=json.dumps(data),
            content_type="application/json",
            **self._headers(),
        )

    def test_create_wiki_page(self):
        resp = self._post({"title": "Migration Runbook", "content": "Some notes"})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["title"], "Migration Runbook")
        self.assertEqual(data["slug"], "migration-runbook")
        self.assertEqual(data["page_type"], "wiki")
        self.assertIsNone(data["date"])

    def test_create_daily_page(self):
        resp = self._post({"page_type": "daily", "date": "2026-02-28"})
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["title"], "2026-02-28")
        self.assertEqual(data["slug"], "2026-02-28")
        self.assertEqual(data["page_type"], "daily")
        self.assertEqual(data["date"], "2026-02-28")

    def test_get_or_create_daily_page(self):
        resp1 = self._post({"page_type": "daily", "date": "2026-02-28"})
        resp2 = self._post({"page_type": "daily", "date": "2026-02-28"})
        self.assertEqual(resp1.json()["id"], resp2.json()["id"])
        self.assertEqual(Page.objects.filter(page_type="daily", date="2026-02-28").count(), 1)

    def test_update_page(self):
        self._post({"title": "Test Page"})
        resp = self._put("test-page", {"content": "Updated content"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["content"], "Updated content")

    def test_delete_page(self):
        self._post({"title": "To Delete"})
        resp = self.client.delete("/api/notebook/pages/to-delete/", **self._headers())
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Page.objects.filter(slug="to-delete").exists())

    def test_get_page_by_slug(self):
        self._post({"title": "My Page", "content": "Hello"})
        resp = self.client.get("/api/notebook/pages/my-page/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["content"], "Hello")

    def test_slug_uniqueness(self):
        self._post({"title": "Duplicate"})
        self._post({"title": "Duplicate"})
        slugs = list(Page.objects.values_list("slug", flat=True))
        self.assertIn("duplicate", slugs)
        self.assertIn("duplicate-2", slugs)


class MentionParsingTests(TestCase):
    def test_parse_person_mention(self):
        mentions, pages = parse_mentions("Met @[person:7|John Smith] today")
        self.assertEqual(mentions, {("person", 7)})
        self.assertEqual(pages, set())

    def test_parse_task_mention(self):
        mentions, pages = parse_mentions("Working on [[task:189|Deploy fix]]")
        self.assertEqual(mentions, {("task", 189)})

    def test_parse_org_mention(self):
        mentions, pages = parse_mentions("Client [[org:3|Acme Corp]] signed")
        self.assertEqual(mentions, {("organization", 3)})

    def test_parse_project_mention(self):
        mentions, pages = parse_mentions("For [[project:5|Alpha]]")
        self.assertEqual(mentions, {("project", 5)})

    def test_parse_page_link(self):
        mentions, pages = parse_mentions("See [[page:12|Runbook]]")
        self.assertEqual(mentions, set())
        self.assertEqual(pages, {12})

    def test_parse_multiple_mentions(self):
        content = "@[person:1|A] and @[person:2|B] about [[task:10|T]]"
        mentions, pages = parse_mentions(content)
        self.assertEqual(mentions, {("person", 1), ("person", 2), ("task", 10)})

    def test_duplicate_mentions(self):
        content = "@[person:7|John] and @[person:7|John] again"
        mentions, _ = parse_mentions(content)
        self.assertEqual(len(mentions), 1)

    def test_no_mentions(self):
        mentions, pages = parse_mentions("Plain text with no mentions")
        self.assertEqual(mentions, set())
        self.assertEqual(pages, set())


class MentionReconciliationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def _post(self, data):
        return self.client.post(
            "/api/notebook/pages/",
            data=json.dumps(data),
            content_type="application/json",
            **self._headers(),
        )

    def _put(self, slug, data):
        return self.client.put(
            f"/api/notebook/pages/{slug}/",
            data=json.dumps(data),
            content_type="application/json",
            **self._headers(),
        )

    def test_mentions_created_on_save(self):
        self._post({
            "title": "Test",
            "content": "Met @[person:7|John] about [[task:1|Fix]]",
        })
        page = Page.objects.get(slug="test")
        mentions = set(
            PageEntityMention.objects.filter(page=page).values_list("entity_type", "entity_id")
        )
        self.assertEqual(mentions, {("person", 7), ("task", 1)})

    def test_mentions_removed_on_update(self):
        self._post({
            "title": "Test",
            "content": "@[person:7|John] and @[person:8|Jane]",
        })
        self._put("test", {"content": "@[person:7|John] only"})
        page = Page.objects.get(slug="test")
        mentions = set(
            PageEntityMention.objects.filter(page=page).values_list("entity_type", "entity_id")
        )
        self.assertEqual(mentions, {("person", 7)})

    def test_page_links_created(self):
        p1 = Page.objects.create(title="Target", slug="target", content="")
        self._post({
            "title": "Source",
            "content": f"See [[page:{p1.id}|Target]]",
        })
        source = Page.objects.get(slug="source")
        self.assertTrue(PageLink.objects.filter(source_page=source, target_page=p1).exists())

    def test_page_links_removed_on_update(self):
        p1 = Page.objects.create(title="Target", slug="target", content="")
        self._post({
            "title": "Source",
            "content": f"See [[page:{p1.id}|Target]]",
        })
        self._put("source", {"content": "No more links"})
        source = Page.objects.get(slug="source")
        self.assertFalse(PageLink.objects.filter(source_page=source).exists())


class BacklinksAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_person_backlinks(self):
        self.client.post(
            "/api/notebook/pages/",
            data=json.dumps({"title": "A", "content": "@[person:7|John]"}),
            content_type="application/json",
            **self._headers(),
        )
        self.client.post(
            "/api/notebook/pages/",
            data=json.dumps({"title": "B", "content": "@[person:7|John] again"}),
            content_type="application/json",
            **self._headers(),
        )
        resp = self.client.get("/api/notebook/mentions/person/7/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)

    def test_task_backlinks(self):
        self.client.post(
            "/api/notebook/pages/",
            data=json.dumps({"title": "A", "content": "[[task:10|Fix]]"}),
            content_type="application/json",
            **self._headers(),
        )
        resp = self.client.get("/api/notebook/mentions/task/10/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_empty_backlinks(self):
        resp = self.client.get("/api/notebook/mentions/person/999/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])


class PageListFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        Page.objects.create(title="Wiki One", slug="wiki-one", page_type="wiki")
        Page.objects.create(title="2026-02-28", slug="2026-02-28", page_type="daily", date="2026-02-28")
        Page.objects.create(title="Migration Notes", slug="migration-notes", page_type="wiki")

    def test_filter_by_page_type_wiki(self):
        resp = self.client.get("/api/notebook/pages/?page_type=wiki")
        self.assertEqual(len(resp.json()), 2)

    def test_filter_by_page_type_daily(self):
        resp = self.client.get("/api/notebook/pages/?page_type=daily")
        self.assertEqual(len(resp.json()), 1)

    def test_search_by_title(self):
        resp = self.client.get("/api/notebook/pages/?search=migration")
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Migration Notes")

    def test_list_all(self):
        resp = self.client.get("/api/notebook/pages/")
        self.assertEqual(len(resp.json()), 3)
