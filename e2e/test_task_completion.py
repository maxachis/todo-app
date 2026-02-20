"""E2E tests for task completion and undo flows."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db


class TestTaskCompletion:
    def test_complete_task_shows_toast(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"] input[type="checkbox"]').click()

        expect(page.locator(".toast")).to_contain_text("completed")
        page.wait_for_timeout(300)
        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is True

    def test_undo_from_toast(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"] input[type="checkbox"]').click()
        expect(page.locator(".toast")).to_be_visible()

        page.locator('.toast .action:has-text("Undo")').click()
        page.wait_for_timeout(500)

        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is False

    def test_uncomplete_from_completed_group(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        tasks[0].complete()

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator('.completed-toggle:has-text("Completed")').click()
        page.locator(f'.task-row[data-task-id="{tasks[0].id}"] input[type="checkbox"]').click()
        page.wait_for_timeout(400)

        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is False
