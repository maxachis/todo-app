"""E2E tests for keyboard navigation."""

from playwright.sync_api import expect


class TestArrowNavigation:
    def test_arrow_down_focuses_first_task(self, page, base_url, seed_list_with_tasks):
        """Pressing ArrowDown when no task is focused selects the first task."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Press ArrowDown on body (not inside an input)
        page.keyboard.press("ArrowDown")

        # First task should have keyboard focus
        focused = page.locator(".task-row.keyboard-focus")
        expect(focused).to_be_visible()
        expect(focused).to_contain_text("Buy groceries")

    def test_arrow_down_moves_to_next(self, page, base_url, seed_list_with_tasks):
        """ArrowDown moves focus to the next task."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.keyboard.press("ArrowDown")
        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Buy groceries"
        )

        page.keyboard.press("ArrowDown")
        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Walk the dog"
        )

    def test_arrow_up_moves_to_previous(self, page, base_url, seed_list_with_tasks):
        """ArrowUp moves focus to the previous task."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Move down twice, then up once
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("ArrowUp")

        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Buy groceries"
        )


class TestJKNavigation:
    def test_j_moves_down(self, page, base_url, seed_list_with_tasks):
        """Pressing 'j' moves focus down like ArrowDown."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.keyboard.press("j")
        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Buy groceries"
        )

        page.keyboard.press("j")
        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Walk the dog"
        )

    def test_k_moves_up(self, page, base_url, seed_list_with_tasks):
        """Pressing 'k' moves focus up like ArrowUp."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.keyboard.press("j")
        page.keyboard.press("j")
        page.keyboard.press("k")

        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Buy groceries"
        )


class TestQuickComplete:
    def test_x_completes_focused_task(self, page, base_url, seed_list_with_tasks):
        """Pressing 'x' completes the currently focused task."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Focus first task
        page.keyboard.press("ArrowDown")
        expect(page.locator(".task-row.keyboard-focus")).to_contain_text(
            "Buy groceries"
        )

        # Press x to complete
        page.keyboard.press("x")

        # Should show toast
        expect(page.locator("#undo-toast")).to_be_visible()

        tasks[0].refresh_from_db()
        assert tasks[0].is_completed is True


class TestEscape:
    def test_escape_clears_focus(self, page, base_url, seed_list_with_tasks):
        """Pressing Escape removes keyboard focus from all tasks."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.keyboard.press("ArrowDown")
        expect(page.locator(".task-row.keyboard-focus")).to_be_visible()

        page.keyboard.press("Escape")
        expect(page.locator(".task-row.keyboard-focus")).not_to_be_visible()


class TestClickAwayClearsFocus:
    def test_click_sidebar_clears_focus(self, page, base_url, seed_list_with_tasks):
        """Clicking the sidebar clears the task highlight."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Focus a task
        page.keyboard.press("ArrowDown")
        expect(page.locator(".task-row.keyboard-focus")).to_be_visible()

        # Click the sidebar
        page.locator("#sidebar").click()
        expect(page.locator(".task-row.keyboard-focus")).not_to_be_visible()

    def test_click_detail_panel_clears_focus(self, page, base_url, seed_list_with_tasks):
        """Clicking the detail panel clears the task highlight."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Click a task to focus it and load its detail
        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator(".task-row.keyboard-focus")).to_be_visible()

        # Click the detail panel area
        page.locator("#detail-panel h2").click()
        expect(page.locator(".task-row.keyboard-focus")).not_to_be_visible()
