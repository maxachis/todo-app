import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from network.models import (
    Interaction,
    InteractionTask,
    InteractionType,
    Lead,
    LeadTask,
    Organization,
    OrgType,
    Person,
    RelationshipOrganizationPerson,
    RelationshipPersonPerson,
    TaskOrganization,
    TaskPerson,
)
from tasks.models import List, Project, ProjectLink, Section, Tag, Task, TimeEntry


class FullBackupExportTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a representative dataset
        self.tag = Tag.objects.create(name="urgent")
        self.project = Project.objects.create(name="Alpha", position=0)
        self.project_link = ProjectLink.objects.create(
            project=self.project, url="https://example.com", descriptor="Docs"
        )
        self.lst = List.objects.create(name="Work", emoji="W", position=0, project=self.project)
        self.section = Section.objects.create(list=self.lst, name="Todo", position=0)
        self.task = Task.objects.create(
            section=self.section, title="Write report", notes="quarterly",
            position=0, is_pinned=True,
        )
        self.task.tags.add(self.tag)
        self.subtask = Task.objects.create(
            section=self.section, title="Draft", parent=self.task, position=0,
        )
        self.time_entry = TimeEntry.objects.create(
            project=self.project, description="coding", date="2026-02-27"
        )
        self.time_entry.tasks.add(self.task)

        self.org_type = OrgType.objects.create(name="Company")
        self.interaction_type = InteractionType.objects.create(name="Meeting")
        self.person = Person.objects.create(
            first_name="Jane", last_name="Doe", email="jane@example.com"
        )
        self.org = Organization.objects.create(name="Acme", org_type=self.org_type)
        self.interaction = Interaction.objects.create(
            interaction_type=self.interaction_type, date="2026-02-27"
        )
        self.interaction.people.add(self.person)
        self.lead = Lead.objects.create(title="New deal", person=self.person)
        LeadTask.objects.create(lead=self.lead, task=self.task)
        RelationshipOrganizationPerson.objects.create(
            organization=self.org, person=self.person
        )
        TaskPerson.objects.create(task=self.task, person=self.person)
        TaskOrganization.objects.create(task=self.task, organization=self.org)
        InteractionTask.objects.create(interaction=self.interaction, task=self.task)

    def test_export_envelope_structure(self):
        resp = self.client.get("/api/export/full/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/json")
        self.assertIn("nexus-backup.json", resp["Content-Disposition"])

        data = json.loads(resp.content)
        self.assertEqual(data["format"], "nexus-full-backup")
        self.assertEqual(data["version"], 1)
        self.assertIn("exported_at", data)

    def test_export_includes_all_entity_keys(self):
        resp = self.client.get("/api/export/full/")
        data = json.loads(resp.content)

        expected_keys = {
            "tags", "projects", "project_links", "lists", "sections", "tasks",
            "time_entries", "org_types", "interaction_types", "people",
            "organizations", "interactions", "leads", "lead_tasks",
            "relationships_person_person", "relationships_organization_person",
            "task_persons", "task_organizations", "interaction_tasks",
        }
        for key in expected_keys:
            self.assertIn(key, data, f"Missing key: {key}")

    def test_export_task_fields(self):
        resp = self.client.get("/api/export/full/")
        data = json.loads(resp.content)

        tasks = data["tasks"]
        parent_task = next(t for t in tasks if t["title"] == "Write report")
        self.assertEqual(parent_task["section_id"], self.section.id)
        self.assertIsNone(parent_task["parent_id"])
        self.assertTrue(parent_task["is_pinned"])
        self.assertIn(self.tag.id, parent_task["tag_ids"])

        sub = next(t for t in tasks if t["title"] == "Draft")
        self.assertEqual(sub["parent_id"], self.task.id)

    def test_export_m2m_fields(self):
        resp = self.client.get("/api/export/full/")
        data = json.loads(resp.content)

        te = data["time_entries"][0]
        self.assertIn(self.task.id, te["task_ids"])

    def test_export_empty_database(self):
        # Clear everything
        InteractionTask.objects.all().delete()
        TaskOrganization.objects.all().delete()
        TaskPerson.objects.all().delete()
        RelationshipOrganizationPerson.objects.all().delete()
        LeadTask.objects.all().delete()
        Lead.objects.all().delete()
        Interaction.objects.all().delete()
        TimeEntry.objects.all().delete()
        Task.objects.all().delete()
        Section.objects.all().delete()
        List.objects.all().delete()
        ProjectLink.objects.all().delete()
        Project.objects.all().delete()
        Tag.objects.all().delete()
        Organization.objects.all().delete()
        OrgType.objects.all().delete()
        InteractionType.objects.all().delete()
        Person.objects.all().delete()

        resp = self.client.get("/api/export/full/")
        data = json.loads(resp.content)
        self.assertEqual(data["tasks"], [])
        self.assertEqual(data["people"], [])


class FullBackupRoundTripTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/health/")
        self.csrf = self.client.cookies["csrftoken"].value

    def _headers(self):
        return {"HTTP_X_CSRFTOKEN": self.csrf}

    def _populate_db(self):
        """Create a representative dataset and return expected counts."""
        tag = Tag.objects.create(name="urgent")
        project = Project.objects.create(name="Alpha", position=0)
        ProjectLink.objects.create(
            project=project, url="https://example.com", descriptor="Docs"
        )
        lst = List.objects.create(name="Work", emoji="W", position=0, project=project)
        section = Section.objects.create(list=lst, name="Todo", position=0)
        task = Task.objects.create(
            section=section, title="Write report", position=0
        )
        task.tags.add(tag)
        subtask = Task.objects.create(
            section=section, title="Draft", parent=task, position=0
        )
        te = TimeEntry.objects.create(
            project=project, description="coding", date="2026-02-27"
        )
        te.tasks.add(task)

        org_type = OrgType.objects.create(name="Company")
        it = InteractionType.objects.create(name="Meeting")
        person = Person.objects.create(first_name="Jane", last_name="Doe")
        org = Organization.objects.create(name="Acme", org_type=org_type)
        interaction = Interaction.objects.create(
            interaction_type=it, date="2026-02-27"
        )
        interaction.people.add(person)
        lead = Lead.objects.create(title="New deal", person=person)
        LeadTask.objects.create(lead=lead, task=task)
        RelationshipOrganizationPerson.objects.create(
            organization=org, person=person
        )
        TaskPerson.objects.create(task=task, person=person)
        TaskOrganization.objects.create(task=task, organization=org)
        InteractionTask.objects.create(interaction=interaction, task=task)

        return {
            "tags": 1, "projects": 1, "project_links": 1, "lists": 1,
            "sections": 1, "tasks": 2, "time_entries": 1, "org_types": 1,
            "interaction_types": 1, "people": 1, "organizations": 1,
            "interactions": 1, "leads": 1, "lead_tasks": 1,
            "relationships_op": 1, "task_persons": 1,
            "task_organizations": 1, "interaction_tasks": 1,
        }

    def _clear_all(self):
        InteractionTask.objects.all().delete()
        TaskOrganization.objects.all().delete()
        TaskPerson.objects.all().delete()
        RelationshipOrganizationPerson.objects.all().delete()
        RelationshipPersonPerson.objects.all().delete()
        LeadTask.objects.all().delete()
        Lead.objects.all().delete()
        Interaction.objects.all().delete()
        TimeEntry.objects.all().delete()
        Task.objects.all().delete()
        Section.objects.all().delete()
        List.objects.all().delete()
        ProjectLink.objects.all().delete()
        Project.objects.all().delete()
        Tag.objects.all().delete()
        Organization.objects.all().delete()
        OrgType.objects.all().delete()
        InteractionType.objects.all().delete()
        Person.objects.all().delete()

    def _upload_json(self, data):
        content = json.dumps(data).encode("utf-8")
        upload = SimpleUploadedFile(
            "nexus-backup.json", content, content_type="application/json"
        )
        return self.client.post("/api/import/", {"file": upload}, **self._headers())

    def test_round_trip(self):
        counts = self._populate_db()

        # Export
        resp = self.client.get("/api/export/full/")
        export_data = json.loads(resp.content)

        # Clear DB
        self._clear_all()
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(Person.objects.count(), 0)

        # Import
        resp = self._upload_json(export_data)
        self.assertEqual(resp.status_code, 200)
        stats = resp.json()

        # Verify counts match
        self.assertEqual(stats["tags_created"], counts["tags"])
        self.assertEqual(stats["projects_created"], counts["projects"])
        self.assertEqual(stats["lists_created"], counts["lists"])
        self.assertEqual(stats["sections_created"], counts["sections"])
        self.assertEqual(stats["tasks_created"], counts["tasks"])
        self.assertEqual(stats["people_created"], counts["people"])
        self.assertEqual(stats["organizations_created"], counts["organizations"])
        self.assertEqual(stats["interactions_created"], counts["interactions"])
        self.assertEqual(stats["leads_created"], counts["leads"])
        self.assertEqual(stats["errors"], 0)

        # Verify FK relationships are intact
        task = Task.objects.get(title="Write report")
        subtask = Task.objects.get(title="Draft")
        self.assertEqual(subtask.parent_id, task.id)
        self.assertTrue(task.tags.filter(name="urgent").exists())
        self.assertEqual(task.section.name, "Todo")
        self.assertEqual(task.section.list.name, "Work")

        te = TimeEntry.objects.first()
        self.assertIn(task.id, list(te.tasks.values_list("id", flat=True)))

        # Verify cross-app links
        self.assertTrue(TaskPerson.objects.filter(task=task).exists())
        self.assertTrue(TaskOrganization.objects.filter(task=task).exists())
        self.assertTrue(
            InteractionTask.objects.filter(task=task).exists()
        )

    def test_format_detection_full_backup(self):
        """Full-backup JSON routes to full import."""
        data = {
            "format": "nexus-full-backup",
            "version": 1,
            "exported_at": "2026-02-27T00:00:00",
            "tags": [], "org_types": [], "interaction_types": [],
            "projects": [], "project_links": [], "people": [],
            "organizations": [], "lists": [], "sections": [], "tasks": [],
            "time_entries": [], "interactions": [], "leads": [],
            "lead_tasks": [], "relationships_person_person": [],
            "relationships_organization_person": [],
            "task_persons": [], "task_organizations": [],
            "interaction_tasks": [],
        }
        resp = self._upload_json(data)
        self.assertEqual(resp.status_code, 200)
        stats = resp.json()
        # Full import stats have per-entity keys
        self.assertIn("tags_created", stats)
        self.assertIn("people_created", stats)

    def test_format_detection_native_json(self):
        """Regular list JSON still uses native import."""
        data = {
            "name": "Test List",
            "emoji": "",
            "position": 0,
            "sections": [
                {"name": "Default", "emoji": "", "position": 0, "tasks": []}
            ],
        }
        resp = self._upload_json(data)
        self.assertEqual(resp.status_code, 200)
        stats = resp.json()
        # Native import stats have these keys
        self.assertIn("lists_created", stats)
        # But NOT the full-backup-specific keys
        self.assertNotIn("people_created", stats)

    def test_duplicate_detection(self):
        """Importing the same backup twice skips all entities on second run."""
        self._populate_db()

        # Export
        resp = self.client.get("/api/export/full/")
        export_data = json.loads(resp.content)

        # Import again (data already exists)
        resp = self._upload_json(export_data)
        self.assertEqual(resp.status_code, 200)
        stats = resp.json()

        # Everything should be skipped
        self.assertEqual(stats["tags_skipped"], 1)
        self.assertEqual(stats["tags_created"], 0)
        self.assertEqual(stats["projects_skipped"], 1)
        self.assertEqual(stats["projects_created"], 0)
        self.assertEqual(stats["people_skipped"], 1)
        self.assertEqual(stats["people_created"], 0)
        self.assertEqual(stats["tasks_skipped"], 2)
        self.assertEqual(stats["tasks_created"], 0)
        self.assertEqual(stats["organizations_skipped"], 1)
        self.assertEqual(stats["organizations_created"], 0)
        self.assertEqual(stats["errors"], 0)
