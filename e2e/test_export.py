"""E2E tests for export functionality (JSON, CSV, Markdown)."""

import json

from playwright.sync_api import expect

from tasks.models import List, Section, Task


class TestExportSingleList:
    def test_export_json(self, page, base_url, seed_list_with_tasks):
        """Export a list as JSON and verify structure."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Intercept the download
        with page.expect_download() as download_info:
            page.click('.list-actions a:has-text("JSON")')

        download = download_info.value
        assert download.suggested_filename.endswith(".json")

        content = download.path().read_text()
        data = json.loads(content)
        assert data["name"] == "Test List"
        assert len(data["sections"]) == 1
        assert len(data["sections"][0]["tasks"]) == 3

    def test_export_csv(self, page, base_url, seed_list_with_tasks):
        """Export a list as CSV and verify it has header + data rows."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        with page.expect_download() as download_info:
            page.click('.list-actions a:has-text("CSV")')

        download = download_info.value
        assert download.suggested_filename.endswith(".csv")

        content = download.path().read_text()
        lines = content.strip().split("\n")
        # Header + 3 data rows
        assert len(lines) >= 4
        assert "list" in lines[0] and "task" in lines[0]

    def test_export_markdown(self, page, base_url, seed_list_with_tasks):
        """Export a list as Markdown and verify structure."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        with page.expect_download() as download_info:
            page.click('.list-actions a:has-text("MD")')

        download = download_info.value
        assert download.suggested_filename.endswith(".md")

        content = download.path().read_text()
        assert "# Test List" in content
        assert "## To Do" in content
        assert "- [ ] Buy groceries" in content


class TestExportAll:
    def test_export_all_json(self, page, base_url, seed_full):
        """Export All button downloads all lists as JSON."""
        page.goto(base_url)

        with page.expect_download() as download_info:
            page.click('.sidebar-actions a:has-text("Export All")')

        download = download_info.value
        content = download.path().read_text()
        data = json.loads(content)

        # Should be an array of lists
        assert isinstance(data, list)
        assert len(data) == 2
        names = {d["name"] for d in data}
        assert "Test List" in names
        assert "Work" in names
