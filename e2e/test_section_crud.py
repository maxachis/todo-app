"""E2E tests for Section CRUD operations."""

from playwright.sync_api import expect

from tasks.models import Section


class TestSectionCreate:
    def test_create_section(self, page, base_url, seed_list):
        """Create a new section within a list."""
        task_list, _ = seed_list
        page.goto(base_url)

        page.fill('.section-form input[name="name"]', "Done")
        page.click('.section-form button[type="submit"]')

        # New section should appear in center panel
        expect(page.locator("#center-panel")).to_contain_text("Done")
        assert Section.objects.filter(name="Done", list=task_list).exists()


class TestSectionDelete:
    def test_delete_section_with_confirm(self, page, base_url, seed_list_with_tasks):
        """Delete a section after confirming the dialog."""
        task_list, section, tasks = seed_list_with_tasks
        page.goto(base_url)

        page.on("dialog", lambda d: d.accept())

        section_el = page.locator(f'.section[data-section-id="{section.id}"]')
        section_el.locator(".btn-danger:has-text('Delete')").click()

        # Section should be removed
        expect(page.locator("#center-panel")).not_to_contain_text("To Do")
        assert not Section.objects.filter(pk=section.pk).exists()
