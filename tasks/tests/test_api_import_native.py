import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from tasks.models import List, Section, Tag, Task


class NativeJSONImportTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def _upload_json(self, data):
        content = json.dumps(data).encode("utf-8")
        upload = SimpleUploadedFile("export.json", content, content_type="application/json")
        return self.client.post("/api/import/", {"file": upload}, **self._headers())

    def test_single_list_import(self):
        data = {
            "name": "Work",
            "emoji": "W",
            "position": 0,
            "sections": [
                {
                    "name": "Todo",
                    "emoji": "",
                    "position": 0,
                    "tasks": [
                        {
                            "title": "Write report",
                            "notes": "quarterly",
                            "due_date": "2026-03-01",
                            "is_completed": False,
                            "completed_at": None,
                            "position": 0,
                            "tags": ["work"],
                            "subtasks": [],
                        }
                    ],
                }
            ],
        }
        resp = self._upload_json(data)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["lists_created"], 1)
        self.assertEqual(body["sections_created"], 1)
        self.assertEqual(body["tasks_created"], 1)
        self.assertEqual(body["tags_created"], 1)
        self.assertTrue(List.objects.filter(name="Work").exists())
        task = Task.objects.get(title="Write report")
        self.assertEqual(str(task.due_date), "2026-03-01")
        self.assertTrue(task.tags.filter(name="work").exists())

    def test_multi_list_import(self):
        data = [
            {
                "name": "List A",
                "emoji": "",
                "position": 0,
                "sections": [
                    {"name": "Sec1", "emoji": "", "position": 0, "tasks": []},
                ],
            },
            {
                "name": "List B",
                "emoji": "",
                "position": 10,
                "sections": [
                    {"name": "Sec2", "emoji": "", "position": 0, "tasks": []},
                ],
            },
        ]
        resp = self._upload_json(data)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["lists_created"], 2)
        self.assertEqual(body["sections_created"], 2)

    def test_subtask_hierarchy(self):
        data = {
            "name": "Nested",
            "emoji": "",
            "position": 0,
            "sections": [
                {
                    "name": "Main",
                    "emoji": "",
                    "position": 0,
                    "tasks": [
                        {
                            "title": "Parent",
                            "notes": "",
                            "due_date": None,
                            "is_completed": False,
                            "completed_at": None,
                            "position": 0,
                            "tags": [],
                            "subtasks": [
                                {
                                    "title": "Child",
                                    "notes": "",
                                    "due_date": None,
                                    "is_completed": False,
                                    "completed_at": None,
                                    "position": 0,
                                    "tags": [],
                                    "subtasks": [
                                        {
                                            "title": "Grandchild",
                                            "notes": "",
                                            "due_date": None,
                                            "is_completed": False,
                                            "completed_at": None,
                                            "position": 0,
                                            "tags": [],
                                            "subtasks": [],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        resp = self._upload_json(data)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["tasks_created"], 3)
        self.assertEqual(body["parents_linked"], 2)

        parent = Task.objects.get(title="Parent")
        child = Task.objects.get(title="Child")
        grandchild = Task.objects.get(title="Grandchild")
        self.assertIsNone(parent.parent)
        self.assertEqual(child.parent_id, parent.id)
        self.assertEqual(grandchild.parent_id, child.id)

    def test_tags_created_and_linked(self):
        data = {
            "name": "Tags Test",
            "emoji": "",
            "position": 0,
            "sections": [
                {
                    "name": "Sec",
                    "emoji": "",
                    "position": 0,
                    "tasks": [
                        {
                            "title": "Tagged task",
                            "notes": "",
                            "due_date": None,
                            "is_completed": False,
                            "completed_at": None,
                            "position": 0,
                            "tags": ["alpha", "beta"],
                            "subtasks": [],
                        }
                    ],
                }
            ],
        }
        resp = self._upload_json(data)
        body = resp.json()
        self.assertEqual(body["tags_created"], 2)
        task = Task.objects.get(title="Tagged task")
        self.assertEqual(set(task.tags.values_list("name", flat=True)), {"alpha", "beta"})

    def test_duplicate_detection_skips(self):
        data = {
            "name": "Dup Test",
            "emoji": "",
            "position": 0,
            "sections": [
                {
                    "name": "Sec",
                    "emoji": "",
                    "position": 0,
                    "tasks": [
                        {
                            "title": "Same task",
                            "notes": "",
                            "due_date": None,
                            "is_completed": False,
                            "completed_at": None,
                            "position": 0,
                            "tags": [],
                            "subtasks": [],
                        }
                    ],
                }
            ],
        }
        self._upload_json(data)
        resp = self._upload_json(data)
        body = resp.json()
        self.assertEqual(body["tasks_created"], 0)
        self.assertEqual(body["tasks_skipped"], 1)
        self.assertEqual(Task.objects.filter(title="Same task").count(), 1)

    def test_summary_stats_shape(self):
        data = {"name": "Stats", "emoji": "", "position": 0, "sections": []}
        resp = self._upload_json(data)
        body = resp.json()
        for key in ("lists_created", "sections_created", "tasks_created", "tasks_skipped",
                     "tags_created", "parents_linked", "errors", "error_details"):
            self.assertIn(key, body)


class NativeCSVImportTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def _upload_csv(self, csv_text):
        upload = SimpleUploadedFile("export.csv", csv_text.encode("utf-8"), content_type="text/csv")
        return self.client.post("/api/import/", {"file": upload}, **self._headers())

    def test_flat_tasks(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,Task A,,0,some notes,2026-03-01,tag1,False\n"
            "Work,Todo,Task B,,0,,,,False\n"
        )
        resp = self._upload_csv(csv_text)
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertEqual(body["lists_created"], 1)
        self.assertEqual(body["sections_created"], 1)
        self.assertEqual(body["tasks_created"], 2)
        task_a = Task.objects.get(title="Task A")
        self.assertEqual(task_a.notes, "some notes")
        self.assertEqual(str(task_a.due_date), "2026-03-01")
        self.assertIsNone(task_a.parent)

    def test_subtasks_via_depth(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,Parent,,0,,,,,\n"
            "Work,Todo,Child,Parent,1,,,,,\n"
        )
        resp = self._upload_csv(csv_text)
        body = resp.json()
        self.assertEqual(body["tasks_created"], 2)
        self.assertEqual(body["parents_linked"], 1)
        child = Task.objects.get(title="Child")
        parent = Task.objects.get(title="Parent")
        self.assertEqual(child.parent_id, parent.id)

    def test_tags_parsing(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,Tagged,,0,,,alpha,beta,False\n"
        )
        # Note: comma in tags field needs proper CSV quoting
        csv_text = (
            'list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n'
            'Work,Todo,Tagged,,0,,,"alpha,beta",False\n'
        )
        resp = self._upload_csv(csv_text)
        body = resp.json()
        self.assertEqual(body["tags_created"], 2)
        task = Task.objects.get(title="Tagged")
        self.assertEqual(set(task.tags.values_list("name", flat=True)), {"alpha", "beta"})

    def test_due_date_parsing(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,Dated,,0,,2026-06-15,,False\n"
        )
        resp = self._upload_csv(csv_text)
        self.assertEqual(resp.status_code, 200)
        task = Task.objects.get(title="Dated")
        self.assertEqual(str(task.due_date), "2026-06-15")

    def test_is_completed_parsing(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,Done,,0,,,,True\n"
            "Work,Todo,Not Done,,0,,,,False\n"
        )
        resp = self._upload_csv(csv_text)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Task.objects.get(title="Done").is_completed)
        self.assertFalse(Task.objects.get(title="Not Done").is_completed)

    def test_duplicate_detection_skips(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,Repeat,,0,,,,False\n"
        )
        self._upload_csv(csv_text)
        resp = self._upload_csv(csv_text)
        body = resp.json()
        self.assertEqual(body["tasks_created"], 0)
        self.assertEqual(body["tasks_skipped"], 1)

    def test_summary_stats_shape(self):
        csv_text = "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
        resp = self._upload_csv(csv_text)
        body = resp.json()
        for key in ("lists_created", "sections_created", "tasks_created", "tasks_skipped",
                     "tags_created", "parents_linked", "errors", "error_details"):
            self.assertIn(key, body)


class FormatAutoDetectionTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def test_json_file_routes_to_native_json(self):
        data = {"name": "Test", "emoji": "", "position": 0, "sections": []}
        content = json.dumps(data).encode("utf-8")
        upload = SimpleUploadedFile("export.json", content, content_type="application/json")
        resp = self.client.post("/api/import/", {"file": upload}, **self._headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["lists_created"], 1)

    def test_native_csv_header_routes_to_native_csv(self):
        csv_text = (
            "list,section,task,parent_task,depth,notes,due_date,tags,is_completed\n"
            "Work,Todo,A task,,0,,,,False\n"
        )
        upload = SimpleUploadedFile("export.csv", csv_text.encode("utf-8"), content_type="text/csv")
        resp = self.client.post("/api/import/", {"file": upload}, **self._headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["tasks_created"], 1)

    def test_ticktick_csv_header_routes_to_ticktick(self):
        csv_text = (
            "Title,taskId,List Name,Column Name,Content,Priority,Status,Due Date,Is All Day,Created Time,Completed Time,Tags,parentId\n"
            "TT Task,ext-99,Inbox,Default,,,0,,,,,urgent,\n"
        )
        upload = SimpleUploadedFile("ticktick.csv", csv_text.encode("utf-8"), content_type="text/csv")
        resp = self.client.post("/api/import/", {"file": upload}, **self._headers())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["tasks_created"], 1)
        self.assertTrue(Task.objects.filter(title="TT Task", external_id="ext-99").exists())

    def test_unrecognized_csv_returns_400(self):
        csv_text = "col_a,col_b,col_c\n1,2,3\n"
        upload = SimpleUploadedFile("weird.csv", csv_text.encode("utf-8"), content_type="text/csv")
        resp = self.client.post("/api/import/", {"file": upload}, **self._headers())
        self.assertEqual(resp.status_code, 400)

    def test_unsupported_file_type_returns_400(self):
        upload = SimpleUploadedFile("data.xml", b"<data/>", content_type="text/xml")
        resp = self.client.post("/api/import/", {"file": upload}, **self._headers())
        self.assertEqual(resp.status_code, 400)
