"""E2E tests for Task CRUD operations."""

import re

from playwright.sync_api import expect

from tasks.models import Task


class TestTaskCreate:
    def test_create_task(self, page, base_url, seed_list):
        """Create a task using the section's inline form."""
        task_list, section = seed_list
        page.goto(base_url)

        section_el = page.locator(f'.section[data-section-id="{section.id}"]')
        section_el.locator('.task-form input[name="title"]').fill("New task")
        section_el.locator('.task-form button[type="submit"]').click()

        # Task appears in the section
        expect(section_el).to_contain_text("New task")
        assert Task.objects.filter(title="New task", section=section).exists()

    def test_create_task_clears_input(self, page, base_url, seed_list):
        """Input is cleared after task creation."""
        task_list, section = seed_list
        page.goto(base_url)

        section_el = page.locator(f'.section[data-section-id="{section.id}"]')
        title_input = section_el.locator('.task-form input[name="title"]')
        title_input.fill("Another task")
        section_el.locator('.task-form button[type="submit"]').click()

        # Wait for task to appear
        expect(section_el).to_contain_text("Another task")
        # Input should reset
        expect(title_input).to_have_value("")

    def test_create_multiple_tasks(self, page, base_url, seed_list):
        """Create multiple tasks in sequence."""
        task_list, section = seed_list
        page.goto(base_url)

        section_el = page.locator(f'.section[data-section-id="{section.id}"]')
        for title in ["First", "Second", "Third"]:
            section_el.locator('.task-form input[name="title"]').fill(title)
            section_el.locator('.task-form button[type="submit"]').click()
            expect(section_el).to_contain_text(title)

        assert Task.objects.filter(section=section).count() == 3


class TestTaskEdit:
    def test_edit_task_title_in_detail_panel(
        self, page, base_url, seed_list_with_tasks
    ):
        """Click a task, edit title in detail panel, save."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Click the first task row to load detail
        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()

        # Wait for detail panel to load
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        # Edit the title
        page.fill('#detail-panel input[name="title"]', "Buy organic groceries")
        page.click('#detail-panel .btn:has-text("Save")')

        # Detail panel should update
        expect(page.locator("#detail-panel")).to_contain_text("Buy organic groceries")
        # Center panel task row should also update via OOB swap
        expect(
            page.locator(f'.task-item[data-task-id="{tasks[0].id}"]')
        ).to_contain_text("Buy organic groceries")

        tasks[0].refresh_from_db()
        assert tasks[0].title == "Buy organic groceries"

    def test_edit_task_due_date(self, page, base_url, seed_list_with_tasks):
        """Set a due date on a task via the detail panel."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Click task to open detail
        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        # Set due date
        page.fill('#detail-panel input[name="due_date"]', "2026-03-15")
        page.click('#detail-panel .btn:has-text("Save")')

        # Due date should appear on the task row
        expect(
            page.locator(f'.task-item[data-task-id="{tasks[0].id}"]')
        ).to_contain_text("Mar 15")

        tasks[0].refresh_from_db()
        assert str(tasks[0].due_date) == "2026-03-15"


class TestTaskDelete:
    def test_delete_task_from_detail_panel(
        self, page, base_url, seed_list_with_tasks
    ):
        """Delete a task using the Delete button in the detail panel."""
        task_list, section, tasks = seed_list_with_tasks
        task_id = tasks[1].id
        page.goto(base_url)

        # Click task to open detail
        page.locator(f'.task-item[data-task-id="{task_id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Walk the dog")

        # Accept confirm dialog and delete
        page.on("dialog", lambda d: d.accept())
        page.click('#detail-panel .btn-danger:has-text("Delete Task")')

        # Task should be removed from center panel
        expect(page.locator("#center-panel")).not_to_contain_text("Walk the dog")
        assert not Task.objects.filter(pk=task_id).exists()


class TestSubtask:
    def test_subtask_displayed_under_parent(
        self, page, base_url, seed_full
    ):
        """Subtask appears nested under its parent task."""
        data = seed_full
        page.goto(base_url)

        parent = page.locator(
            f'.task-item[data-task-id="{data["tasks"][0].id}"]'
        )
        expect(parent).to_contain_text("Buy groceries")
        # Subtask should be inside parent's subtask drop zone
        expect(parent).to_contain_text("Buy milk")
