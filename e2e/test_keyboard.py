"""E2E tests for keyboard navigation and task actions."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import Section, Task


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
                selected?.dispatchEvent(new KeyboardEvent('keydown', { key: 'Delete', bubbles: true }));
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

    def test_arrow_up_from_add_input_selects_task_above(self, page, base_url, seed_list_with_tasks):
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        task_input = page.locator(f'.create-form[data-section-id="{section.id}"] .task-input')
        task_input.click()

        # Selection should be cleared when input is focused
        expect(page.locator(".task-row.selected")).to_have_count(0)

        page.keyboard.press("ArrowUp")
        # Should select the last task in the section (immediately above the input)
        expect(page.locator("#detail-title")).to_have_value("Read a book")

    def test_arrow_down_from_last_task_focuses_add_input(self, page, base_url, seed_list_with_tasks):
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        row = page.locator(f'.task-row[data-task-id="{tasks[2].id}"]')
        row.click()
        row.focus()
        row.press("ArrowDown")

        # Should focus the add-task input and clear selection
        task_input = page.locator(f'.create-form[data-section-id="{section.id}"] .task-input')
        expect(task_input).to_be_focused()
        expect(page.locator(".task-row.selected")).to_have_count(0)

    def test_arrow_nav_cycles_between_tasks_and_add_input(self, page, base_url, seed_list_with_tasks):
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        # Start at last task, arrow down to input
        row = page.locator(f'.task-row[data-task-id="{tasks[2].id}"]')
        row.click()
        row.focus()
        row.press("ArrowDown")

        task_input = page.locator(f'.create-form[data-section-id="{section.id}"] .task-input')
        expect(task_input).to_be_focused()

        # Arrow up from input back to last task
        page.keyboard.press("ArrowUp")
        expect(page.locator("#detail-title")).to_have_value("Read a book")

        # Arrow down continues working from the selected task
        page.keyboard.press("ArrowDown")
        expect(task_input).to_be_focused()

    def test_arrow_down_from_input_goes_to_next_section_task(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        # Focus the first section's add-task input
        task_input = page.locator(f'.create-form[data-section-id="{data["section1"].id}"] .task-input')
        task_input.click()

        # Arrow Down should go to the first task in the next section
        page.keyboard.press("ArrowDown")
        expect(page.locator("#detail-title")).to_have_value("Write report")

    def test_arrow_down_from_input_to_empty_section_input(self, page, base_url, seed_list):
        task_list, section1 = seed_list
        Task.objects.create(section=section1, title="Task A", position=10)
        section2 = Section.objects.create(list=task_list, name="Empty Section", position=20)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        # Focus first section's input
        task_input1 = page.locator(f'.create-form[data-section-id="{section1.id}"] .task-input')
        task_input1.click()

        # Arrow Down should focus the empty section's input
        page.keyboard.press("ArrowDown")
        task_input2 = page.locator(f'.create-form[data-section-id="{section2.id}"] .task-input')
        expect(task_input2).to_be_focused()

    def test_arrow_up_from_top_of_section_goes_to_prev_section_input(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        # Select the first (only) task in section 2
        row = page.locator(f'.task-row[data-task-id="{data["task_in_progress"].id}"]')
        row.click()
        row.focus()

        # Arrow Up should go to section 1's add-task input, not section 1's last task
        row.press("ArrowUp")
        task_input = page.locator(f'.create-form[data-section-id="{data["section1"].id}"] .task-input')
        expect(task_input).to_be_focused()
        expect(page.locator(".task-row.selected")).to_have_count(0)

    def test_full_section_navigation_cycle(self, page, base_url, seed_full):
        """Arrow keys traverse: section1 tasks → section1 input → section2 tasks → section2 input and back."""
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        # Start at last task in section 1
        row = page.locator(f'.task-row[data-task-id="{data["tasks"][2].id}"]')
        row.click()
        row.focus()

        # Down → section 1 input
        row.press("ArrowDown")
        input1 = page.locator(f'.create-form[data-section-id="{data["section1"].id}"] .task-input')
        expect(input1).to_be_focused()

        # Down → section 2 first task
        page.keyboard.press("ArrowDown")
        expect(page.locator("#detail-title")).to_have_value("Write report")

        # Down → section 2 input
        page.keyboard.press("ArrowDown")
        input2 = page.locator(f'.create-form[data-section-id="{data["section2"].id}"] .task-input')
        expect(input2).to_be_focused()

        # Up → section 2 first task
        page.keyboard.press("ArrowUp")
        expect(page.locator("#detail-title")).to_have_value("Write report")

        # Up → section 1 input
        page.keyboard.press("ArrowUp")
        expect(input1).to_be_focused()

        # Up → section 1 last task
        page.keyboard.press("ArrowUp")
        expect(page.locator("#detail-title")).to_have_value("Read a book")

    def test_arrow_up_through_section_to_prev_input(self, page, base_url, seed_list):
        """Navigate up through multiple tasks in section 2, then across boundary to section 1 input."""
        task_list, section1 = seed_list
        Task.objects.create(section=section1, title="S1 Task", position=10)
        section2 = Section.objects.create(list=task_list, name="Section 2", position=20)
        Task.objects.create(section=section2, title="S2 First", position=10)
        Task.objects.create(section=section2, title="S2 Second", position=20)
        Task.objects.create(section=section2, title="S2 Third", position=30)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        # Click the last task in section 2
        s2_tasks = page.locator(f'.task-row[data-section-id="{section2.id}"]')
        s2_tasks.last.click()
        s2_tasks.last.focus()
        expect(page.locator("#detail-title")).to_have_value("S2 Third")

        # Navigate up through section 2
        page.keyboard.press("ArrowUp")
        expect(page.locator("#detail-title")).to_have_value("S2 Second")

        page.keyboard.press("ArrowUp")
        expect(page.locator("#detail-title")).to_have_value("S2 First")

        # One more ArrowUp should go to section 1's input, NOT section 1's last task
        page.keyboard.press("ArrowUp")
        input1 = page.locator(f'.create-form[data-section-id="{section1.id}"] .task-input')
        expect(input1).to_be_focused()
        expect(page.locator(".task-row.selected")).to_have_count(0)

    def test_arrow_up_from_empty_section_input_goes_to_prev_section_input(self, page, base_url, seed_list):
        task_list, section1 = seed_list
        Task.objects.create(section=section1, title="Task A", position=10)
        section2 = Section.objects.create(list=task_list, name="Empty Section", position=20)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        # Focus the empty section's input
        input2 = page.locator(f'.create-form[data-section-id="{section2.id}"] .task-input')
        input2.click()

        # Arrow Up should go to section 1's input, NOT section 1's task
        page.keyboard.press("ArrowUp")
        input1 = page.locator(f'.create-form[data-section-id="{section1.id}"] .task-input')
        expect(input1).to_be_focused()
        expect(page.locator(".task-row.selected")).to_have_count(0)

    def test_escape_clears_add_input(self, page, base_url, seed_list):
        task_list, section = seed_list
        Task.objects.create(section=section, title="Some task", position=10)
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        task_input = page.locator(f'.create-form[data-section-id="{section.id}"] .task-input')
        task_input.click()
        task_input.fill("some text")
        expect(task_input).to_have_value("some text")

        page.keyboard.press("Escape")
        expect(task_input).to_have_value("")
        expect(task_input).not_to_be_focused()

    def test_shortcut_keys_typeable_in_task_input(self, page, base_url, seed_list):
        task_list, section = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        task_input = page.locator(f'.create-form[data-section-id="{section.id}"] .task-input')
        task_input.click()

        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        punctuation = "!@#$%^&*()-_=+[]{}|;:',.<>?/`~"

        all_chars = lowercase + uppercase + digits + punctuation
        task_input.press_sequentially(all_chars, delay=0)

        expect(task_input).to_have_value(all_chars)
