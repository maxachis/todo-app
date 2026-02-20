"""E2E tests for pin/unpin interactions."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db


class TestPinning:
    def test_pin_and_unpin_task(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        pin_btn = page.locator(f'.task-row[data-task-id="{tasks[0].id}"] .pin-btn')
        pin_btn.click()
        page.wait_for_timeout(300)

        expect(page.locator(".pinned-section")).to_contain_text("Buy groceries")
        fresh_from_db(tasks[0])
        assert tasks[0].is_pinned is True

        page.locator('.pinned-section .pinned-task:has-text("Buy groceries")').click()
        page.locator(f'.task-row[data-task-id="{tasks[0].id}"] .pin-btn').click(force=True)
        page.wait_for_timeout(300)

        fresh_from_db(tasks[0])
        assert tasks[0].is_pinned is False

    def test_pinned_order_stable_when_task_positions_change(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"] .pin-btn').click()
        page.locator(f'.task-row[data-task-id="{tasks[1].id}"] .pin-btn').click()
        page.wait_for_timeout(300)

        before = page.evaluate(
            """() => Array.from(document.querySelectorAll('.pinned-section .pinned-title'))
                .map((el) => el.textContent?.trim())"""
        )

        page.evaluate(
            """(taskIds) => {
                const zone = document.querySelectorAll('.task-dnd-zone')[0];
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: taskIds.map((id) => ({ id })) }
                }));
            }""",
            [tasks[1].id, tasks[0].id, tasks[2].id],
        )
        page.wait_for_timeout(500)

        after = page.evaluate(
            """() => Array.from(document.querySelectorAll('.pinned-section .pinned-title'))
                .map((el) => el.textContent?.trim())"""
        )
        assert before == after

    def test_reorder_pinned_tasks_within_pinned_view(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"] .pin-btn').click()
        page.locator(f'.task-row[data-task-id="{tasks[1].id}"] .pin-btn').click()
        page.wait_for_timeout(300)

        page.evaluate(
            """(ids) => {
                const zone = document.querySelector('.pinned-dnd-zone');
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: ids.map((id) => ({ id })) }
                }));
            }""",
            [tasks[1].id, tasks[0].id],
        )
        page.wait_for_timeout(300)

        titles = page.evaluate(
            """() => Array.from(document.querySelectorAll('.pinned-section .pinned-title'))
                .map((el) => el.textContent?.trim())"""
        )
        assert titles[:2] == ["Walk the dog", "Buy groceries"]
