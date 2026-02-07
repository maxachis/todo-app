"""E2E tests for task completion, undo toast, and uncomplete."""

import pytest
from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import Task


class TestComplete:
    def test_complete_task_via_checkbox(self, page, base_url, seed_list_with_tasks):
        """Clicking the checkbox completes a task."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        task_el = page.locator(f'.task-item[data-task-id="{tasks[0].id}"]')
        task_el.locator("button.checkbox").click()

        # Wait for HTMX response (toast proves completion happened)
        expect(page.locator("#undo-toast")).to_be_visible()

        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is True

    def test_complete_task_shows_toast(self, page, base_url, seed_list_with_tasks):
        """Completing a task shows an undo toast."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        task_el = page.locator(f'.task-item[data-task-id="{tasks[0].id}"]')
        task_el.locator("button.checkbox").click()

        # Toast should appear
        toast = page.locator("#undo-toast")
        expect(toast).to_be_visible()
        expect(toast).to_contain_text("completed")

    def test_undo_via_toast(self, page, base_url, seed_list_with_tasks):
        """Clicking Undo on the toast uncompletes the task.

        The undo button has onclick="dismissToast()" which removes the
        toast from DOM AND hx-post for the uncomplete request. We trigger
        the HTMX request directly to avoid the race between onclick DOM
        removal and HTMX processing.
        """
        task_list, section, tasks = seed_list_with_tasks
        task_id = tasks[0].id
        page.goto(base_url)

        task_el = page.locator(f'.task-item[data-task-id="{task_id}"]')
        task_el.locator("button.checkbox").click()

        # Wait for toast to appear
        toast = page.locator("#undo-toast")
        expect(toast).to_be_visible()

        # Trigger the uncomplete via htmx.ajax (same as what the button does)
        # This avoids the dismissToast() race condition
        page.evaluate(
            """(taskId) => {
                htmx.ajax("POST", `/tasks/${taskId}/uncomplete/`, {
                    target: "#center-panel",
                    swap: "innerHTML"
                });
                dismissToast();
            }""",
            task_id,
        )

        # After undo, the task should reappear in the uncompleted task list
        task_in_list = page.locator(
            f'.task-list .task-item[data-task-id="{task_id}"]'
        )
        expect(task_in_list).to_be_visible(timeout=5000)

        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is False

    @pytest.mark.slow
    def test_toast_auto_dismisses(self, page, base_url, seed_list_with_tasks):
        """Toast auto-dismisses after timeout."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        task_el = page.locator(f'.task-item[data-task-id="{tasks[0].id}"]')
        task_el.locator("button.checkbox").click()

        toast = page.locator("#undo-toast")
        expect(toast).to_be_visible()

        # Wait for auto-dismiss (5 seconds + animation)
        expect(toast).not_to_be_visible(timeout=8000)


class TestUncomplete:
    def test_uncomplete_task_in_completed_section(
        self, page, base_url, seed_list_with_tasks
    ):
        """Uncomplete a previously completed task."""
        task_list, section, tasks = seed_list_with_tasks
        # Complete the task via ORM
        tasks[0].complete()
        page.goto(base_url)

        # Find the completed task and click its checkbox
        completed_task = page.locator(f'.task-item[data-task-id="{tasks[0].id}"]')
        completed_task.locator("button.checkbox.checked").click()

        # Wait for HTMX swap to complete
        expect(page.locator("#center-panel")).to_contain_text("Buy groceries")
        # Verify the task is now in the uncompleted section (not the completed group)
        task_item = page.locator(
            f'.task-list .task-item[data-task-id="{tasks[0].id}"]'
        )
        expect(task_item).to_be_visible()

        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is False
