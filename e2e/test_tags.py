"""E2E tests for tag add/remove on tasks."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import Tag


class TestTagAdd:
    def test_add_tag_to_task(self, page, base_url, seed_list_with_tasks):
        """Add a tag via the detail panel form."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        # Open detail for first task
        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        # Add a tag
        page.fill('#detail-panel .tag-form input[name="name"]', "urgent")
        page.click('#detail-panel .tag-form button[type="submit"]')

        # Tag should appear in detail panel
        expect(page.locator("#detail-panel .tag")).to_contain_text("urgent")
        assert Tag.objects.filter(name="urgent").exists()
        fresh_from_db(tasks[0])
        assert tasks[0].tags.filter(name="urgent").exists()

    def test_add_multiple_tags(self, page, base_url, seed_list_with_tasks):
        """Add multiple tags to the same task."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.locator(f'.task-item[data-task-id="{tasks[0].id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("Buy groceries")

        for tag_name in ["urgent", "shopping"]:
            page.fill('#detail-panel .tag-form input[name="name"]', tag_name)
            page.click('#detail-panel .tag-form button[type="submit"]')
            expect(page.locator("#detail-panel")).to_contain_text(tag_name)

        fresh_from_db(tasks[0])
        assert tasks[0].tags.count() == 2


class TestTagRemove:
    def test_remove_tag_from_task(self, page, base_url, seed_full):
        """Remove a tag by clicking the x button."""
        data = seed_full
        task = data["tasks"][0]
        page.goto(base_url)

        # Open detail for the task that has tags
        page.locator(f'.task-item[data-task-id="{task.id}"] > .task-row').click()
        expect(page.locator("#detail-panel")).to_contain_text("urgent")

        # Count tags before
        initial_count = task.tags.count()

        # Click remove on the first tag
        page.locator("#detail-panel .tag-remove").first.click()

        # Wait for HTMX swap — the detail panel should refresh
        # After removing one tag, there should be fewer .tag elements
        expect(page.locator("#detail-panel .tag")).to_have_count(initial_count - 1)

        fresh_from_db(task)
        assert task.tags.count() == initial_count - 1
