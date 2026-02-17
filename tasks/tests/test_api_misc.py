import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from tasks.models import List, Section, Tag, Task


class MiscAPITests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value
        self.task_list = List.objects.create(name="Main", emoji="M", position=10)
        self.section = Section.objects.create(list=self.task_list, name="Todo", emoji="", position=10)
        self.task = Task.objects.create(section=self.section, title="Find urgent issue", notes="note body", position=10)

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_tags_endpoints(self):
        add_response = self.client.post(
            f"/api/tasks/{self.task.id}/tags/",
            data=json.dumps({"name": "urgent"}),
            content_type="application/json",
            **self._headers(),
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.json()[0]["name"], "urgent")

        tag = Tag.objects.get(name="urgent")
        list_response = self.client.get(f"/api/tags/?exclude_task={self.task.id}")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.json(), [])

        remove_response = self.client.delete(
            f"/api/tasks/{self.task.id}/tags/{tag.id}/",
            **self._headers(),
        )
        self.assertEqual(remove_response.status_code, 204)

    def test_search_endpoint(self):
        tag = Tag.objects.create(name="urgent")
        self.task.tags.add(tag)

        response = self.client.get("/api/search/?q=urgent")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_count"], 1)
        self.assertEqual(data["results"][0]["list"]["id"], self.task_list.id)
        self.assertEqual(data["results"][0]["tasks"][0]["id"], self.task.id)

    def test_export_endpoints(self):
        json_response = self.client.get("/api/export/json/")
        self.assertEqual(json_response.status_code, 200)
        self.assertEqual(json_response["Content-Type"], "application/json")
        self.assertIn("attachment;", json_response["Content-Disposition"])

        markdown_response = self.client.get(f"/api/export/{self.task_list.id}/markdown/")
        self.assertEqual(markdown_response.status_code, 200)
        self.assertIn("attachment;", markdown_response["Content-Disposition"])

        bad_format_response = self.client.get("/api/export/xml/")
        self.assertEqual(bad_format_response.status_code, 400)

    def test_import_endpoint_and_duplicate_skip(self):
        csv_content = (
            "Title,taskId,List Name,Column Name,Content,Priority,Status,Due Date,Is All Day,Created Time,Completed Time,Tags,parentId\n"
            "Imported Task,ext-1,Imported,Inbox,Body,0,0,,,,,work,\n"
        )
        upload = SimpleUploadedFile("tasks.csv", csv_content.encode("utf-8"), content_type="text/csv")

        first_response = self.client.post("/api/import/", {"csv_file": upload}, **self._headers())
        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(first_response.json()["tasks_created"], 1)

        upload_again = SimpleUploadedFile("tasks.csv", csv_content.encode("utf-8"), content_type="text/csv")
        second_response = self.client.post("/api/import/", {"csv_file": upload_again}, **self._headers())
        self.assertEqual(second_response.status_code, 200)
        self.assertGreaterEqual(second_response.json()["tasks_skipped"], 1)
