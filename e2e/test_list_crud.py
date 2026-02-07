"""E2E tests for List CRUD operations."""

import re

from playwright.sync_api import expect

from tasks.models import List, Section


class TestListCreate:
    def test_create_list_via_sidebar_form(self, page, base_url):
        """Create a list using the sidebar inline form."""
        page.goto(base_url)
        page.fill('#sidebar .inline-form input[name="name"]', "Shopping")
        page.click('#sidebar .inline-form button[type="submit"]')

        # New list appears in sidebar
        expect(page.locator("#sidebar")).to_contain_text("Shopping")
        assert List.objects.filter(name="Shopping").exists()

    def test_create_list_appears_active(self, page, base_url):
        """Newly created list becomes the active list in the sidebar."""
        page.goto(base_url)
        page.fill('#sidebar .inline-form input[name="name"]', "My Tasks")
        page.click('#sidebar .inline-form button[type="submit"]')

        # The new list item should have the active class
        expect(page.locator('.list-nav-item.active')).to_contain_text("My Tasks")

    def test_create_list_clears_input(self, page, base_url):
        """After creating a list, the input field is cleared."""
        page.goto(base_url)
        sidebar_input = page.locator('#sidebar .inline-form input[name="name"]')
        sidebar_input.fill("New List")
        page.click('#sidebar .inline-form button[type="submit"]')

        # Wait for HTMX swap
        expect(page.locator("#sidebar")).to_contain_text("New List")
        # Input should be empty after swap (whole sidebar re-renders)
        expect(page.locator('#sidebar .inline-form input[name="name"]')).to_have_value(
            ""
        )


class TestListRename:
    def test_rename_list_via_double_click(self, page, base_url, seed_list):
        """Double-click list name to enter edit mode, then rename."""
        task_list, _ = seed_list
        page.goto(base_url)

        list_item = page.locator(f'.list-nav-item[data-list-id="{task_list.id}"]')
        display = list_item.locator(".list-nav-display")
        display.dblclick()

        # Should be in edit mode
        expect(list_item).to_have_class(re.compile(r"editing"))

        # Clear and type new name
        name_input = list_item.locator('.list-nav-edit-form input[name="name"]')
        name_input.fill("Renamed List")
        name_input.press("Enter")

        # Should update in sidebar
        expect(page.locator("#sidebar")).to_contain_text("Renamed List")
        task_list.refresh_from_db()
        assert task_list.name == "Renamed List"

    def test_rename_list_cancel_with_escape(self, page, base_url, seed_list):
        """Pressing Escape cancels the rename."""
        task_list, _ = seed_list
        page.goto(base_url)

        list_item = page.locator(f'.list-nav-item[data-list-id="{task_list.id}"]')
        list_item.locator(".list-nav-display").dblclick()

        name_input = list_item.locator('.list-nav-edit-form input[name="name"]')
        name_input.fill("Should Not Save")
        name_input.press("Escape")

        # Should revert and exit edit mode
        expect(list_item).not_to_have_class(re.compile(r"editing"))
        task_list.refresh_from_db()
        assert task_list.name == "Test List"


class TestListDelete:
    def test_delete_list_with_confirm(self, page, base_url, seed_list):
        """Delete a list after confirming the dialog."""
        task_list, _ = seed_list
        page.goto(base_url)

        # Register dialog handler before clicking
        page.on("dialog", lambda d: d.accept())

        page.click(".btn-danger:has-text('Delete List')")

        # List should be removed from sidebar
        expect(page.locator("#sidebar")).not_to_contain_text("Test List")
        assert not List.objects.filter(pk=task_list.pk).exists()
