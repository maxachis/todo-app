"""E2E tests for task recurrence feature."""

from datetime import date

import pytest
from playwright.sync_api import Page, expect

from tasks.models import List, Section, Task


@pytest.fixture()
def seed_recurring_task(seed_list):
    task_list, section = seed_list
    task = Task.objects.create(
        section=section,
        title="File quarterly taxes",
        position=10,
        due_date=date(2026, 3, 15),
        recurrence_type="custom_dates",
        recurrence_rule={"dates": ["03-15", "06-15", "09-15", "12-15"]},
    )
    return task_list, section, task


def test_recurring_task_shows_repeat_icon(page: Page, base_url: str, seed_recurring_task):
    """A recurring task should display a repeat icon on its row."""
    task_list, section, task = seed_recurring_task

    page.goto(base_url)
    page.get_by_text("Test List").click()
    page.wait_for_timeout(500)

    row = page.locator(f'[data-task-id="{task.id}"]')
    expect(row).to_be_visible()
    expect(row.locator(".repeat-icon")).to_be_visible()


def test_set_recurrence_via_detail_panel(page: Page, base_url: str, seed_list_with_tasks):
    """Setting recurrence via detail panel should show repeat icon on task row."""
    task_list, section, tasks = seed_list_with_tasks
    task = tasks[0]

    page.goto(base_url)
    page.get_by_text("Test List").click()
    page.wait_for_timeout(500)

    # Select the task
    page.locator(f'[data-task-id="{task.id}"]').click()
    page.wait_for_timeout(300)

    # Set recurrence to Daily
    recurrence_select = page.locator("#recurrence-type")
    expect(recurrence_select).to_be_visible()
    recurrence_select.select_option("daily")
    recurrence_select.blur()
    page.wait_for_timeout(500)

    # Verify repeat icon appears on the task row
    row = page.locator(f'[data-task-id="{task.id}"]')
    expect(row.locator(".repeat-icon")).to_be_visible()


def test_complete_recurring_task_creates_next_occurrence(
    page: Page, base_url: str, seed_recurring_task
):
    """Completing a recurring task should create the next occurrence in the section."""
    task_list, section, task = seed_recurring_task

    page.goto(base_url)
    page.get_by_text("Test List").click()
    page.wait_for_timeout(500)

    # Complete the task via checkbox
    row = page.locator(f'[data-task-id="{task.id}"]')
    row.locator(".checkbox").click()
    page.wait_for_timeout(1500)

    # The next occurrence should appear (same title, new task ID)
    new_task = Task.objects.filter(
        section=section, title="File quarterly taxes", is_completed=False
    ).first()
    assert new_task is not None
    assert new_task.id != task.id
    assert new_task.due_date == date(2026, 6, 15)
