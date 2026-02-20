"""E2E tests for drag/drop behavior in Svelte UI."""

from e2e.conftest import fresh_from_db
from playwright.sync_api import expect
from tasks.models import Task


class TestDragDrop:
    def test_reorder_within_section(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.wait_for_selector(".task-dnd-zone")

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
        page.wait_for_timeout(400)

        rows = page.locator(".task-dnd-zone .task-row")
        expect(rows).to_have_count(3)
        expect(page.locator(".task-dnd-zone")).to_contain_text("Buy groceries")
        expect(page.locator(".task-dnd-zone")).to_contain_text("Walk the dog")
        expect(page.locator(".task-dnd-zone")).to_contain_text("Read a book")

        fresh_from_db(tasks[1])
        fresh_from_db(tasks[0])
        assert tasks[1].position < tasks[0].position

    def test_move_across_sections(self, page, base_url, seed_full):
        data = seed_full
        moving = data["tasks"][1]
        target_section_id = data["section2"].id
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()
        page.wait_for_selector(".task-dnd-zone")

        page.evaluate(
            """(taskId) => {
                const zones = document.querySelectorAll('.task-dnd-zone');
                const zone = zones[1];
                const ids = Array.from(zone.querySelectorAll('[data-task-id]')).map((el) => Number(el.dataset.taskId));
                if (!ids.includes(taskId)) ids.unshift(taskId);
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: ids.map((id) => ({ id })) }
                }));
            }""",
            moving.id,
        )
        page.wait_for_timeout(400)

        fresh_from_db(moving)
        assert moving.section_id == target_section_id

    def test_cross_list_drop_target(self, page, base_url, seed_full):
        data = seed_full
        moving = data["tasks"][0]
        target_list = data["list2"]
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()
        page.wait_for_selector(f'[data-list-id="{target_list.id}"]')

        page.evaluate(
            """([taskId, listId]) => {
                const target = document.querySelector(`[data-list-id="${listId}"]`);
                const dt = new DataTransfer();
                dt.setData('text/task-id', String(taskId));
                target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer: dt }));
                target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer: dt }));
            }""",
            [moving.id, target_list.id],
        )
        page.wait_for_timeout(500)

        fresh_from_db(moving)
        assert moving.section.list_id == target_list.id

    def test_reorder_sections_without_duplicates(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()
        page.wait_for_selector(".sections-dnd")

        page.evaluate(
            """(sectionIds) => {
                const zone = document.querySelector('.sections-dnd');
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: sectionIds.map((id) => ({ id })) }
                }));
            }""",
            [data["section2"].id, data["section1"].id],
        )
        page.wait_for_timeout(500)

        headers = page.locator(".section-header[data-section-id]")
        expect(headers).to_have_count(2)

        unique_count = page.evaluate(
            """() => {
                const ids = Array.from(document.querySelectorAll('.section-header[data-section-id]'))
                    .map((el) => Number(el.getAttribute('data-section-id')));
                return new Set(ids).size;
            }"""
        )
        assert unique_count == 2

        fresh_from_db(data["section1"])
        fresh_from_db(data["section2"])
        assert data["section2"].position < data["section1"].position

    def test_sections_use_header_drag_handle_only(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        handles = page.locator(".section-header .drag-handle")
        expect(handles).to_have_count(2)
        expect(page.locator(".task-row .drag-handle")).to_have_count(0)

    def test_drop_below_midpoint_nests_under_target_task(self, page, base_url, seed_list):
        task_list, section = seed_list
        task_a = Task.objects.create(section=section, title="Task A", position=10)
        task_b = Task.objects.create(section=section, title="Task B", position=20)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator(f'.task-row[data-task-id="{task_b.id}"]').wait_for()

        page.evaluate(
            """([dragId, targetId]) => {
                const target = document.querySelector(`.task-row[data-task-id="${targetId}"]`);
                if (!target) return;
                const rect = target.getBoundingClientRect();
                const y = rect.top + (rect.height * 0.75);
                const dt = new DataTransfer();
                dt.setData('text/task-id', String(dragId));
                target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, clientY: y, dataTransfer: dt }));
                target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, clientY: y, dataTransfer: dt }));
            }""",
            [task_a.id, task_b.id],
        )
        page.wait_for_timeout(500)

        fresh_from_db(task_a)
        assert task_a.parent_id == task_b.id

    def test_drop_above_midpoint_on_subtask_keeps_same_parent_level(self, page, base_url, seed_list):
        task_list, section = seed_list
        task_a = Task.objects.create(section=section, title="Task A", position=10)
        task_c = Task.objects.create(section=section, title="Task C", position=20)
        task_b = Task.objects.create(section=section, parent=task_c, title="Task B", position=10)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator(f'.task-row[data-task-id="{task_b.id}"]').wait_for()

        page.evaluate(
            """([dragId, targetId]) => {
                const target = document.querySelector(`.task-row[data-task-id="${targetId}"]`);
                if (!target) return;
                const rect = target.getBoundingClientRect();
                const y = rect.top + (rect.height * 0.25);
                const dt = new DataTransfer();
                dt.setData('text/task-id', String(dragId));
                target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, clientY: y, dataTransfer: dt }));
                target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, clientY: y, dataTransfer: dt }));
            }""",
            [task_a.id, task_b.id],
        )
        page.wait_for_timeout(500)

        fresh_from_db(task_a)
        assert task_a.parent_id == task_c.id

    def test_rapid_finalize_reorders_do_not_break_task_list(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.wait_for_selector(".task-dnd-zone")

        page.evaluate(
            """(taskIds) => {
                const zone = document.querySelectorAll('.task-dnd-zone')[0];
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: taskIds.map((id) => ({ id })) }
                }));
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: taskIds.slice().reverse().map((id) => ({ id })) }
                }));
            }""",
            [tasks[0].id, tasks[1].id, tasks[2].id],
        )
        page.wait_for_timeout(600)

        rows = page.locator(".task-dnd-zone .task-row")
        expect(rows).to_have_count(3)
