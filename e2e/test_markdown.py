"""E2E tests for Markdown rendering and XSS protection."""

from playwright.sync_api import expect

from tasks.models import Task


class TestMarkdownRendering:
    def test_markdown_renders_in_preview(self, page, base_url, seed_list_with_tasks):
        """Saving notes with markdown renders a preview below the editor."""
        task_list, section, tasks = seed_list_with_tasks
        # Set notes via ORM so we can test rendering
        tasks[0].notes = "**bold text** and *italic*"
        tasks[0].save()

        page.goto(base_url)

        # Click task to open detail
        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        # Preview should contain rendered HTML
        preview = page.locator("#detail-panel .rendered-notes")
        expect(preview).to_be_visible()
        # Check that bold text is rendered as <strong>
        expect(preview.locator("strong")).to_contain_text("bold text")
        expect(preview.locator("em")).to_contain_text("italic")

    def test_links_open_in_new_tab(self, page, base_url, seed_list_with_tasks):
        """Links in rendered markdown have target=_blank."""
        task_list, section, tasks = seed_list_with_tasks
        tasks[0].notes = "Visit https://example.com for more"
        tasks[0].save()

        page.goto(base_url)

        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        preview = page.locator("#detail-panel .rendered-notes")
        link = preview.locator("a")
        expect(link).to_have_attribute("target", "_blank")
        expect(link).to_have_attribute("rel", "noopener noreferrer")


class TestXSSProtection:
    def test_script_tag_stripped(self, page, base_url, seed_list_with_tasks):
        """Script tags in notes are stripped by bleach."""
        task_list, section, tasks = seed_list_with_tasks
        tasks[0].notes = '<script>alert("xss")</script>Safe text'
        tasks[0].save()

        page.goto(base_url)

        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        preview = page.locator("#detail-panel .rendered-notes")
        expect(preview).to_contain_text("Safe text")

        # No script tags should exist in the preview
        script_count = preview.locator("script").count()
        assert script_count == 0

    def test_onerror_attribute_stripped(self, page, base_url, seed_list_with_tasks):
        """Event handler attributes are stripped from HTML in notes."""
        task_list, section, tasks = seed_list_with_tasks
        tasks[0].notes = '<img src=x onerror="alert(1)">Normal text'
        tasks[0].save()

        page.goto(base_url)

        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        preview = page.locator("#detail-panel .rendered-notes")
        expect(preview).to_contain_text("Normal text")

        # If an img tag is present, it should not have onerror
        img_tags = preview.locator("img")
        if img_tags.count() > 0:
            # onerror should have been stripped
            expect(img_tags.first).not_to_have_attribute("onerror", "alert(1)")
