"""E2E tests for search functionality."""

from playwright.sync_api import expect


class TestSearch:
    def test_search_shows_results(self, page, base_url, seed_list_with_tasks):
        """Typing in the search box shows matching tasks."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        search_input = page.locator(".navbar-search-input")
        search_input.fill("groceries")

        # Results should appear in dropdown
        dropdown = page.locator("#search-results-dropdown")
        expect(dropdown).to_contain_text("Buy groceries", timeout=5000)

    def test_search_no_results(self, page, base_url, seed_list_with_tasks):
        """Searching for nonexistent text shows no results."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        search_input = page.locator(".navbar-search-input")
        search_input.fill("zzzznonexistent")

        # Wait for debounce + response
        page.wait_for_timeout(500)

        dropdown = page.locator("#search-results-dropdown")
        expect(dropdown).not_to_contain_text("Buy groceries")

    def test_search_clears_on_outside_click(self, page, base_url, seed_list_with_tasks):
        """Clicking outside the search area clears results."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        search_input = page.locator(".navbar-search-input")
        search_input.fill("groceries")

        dropdown = page.locator("#search-results-dropdown")
        expect(dropdown).to_contain_text("Buy groceries", timeout=5000)

        # Click outside
        page.locator("#center-panel").click()

        # Dropdown should be cleared
        expect(dropdown).to_be_empty()
