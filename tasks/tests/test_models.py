import csv
import io
import json

from django.test import TestCase
from django.utils import timezone

from tasks.models import List, Section, Tag, Task


class ModelTestBase(TestCase):
    def setUp(self):
        self.task_list = List.objects.create(name="Work", emoji="💼", position=10)
        self.section = Section.objects.create(
            list=self.task_list, name="To Do", position=10
        )
        self.task = Task.objects.create(
            section=self.section, title="Write tests", position=10
        )


class ListModelTests(ModelTestBase):
    def test_tm1_list_with_emoji(self):
        """T-M-1: Creating a List with name and emoji persists correctly."""
        lst = List.objects.get(pk=self.task_list.pk)
        self.assertEqual(lst.name, "Work")
        self.assertEqual(lst.emoji, "💼")

    def test_tm2_list_without_emoji(self):
        """T-M-2: Creating a List without emoji succeeds."""
        lst = List.objects.create(name="Personal", position=20)
        self.assertEqual(lst.name, "Personal")
        self.assertEqual(lst.emoji, "")

    def test_tm3_delete_list_cascades(self):
        """T-M-3: Deleting a List cascades to its Sections and Tasks."""
        section2 = Section.objects.create(
            list=self.task_list, name="Done", position=20
        )
        task2 = Task.objects.create(section=section2, title="Another task", position=10)
        subtask = Task.objects.create(
            section=self.section, title="Subtask", parent=self.task, position=20
        )

        list_id = self.task_list.pk
        section_ids = [self.section.pk, section2.pk]
        task_ids = [self.task.pk, task2.pk, subtask.pk]

        self.task_list.delete()

        self.assertFalse(List.objects.filter(pk=list_id).exists())
        self.assertFalse(Section.objects.filter(pk__in=section_ids).exists())
        self.assertFalse(Task.objects.filter(pk__in=task_ids).exists())


class SectionModelTests(ModelTestBase):
    def test_tm4_section_linked_to_list(self):
        """T-M-4: Creating a Section linked to a List persists correctly."""
        section = Section.objects.get(pk=self.section.pk)
        self.assertEqual(section.list, self.task_list)
        self.assertEqual(section.name, "To Do")

    def test_tm5_delete_section_cascades(self):
        """T-M-5: Deleting a Section cascades to its Tasks."""
        subtask = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
        section_id = self.section.pk
        task_ids = [self.task.pk, subtask.pk]

        self.section.delete()

        self.assertFalse(Section.objects.filter(pk=section_id).exists())
        self.assertFalse(Task.objects.filter(pk__in=task_ids).exists())


class TaskModelTests(ModelTestBase):
    def test_tm6_task_within_section(self):
        """T-M-6: Creating a Task within a Section persists correctly."""
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(task.section, self.section)
        self.assertEqual(task.title, "Write tests")
        self.assertFalse(task.is_completed)

    def test_tm7_nested_subtasks(self):
        """T-M-7: Creating nested subtasks (3+ levels) persists parent chain."""
        level1 = self.task
        level2 = Task.objects.create(
            section=self.section, title="Level 2", parent=level1, position=20
        )
        level3 = Task.objects.create(
            section=self.section, title="Level 3", parent=level2, position=30
        )
        level4 = Task.objects.create(
            section=self.section, title="Level 4", parent=level3, position=40
        )

        self.assertEqual(level2.parent, level1)
        self.assertEqual(level3.parent, level2)
        self.assertEqual(level4.parent, level3)

        # Verify chain via DB reload
        level4_reloaded = Task.objects.get(pk=level4.pk)
        self.assertEqual(level4_reloaded.parent.parent.parent, level1)

    def test_tm8_delete_parent_cascades(self):
        """T-M-8: Deleting a parent Task cascades to all subtasks."""
        sub1 = Task.objects.create(
            section=self.section, title="Sub1", parent=self.task, position=20
        )
        sub2 = Task.objects.create(
            section=self.section, title="Sub2", parent=sub1, position=30
        )

        task_ids = [self.task.pk, sub1.pk, sub2.pk]
        self.task.delete()

        self.assertFalse(Task.objects.filter(pk__in=task_ids).exists())

    def test_tm9_tag_m2m(self):
        """T-M-9: Adding/removing Tags on a Task via M2M works correctly."""
        tag1 = Tag.objects.create(name="urgent")
        tag2 = Tag.objects.create(name="bug")

        self.task.tags.add(tag1, tag2)
        self.assertEqual(set(self.task.tags.values_list("name", flat=True)), {"urgent", "bug"})

        self.task.tags.remove(tag1)
        self.assertEqual(list(self.task.tags.values_list("name", flat=True)), ["bug"])

    def test_tm10_complete_task(self):
        """T-M-10: Marking a task complete sets is_completed and completed_at."""
        self.task.complete()
        self.task.refresh_from_db()

        self.assertTrue(self.task.is_completed)
        self.assertIsNotNone(self.task.completed_at)

    def test_tm11_uncomplete_task(self):
        """T-M-11: Un-completing a task sets is_completed=False and clears completed_at."""
        self.task.complete()
        self.task.uncomplete()
        self.task.refresh_from_db()

        self.assertFalse(self.task.is_completed)
        self.assertIsNone(self.task.completed_at)

    def test_tm12_complete_parent_no_cascade(self):
        """T-M-12: Completing a parent does not cascade completion to subtasks."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )

        self.task.complete()
        sub.refresh_from_db()

        self.assertTrue(self.task.is_completed)
        self.assertFalse(sub.is_completed)

    def test_tm13_move_task_to_different_section(self):
        """T-M-13: Moving a task to a different section updates its section FK."""
        new_section = Section.objects.create(
            list=self.task_list, name="In Progress", position=20
        )

        self.task.section = new_section
        self.task.save()
        self.task.refresh_from_db()

        self.assertEqual(self.task.section, new_section)

    def test_tm14_set_parent_makes_subtask(self):
        """T-M-14: Setting a task's parent makes it a subtask."""
        other_task = Task.objects.create(
            section=self.section, title="Other", position=20
        )

        other_task.parent = self.task
        other_task.save()
        other_task.refresh_from_db()

        self.assertEqual(other_task.parent, self.task)
        self.assertIn(other_task, self.task.subtasks.all())

    def test_tm15_clear_parent_promotes(self):
        """T-M-15: Clearing a task's parent promotes it to a top-level task."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )

        sub.parent = None
        sub.save()
        sub.refresh_from_db()

        self.assertIsNone(sub.parent)

    def test_tm16_move_parent_preserves_subtasks(self):
        """T-M-16: Moving a parent task preserves all subtask relationships."""
        sub1 = Task.objects.create(
            section=self.section, title="Sub1", parent=self.task, position=20
        )
        sub2 = Task.objects.create(
            section=self.section, title="Sub2", parent=sub1, position=30
        )

        new_section = Section.objects.create(
            list=self.task_list, name="Done", position=20
        )

        self.task.section = new_section
        self.task.save()

        sub1.refresh_from_db()
        sub2.refresh_from_db()

        # Subtask relationships preserved
        self.assertEqual(sub1.parent, self.task)
        self.assertEqual(sub2.parent, sub1)

    def test_tm17_serialize_list_to_json(self):
        """T-M-17: Serializing a list to JSON produces correct nested hierarchy."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )
        tag = Tag.objects.create(name="important")
        self.task.tags.add(tag)

        from tasks.views.export import serialize_list_to_json

        data = serialize_list_to_json(self.task_list)

        self.assertEqual(data["name"], "Work")
        self.assertEqual(len(data["sections"]), 1)
        section_data = data["sections"][0]
        self.assertEqual(section_data["name"], "To Do")

        # Find top-level tasks (not subtasks)
        tasks = section_data["tasks"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Write tests")
        self.assertEqual(tasks[0]["tags"], ["important"])
        self.assertEqual(len(tasks[0]["subtasks"]), 1)
        self.assertEqual(tasks[0]["subtasks"][0]["title"], "Sub")

    def test_tm18_serialize_tasks_to_csv(self):
        """T-M-18: Serializing tasks to CSV rows includes correct parent and depth."""
        sub = Task.objects.create(
            section=self.section, title="Sub", parent=self.task, position=20
        )

        from tasks.views.export import serialize_list_to_csv

        output = serialize_list_to_csv(self.task_list)
        reader = csv.DictReader(io.StringIO(output))
        rows = list(reader)

        self.assertEqual(len(rows), 2)

        parent_row = rows[0]
        self.assertEqual(parent_row["task"], "Write tests")
        self.assertEqual(parent_row["parent_task"], "")
        self.assertEqual(parent_row["depth"], "0")

        child_row = rows[1]
        self.assertEqual(child_row["task"], "Sub")
        self.assertEqual(child_row["parent_task"], "Write tests")
        self.assertEqual(child_row["depth"], "1")
