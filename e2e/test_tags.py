"""E2E tests for task tag add/remove in detail panel."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import Tag


class TestTags:
    def test_add_tag(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()
        detail = page.locator("#detail-panel")
        tag_input = detail.get_by_placeholder("Add tag...")
        tag_input.fill("urgent")
        detail.locator(".typeahead-option").first.click()

        expect(page.locator("#detail-panel")).to_contain_text("urgent")
        fresh_from_db(tasks[0])
        assert tasks[0].tags.filter(name="urgent").exists()

    def test_tag_suggestions_exclude_existing(self, page, base_url, seed_list_with_tasks):
        task_list, _, tasks = seed_list_with_tasks
        tag = Tag.objects.create(name="errand")
        tasks[0].tags.add(tag)

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()

        detail = page.locator("#detail-panel")
        tag_input = detail.get_by_placeholder("Add tag...")
        tag_input.fill("errand")
        # The existing tag should not appear as a selectable option (only "Create" may appear)
        expect(detail.locator(".typeahead-option:not(.typeahead-create)")).to_have_count(0)

    def test_remove_tag(self, page, base_url, seed_full):
        task = seed_full["tasks"][0]
        page.goto(base_url)
        page.locator(f'[data-list-id="{seed_full["list1"].id}"]').click()

        page.locator(f'.task-row[data-task-id="{task.id}"]').click()
        initial_count = task.tags.count()
        page.locator("#detail-panel .tag button").first.click()
        page.wait_for_timeout(300)

        fresh_from_db(task)
        assert task.tags.count() == initial_count - 1
