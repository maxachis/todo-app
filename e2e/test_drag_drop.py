"""E2E tests for drag-and-drop reordering via SortableJS."""

import pytest
from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import Task


@pytest.mark.slow
class TestDragDrop:
    def test_reorder_tasks_within_section(
        self, page, base_url, seed_list_with_tasks
    ):
        """Drag a task to reorder it within the same section."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Get bounding boxes of first and third task rows
        first_row = page.locator(
            f'.task-item[data-task-id="{tasks[0].id}"] > .task-row'
        )
        third_row = page.locator(
            f'.task-item[data-task-id="{tasks[2].id}"] > .task-row'
        )

        first_box = first_row.bounding_box()
        third_box = third_row.bounding_box()

        # Drag first task below third task
        page.mouse.move(
            first_box["x"] + first_box["width"] / 2,
            first_box["y"] + first_box["height"] / 2,
        )
        page.mouse.down()
        # Move in steps to trigger SortableJS gesture detection
        page.mouse.move(
            third_box["x"] + third_box["width"] / 2,
            third_box["y"] + third_box["height"] + 5,
            steps=10,
        )
        page.mouse.up()

        # Wait for the move request to complete
        page.wait_for_timeout(500)

        # Verify the order changed — "Buy groceries" should no longer be first
        task_items = page.locator(
            f'.section[data-section-id="{section.id}"] .task-list > .task-item'
        )
        first_task_title = task_items.first.locator(".task-title").text_content()
        assert first_task_title != "Buy groceries"

    def test_drag_task_to_different_section(self, page, base_url, seed_full):
        """Verify cross-section move works by simulating via SortableJS API.

        Native browser drag-and-drop across SortableJS groups is hard to
        simulate reliably in headless Chromium. Instead, we programmatically
        move the DOM element and trigger SortableJS's onEnd callback, then
        verify the server persists the move correctly.
        """
        data = seed_full
        task = data["tasks"][1]  # "Walk the dog"
        page.goto(base_url)

        # Use JS to simulate what SortableJS does: move the DOM element
        # and call postMove to persist it
        page.evaluate(
            """([taskId, sectionId]) => {
                const taskEl = document.querySelector(
                    `.task-item[data-task-id="${taskId}"]`
                );
                const targetList = document.querySelector(
                    `.section[data-section-id="${sectionId}"] .task-list`
                );
                // Move DOM element
                targetList.appendChild(taskEl);
                // Persist via the same function SortableJS uses
                postMove(taskId, {
                    section: sectionId,
                    position: 0,
                    parent: "null"
                });
            }""",
            [str(task.id), str(data["section2"].id)],
        )

        page.wait_for_timeout(500)

        # Verify the task appears in the target section's DOM
        target_section = page.locator(
            f'.section[data-section-id="{data["section2"].id}"]'
        )
        expect(target_section).to_contain_text("Walk the dog")

        # Verify in the database
        fresh_from_db(task)
        assert task.section_id == data["section2"].id
