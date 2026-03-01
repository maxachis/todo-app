"""E2E test: navbar navigation works from the task page with a large dataset."""

import json
from pathlib import Path

from playwright.sync_api import expect

from tasks.services.full_import import import_full_database


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "large-dataset.json"


class TestNavFromTaskPage:
    def test_navigate_away_from_task_page_with_large_dataset(self, page, base_url):
        """Load a large dataset, select the biggest list, then click a navbar link."""
        data = json.loads(FIXTURE_PATH.read_text())
        import_full_database(data)

        # Navigate to task page
        page.goto(base_url)

        # Select the Lemali list (largest, 176 tasks)
        sidebar = page.locator("#sidebar")
        lemali_item = sidebar.locator("text=Lemali")
        expect(lemali_item).to_be_visible()
        lemali_item.click()

        # Wait for tasks to render in center panel
        center = page.locator("#center-panel")
        expect(center.locator(".task-row").first).to_be_visible(timeout=10_000)

        # Click a task to simulate typical user interaction
        center.locator(".task-row").first.click()

        # Now click the Dashboard navbar link
        page.locator(".top-nav nav a", has_text="Dashboard").click()

        # Assert navigation happened within the default timeout (10s)
        expect(page).to_have_url(f"{base_url}/dashboard", timeout=5_000)

    def test_navigate_to_multiple_pages_from_task_page(self, page, base_url):
        """After loading the task page with large data, navigate to several pages."""
        data = json.loads(FIXTURE_PATH.read_text())
        import_full_database(data)

        page.goto(base_url)

        # Select the large list
        sidebar = page.locator("#sidebar")
        lemali_item = sidebar.locator("text=Lemali")
        expect(lemali_item).to_be_visible()
        lemali_item.click()

        # Wait for tasks to render
        center = page.locator("#center-panel")
        expect(center.locator(".task-row").first).to_be_visible(timeout=10_000)

        # Navigate to Projects
        page.locator(".top-nav nav a", has_text="Projects").click()
        expect(page).to_have_url(f"{base_url}/projects", timeout=5_000)

        # Navigate back to Tasks
        page.locator(".top-nav nav a", has_text="Tasks").click()
        expect(page).to_have_url(f"{base_url}/", timeout=5_000)

        # Wait for task page to load again
        expect(page.locator("#sidebar")).to_be_visible()
        expect(center.locator(".task-row").first).to_be_visible(timeout=10_000)

        # Navigate to CRM (redirects to /crm/people)
        page.locator(".top-nav nav a", has_text="CRM").click()
        page.wait_for_url(f"{base_url}/crm/**", timeout=5_000)
