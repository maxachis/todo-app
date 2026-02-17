"""E2E tests for markdown editor interactions and sanitization."""

from playwright.sync_api import expect

from tasks.models import Task


class TestMarkdown:
    def test_click_to_edit_and_render(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()
        render_block = page.locator(".markdown-editor .block-render").first
        render_block.click()

        editor = page.locator(".markdown-editor .block-editor").first
        editor.fill("**bold text**")
        editor.press("Control+Enter")

        expect(page.locator(".markdown-editor strong")).to_contain_text("bold text")
        tasks[0].refresh_from_db()
        assert tasks[0].notes == "**bold text**"

    def test_xss_is_sanitized(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        tasks[0].notes = '<script>alert(1)</script><b>safe</b>'
        tasks[0].save()

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()

        expect(page.locator(".markdown-editor")).to_contain_text("safe")
        assert page.locator(".markdown-editor script").count() == 0

    def test_supported_markdown_syntax_renders(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        tasks[0].notes = "# Header\n\n- one\n- two\n\n`code`"
        tasks[0].save()

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()

        expect(page.locator(".markdown-editor h1")).to_contain_text("Header")
        expect(page.locator(".markdown-editor li")).to_have_count(2)
        expect(page.locator(".markdown-editor code")).to_contain_text("code")
