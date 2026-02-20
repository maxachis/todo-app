"""E2E tests for keyboard navigation and task actions."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import Task


class TestKeyboard:
    def test_click_then_arrow_navigation_immediate(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()
        page.keyboard.press("ArrowDown")

        expect(page.locator("#detail-title")).to_have_value("Walk the dog")

    def test_arrow_navigation_updates_selection(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{tasks[0].id}"]')
        row.click()
        row.focus()
        row.press("ArrowDown")

        expect(page.locator("#detail-title")).to_have_value("Walk the dog")

    def test_jk_navigation(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{tasks[0].id}"]')
        row.click()
        row.focus()
        row.press("j")
        expect(page.locator("#detail-title")).to_have_value("Walk the dog")

        row.press("k")
        expect(page.locator("#detail-title")).to_have_value("Buy groceries")

    def test_tab_indent_shift_tab_outdent(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{tasks[1].id}"]')
        row.click()
        row.focus()
        row.press("Tab")
        page.wait_for_timeout(400)
        fresh_from_db(tasks[1])
        assert tasks[1].parent_id == tasks[0].id

        row.press("Shift+Tab")
        page.wait_for_timeout(400)
        fresh_from_db(tasks[0])
        fresh_from_db(tasks[1])
        assert tasks[1].parent_id is None
        assert tasks[1].position > tasks[0].position

    def test_tab_does_not_cross_sections(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{data["task_in_progress"].id}"]')
        row.click()
        row.focus()
        row.press("Tab")
        page.wait_for_timeout(400)

        fresh_from_db(data["task_in_progress"])
        assert data["task_in_progress"].section_id == data["section2"].id
        assert data["task_in_progress"].parent_id is None

    def test_tab_uses_previous_same_level_not_child(self, page, base_url, seed_list):
        task_list, section = seed_list
        task_a = Task.objects.create(section=section, title="Task A", position=10)
        task_b = Task.objects.create(section=section, title="Task B", position=20)
        task_b_child = Task.objects.create(section=section, parent=task_b, title="Task B child", position=10)
        task_c = Task.objects.create(section=section, title="Task C", position=30)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{task_c.id}"]')
        row.click()
        row.focus()
        row.press("Tab")
        page.wait_for_timeout(500)

        fresh_from_db(task_c)
        assert task_c.parent_id == task_b.id
        assert task_c.parent_id != task_b_child.id

    def test_shift_tab_outdents_on_first_press(self, page, base_url, seed_list):
        task_list, section = seed_list
        parent = Task.objects.create(section=section, title="Parent", position=10)
        child = Task.objects.create(section=section, parent=parent, title="Child", position=10)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{child.id}"]')
        row.click()
        row.press("Shift+Tab")
        page.wait_for_timeout(500)

        fresh_from_db(child)
        assert child.parent_id is None

    def test_shift_tab_outdents_immediately_even_after_focus_blur(self, page, base_url, seed_list):
        task_list, section = seed_list
        parent = Task.objects.create(section=section, title="Parent", position=10)
        child = Task.objects.create(section=section, parent=parent, title="Child", position=10)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{child.id}"]')
        row.click()
        page.evaluate("() => document.activeElement instanceof HTMLElement && document.activeElement.blur()")
        page.keyboard.press("Shift+Tab")
        page.wait_for_timeout(500)

        fresh_from_db(child)
        assert child.parent_id is None

    def test_x_completes_and_escape_clears(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{tasks[0].id}"]')
        row.click()
        row.focus()
        row.press("x")
        page.wait_for_timeout(400)
        fresh_from_db(tasks[0])
        assert tasks[0].is_completed is True

        page.evaluate(
            """() => {
                const scope = document.querySelector('.keyboard-scope');
                scope?.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
            }"""
        )
        expect(page.locator("#detail-panel")).to_contain_text("Select a task to view details")

    def test_delete_key_removes_task(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        task_id = tasks[2].id
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{task_id}"]').click()
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
        page.wait_for_timeout(400)

        assert not Task.objects.filter(pk=task_id).exists()

    def test_ctrl_arrows_cycle_sections_and_lists(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{data["tasks"][0].id}"]')
        row.click()
        row.focus()
        row.press("Control+ArrowDown")
        expect(page.locator("#detail-title")).to_have_value("Write report")

        row.press("Control+ArrowRight")
        expect(page.locator("#center-panel")).to_contain_text("Work")

    def test_shortcut_keys_typeable_in_task_input(self, page, base_url, seed_list):
        task_list, section = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        task_input = page.locator(f'.create-form[data-section-id="{section.id}"] .task-input')
        task_input.click()
        task_input.type("jkx")

        expect(task_input).to_have_value("jkx")
