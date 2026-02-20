"""E2E tests for sidebar/navigation/detail states in the Svelte UI."""

from playwright.sync_api import expect


class TestNavigation:
    def test_initial_tasks_view_loads_first_list_content(self, page, base_url, seed_full):
        page.goto(base_url)
        center = page.locator("#center-panel")
        expect(center).to_contain_text("To Do")
        expect(center).to_contain_text("Buy groceries")

    def test_click_list_loads_center_panel(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)

        page.locator(f'[data-list-id="{data["list2"].id}"]').click()

        center = page.locator("#center-panel")
        expect(center).to_contain_text("Work")
        expect(center).to_contain_text("Backlog")
        expect(center).to_contain_text("Review PRs")

    def test_click_task_loads_detail_panel(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()

        detail = page.locator("#detail-panel")
        expect(detail.locator("#detail-title")).to_have_value("Buy groceries")
        expect(detail.locator("#detail-title")).to_have_value("Buy groceries")

    def test_empty_states(self, page, base_url):
        page.goto(base_url)
        expect(page.locator("#center-panel")).to_contain_text("Select or create a list")
        expect(page.locator("#detail-panel")).to_contain_text("Select a task to view details")

    def test_non_tasks_routes_hide_lists_and_task_detail_panels(self, page, base_url):
        page.goto(f"{base_url}/projects")
        expect(page.locator("#sidebar")).to_have_count(0)
        expect(page.locator("#detail-panel")).to_have_count(0)

        page.goto(f"{base_url}/timesheet")
        expect(page.locator("#sidebar")).to_have_count(0)
        expect(page.locator("#detail-panel")).to_have_count(0)
