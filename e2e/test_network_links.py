"""E2E tests for network navigation and task-entity linking."""

import pytest
from playwright.sync_api import expect

from network.models import Person, Organization, TaskPerson, TaskOrganization


@pytest.fixture(autouse=True)
def _reset_network_db():
    """Clean network tables before each test."""
    TaskPerson.objects.all().delete()
    TaskOrganization.objects.all().delete()
    Person.objects.all().delete()
    Organization.objects.all().delete()


class TestNetworkNavigation:
    def test_navbar_includes_all_tabs(self, page, base_url):
        page.goto(base_url)
        nav = page.locator("header.top-nav nav")
        for label in [
            "Tasks",
            "Dashboard",
            "Projects",
            "Timesheet",
            "CRM",
            "Network",
        ]:
            expect(nav.get_by_text(label, exact=True)).to_be_visible()

    def test_network_tabs_navigate_to_correct_routes(self, page, base_url):
        page.goto(base_url)
        nav = page.locator("header.top-nav nav")

        nav.get_by_text("CRM", exact=True).click()
        expect(page).to_have_url(f"{base_url}/crm/people")
        expect(page.locator("h1")).to_contain_text("People")

        page.locator(".sub-tabs").get_by_text("Orgs", exact=True).click()
        expect(page).to_have_url(f"{base_url}/crm/orgs")
        expect(page.locator("h1")).to_contain_text("Organizations")

    def test_network_routes_hide_task_panels(self, page, base_url):
        page.goto(f"{base_url}/crm/people")
        expect(page.locator("#sidebar")).to_have_count(0)
        expect(page.locator("#detail-panel")).to_have_count(0)


class TestTaskPersonLinking:
    def test_link_person_from_task_detail(self, page, base_url, seed_list_with_tasks):
        task_list, section, tasks = seed_list_with_tasks
        person = Person.objects.create(
            first_name="Alice", last_name="Smith"
        )

        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()
        page.locator(f'.task-row[data-task-id="{tasks[0].id}"]').click()

        detail = page.locator("#detail-panel")
        detail.wait_for(state="visible")

        # Find the linked section
        linked_section = detail.locator(".linked-section")
        expect(linked_section).to_be_visible()

        # Type into the typeahead to find the person and select
        typeahead_input = linked_section.locator('.typeahead-input').first
        typeahead_input.fill("Alice")
        linked_section.locator('.typeahead-option').first.click()

        # Person should appear in the linked list
        expect(linked_section).to_contain_text("Alice Smith")

        # Verify DB link was created
        assert TaskPerson.objects.filter(
            task_id=tasks[0].id, person_id=person.id
        ).exists()

        # Remove the link
        linked_section.locator(".remove-btn").first.click()
        expect(linked_section).not_to_contain_text("Alice Smith")

        # Verify DB link was removed
        assert not TaskPerson.objects.filter(
            task_id=tasks[0].id, person_id=person.id
        ).exists()


class TestPersonTaskLinking:
    def test_link_task_from_person_detail(self, page, base_url, seed_list_with_tasks):
        task_list, section, tasks = seed_list_with_tasks
        person = Person.objects.create(
            first_name="Bob", last_name="Jones"
        )

        page.goto(f"{base_url}/crm/people")

        # Select the person
        page.get_by_text("Jones, Bob").click()

        # Find the linked tasks section and wait for tasks to load
        detail = page.locator(".detail-panel")
        linked_section = detail.locator(".linked-tasks-section")
        expect(linked_section).to_be_visible()

        # Wait for task data to load (TypeaheadSelect only renders when options exist)
        typeahead_input = linked_section.locator('.typeahead-input')
        expect(typeahead_input).to_be_visible()
        typeahead_input.fill("Buy groceries")
        linked_section.locator('.typeahead-option').first.click()

        # Task title should appear
        expect(linked_section).to_contain_text("Buy groceries")

        # Verify DB link
        assert TaskPerson.objects.filter(
            task_id=tasks[0].id, person_id=person.id
        ).exists()

        # Remove the link
        linked_section.locator(".remove-btn").first.click()
        expect(linked_section).not_to_contain_text("Buy groceries")
