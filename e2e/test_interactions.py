"""E2E tests for interaction creation."""

import pytest
from playwright.sync_api import expect

from network.models import Interaction, InteractionType, Person


@pytest.fixture(autouse=True)
def _reset_interactions():
    """Clean interaction tables before each test."""
    Interaction.objects.all().delete()
    InteractionType.objects.all().delete()
    Person.objects.all().delete()


class TestConsecutiveInteractionCreation:
    def test_can_create_two_interactions_in_sequence(self, page, base_url):
        """After creating one interaction, the form resets and a second can be created."""
        person = Person.objects.create(first_name="Alice", last_name="Smith")
        itype = InteractionType.objects.create(name="Email")

        page.goto(f"{base_url}/crm/interactions")

        form = page.locator(".create-form")
        person_input = form.get_by_placeholder("Add person...")
        type_input = form.get_by_placeholder("Interaction type")

        # --- First interaction ---
        person_input.fill("Alice")
        form.locator(".typeahead-option").first.click()

        type_input.fill("Email")
        form.locator(".typeahead-option").first.click()

        form.locator('input[type="date"]').fill("2026-02-20")
        form.locator("button[type='submit']").click()

        # Verify first interaction appears in list
        expect(page.locator(".list .list-item")).to_have_count(1)

        # Verify form inputs have been cleared
        expect(person_input).to_have_value("")
        expect(type_input).to_have_value("")

        # --- Second interaction ---
        person_input.fill("Alice")
        form.locator(".typeahead-option").first.click()

        type_input.fill("Email")
        form.locator(".typeahead-option").first.click()

        form.locator('input[type="date"]').fill("2026-02-21")
        form.locator("button[type='submit']").click()

        # Verify both interactions appear in list
        expect(page.locator(".list .list-item")).to_have_count(2)

        # Verify DB has both records
        assert Interaction.objects.count() == 2
