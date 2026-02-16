"""E2E tests for pinning behavior."""

import pytest

from tasks.models import List, Section, Task


class TestPinning:
    def test_pin_task_appears_in_pinned_section(self, page, base_url):
        """Pinning a task adds it to the pinned section at the top."""
        task_list = List.objects.create(name="Work", emoji="💼", position=10)
        section = Section.objects.create(list=task_list, name="To Do", position=10)
        Task.objects.create(section=section, title="Important task", position=10)

        page.goto(base_url)

        target = page.locator('.task-item:has-text("Important task")').first
        target.locator("> .task-row > .pin-btn").click()
        page.wait_for_timeout(500)

        page.locator(".pinned-section .pinned-items .task-title", has_text="Important task").wait_for(state="visible")
