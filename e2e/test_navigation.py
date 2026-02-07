"""E2E tests for navigation: sidebar, detail panel, empty states."""

from playwright.sync_api import expect

from tasks.models import List, Section, Task


class TestSidebarNavigation:
    def test_click_list_loads_center_panel(self, page, base_url, seed_full):
        """Clicking a list in sidebar loads its content in center panel."""
        data = seed_full
        page.goto(base_url)

        # Click the second list
        page.locator(f'.list-nav-item[data-list-id="{data["list2"].id}"]').click()

        # Center panel should show the Work list content
        expect(page.locator("#center-panel")).to_contain_text("Work")
        expect(page.locator("#center-panel")).to_contain_text("Backlog")
        expect(page.locator("#center-panel")).to_contain_text("Review PRs")

    def test_switch_between_lists(self, page, base_url, seed_full):
        """Switching between lists updates center panel each time."""
        data = seed_full
        page.goto(base_url)

        # Start on first list
        expect(page.locator("#center-panel")).to_contain_text("Test List")

        # Switch to Work
        page.locator(f'.list-nav-item[data-list-id="{data["list2"].id}"]').click()
        expect(page.locator("#center-panel")).to_contain_text("Review PRs")

        # Switch back
        page.locator(f'.list-nav-item[data-list-id="{data["list1"].id}"]').click()
        expect(page.locator("#center-panel")).to_contain_text("Buy groceries")


class TestDetailPanel:
    def test_click_task_loads_detail(self, page, base_url, seed_list_with_tasks):
        """Clicking a task row loads its detail in the right panel."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()

        # Detail panel should show task info
        detail = page.locator("#detail-panel")
        expect(detail).to_contain_text("Buy groceries")
        expect(detail.locator('input[name="title"]')).to_have_value("Buy groceries")

    def test_click_different_task_updates_detail(
        self, page, base_url, seed_list_with_tasks
    ):
        """Clicking a different task updates the detail panel."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Click first task
        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        # Click second task
        page.locator(f'.task-item[data-task-id="{tasks[1].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Walk the dog")


class TestEmptyStates:
    def test_empty_state_no_lists(self, page, base_url):
        """With no lists, show the empty state message."""
        page.goto(base_url)
        expect(page.locator(".empty-state")).to_contain_text(
            "Select or create a list"
        )

    def test_detail_empty_state(self, page, base_url, seed_list_with_tasks):
        """With no task selected, detail panel shows empty state."""
        page.goto(base_url)
        expect(page.locator(".detail-empty-state")).to_contain_text(
            "Select a task to view details"
        )
