"""E2E tests for export downloads (JSON/CSV/Markdown)."""

from pathlib import Path
import json


class TestExport:
    def test_export_single_list_json(self, page, base_url, seed_list_with_tasks):
        page.goto(base_url)

        page.locator("#center-panel .export-btn").first.click()
        with page.expect_download() as dl:
            page.locator("#center-panel .export-menu button", has_text="JSON").click()

        download = dl.value
        assert download.suggested_filename.endswith(".json")
        data = json.loads(Path(download.path()).read_text(encoding="utf-8"))
        assert data["name"] == "Test List"

    def test_export_single_list_csv(self, page, base_url, seed_list_with_tasks):
        page.goto(base_url)

        page.locator("#center-panel .export-btn").first.click()
        with page.expect_download() as dl:
            page.locator("#center-panel .export-menu button", has_text="CSV").click()

        download = dl.value
        text = Path(download.path()).read_text(encoding="utf-8")
        assert download.suggested_filename.endswith(".csv")
        assert "list" in text.splitlines()[0]

    def test_export_all_markdown(self, page, base_url, seed_full):
        page.goto(base_url)

        page.locator("#sidebar .export-btn").first.click()
        with page.expect_download() as dl:
            page.locator("#sidebar .export-menu button", has_text="Markdown").click()

        download = dl.value
        text = Path(download.path()).read_text(encoding="utf-8")
        assert download.suggested_filename.endswith(".md")
        assert "Test List" in text
