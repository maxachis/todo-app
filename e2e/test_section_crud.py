"""E2E tests for section create/rename/delete."""

from playwright.sync_api import expect

from tasks.models import Section


class TestSectionCrud:
    def test_create_section(self, page, base_url, seed_list):
        task_list, _ = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator("form.section-create input").fill("Done")
        page.locator("form.section-create button").click()

        expect(page.locator("#center-panel")).to_contain_text("Done")
        assert Section.objects.filter(list=task_list, name="Done").exists()

    def test_rename_section(self, page, base_url, seed_list):
        task_list, section = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        name = page.locator(f'.section-header[data-section-id="{section.id}"] .name')
        name.dblclick()
        page.locator(f'.section-header[data-section-id="{section.id}"] .name-input').fill("Now")
        page.locator(f'.section-header[data-section-id="{section.id}"] .name-input').press("Enter")

        expect(page.locator(f'.section-header[data-section-id="{section.id}"]')).to_contain_text("Now")
        section.refresh_from_db()
        assert section.name == "Now"

    def test_delete_section(self, page, base_url, seed_list_with_tasks):
        task_list, section, _ = seed_list_with_tasks
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.on("dialog", lambda dialog: dialog.accept())
        page.locator(f'.section-header[data-section-id="{section.id}"] button[aria-label="Delete section"]').click()

        expect(page.locator(f'.section-header[data-section-id="{section.id}"]')).to_have_count(0)
        assert not Section.objects.filter(pk=section.pk).exists()

    def test_only_one_section_name_editor_active_at_a_time(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').click()

        section1 = data["section1"]
        section2 = data["section2"]
        row1 = page.locator(f'.section-header[data-section-id="{section1.id}"]')
        row2 = page.locator(f'.section-header[data-section-id="{section2.id}"]')

        row1.locator(".name").dblclick()
        row1.locator(".name-input").fill("Updated Section One")
        row2.locator(".name").dblclick()

        expect(page.locator(".section-header .name-input")).to_have_count(1)
        page.wait_for_timeout(350)
        section1.refresh_from_db()
        assert section1.name == "Updated Section One"
