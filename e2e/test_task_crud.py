"""E2E tests for task create/update/delete against Svelte UI."""

from playwright.sync_api import expect

from tasks.models import Task


class TestTaskCrud:
    def test_create_task(self, page, base_url, seed_list):
        task_list, section = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        form = page.locator(f'form.create-form[data-section-id="{section.id}"]')
        form.locator('input[placeholder="Add task..."]').fill("New task")
        form.locator("button.add-btn").click()

        expect(page.locator("#center-panel")).to_contain_text("New task")
        assert Task.objects.filter(section=section, title="New task").exists()

    def test_edit_task_title_from_detail(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()
        title_input = page.locator("#detail-title")
        title_input.fill("Buy organic groceries")
        title_input.press("Tab")

        expect(page.locator("#center-panel")).to_contain_text("Buy organic groceries")
        tasks[0].refresh_from_db()
        assert tasks[0].title == "Buy organic groceries"

    def test_delete_task_with_keyboard(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        task_id = tasks[1].id
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{task_id}"]')
        row.click()
        expect(page.locator("#detail-title")).to_have_value("Walk the dog")
        page.evaluate(
            """(id) => {
                window.confirm = () => true;
                const scope = document.querySelector('.keyboard-scope');
                const selected = document.querySelector(`.task-row[data-task-id="${id}"]`);
                selected?.focus();
                scope?.dispatchEvent(new KeyboardEvent('keydown', { key: 'Delete', bubbles: true }));
            }""",
            task_id,
        )

        expect(page.locator(f'.task-row[data-task-id="{task_id}"]')).to_have_count(0)
        assert not Task.objects.filter(pk=task_id).exists()
