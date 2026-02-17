"""E2E tests for list create/rename/delete in sidebar."""

from playwright.sync_api import expect

from e2e.conftest import fresh_from_db
from tasks.models import List


class TestListCrud:
    def test_create_list(self, page, base_url):
        page.goto(base_url)

        sidebar = page.locator("#sidebar")
        name_input = sidebar.locator('input[placeholder="Create list..."]')
        name_input.fill("Shopping")
        name_input.press("Enter")
        page.wait_for_timeout(300)

        expect(sidebar).to_contain_text("Shopping")
        assert List.objects.filter(name="Shopping").exists()

    def test_rename_list_inline(self, page, base_url, seed_list):
        task_list, _ = seed_list
        page.goto(base_url)

        row = page.locator(f'[data-list-id="{task_list.id}"]')
        row.dblclick()
        row.locator("input").fill("Renamed List")
        row.locator("input").press("Enter")

        expect(row).to_contain_text("Renamed List")
        task_list.refresh_from_db()
        assert task_list.name == "Renamed List"

    def test_delete_list(self, page, base_url, seed_list):
        task_list, _section = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').wait_for()

        dialog_seen = {"value": False}

        def on_dialog(dialog):
            dialog_seen["value"] = True
            dialog.dismiss()

        page.on("dialog", on_dialog)
        page.evaluate(
            """(id) => {
                const btn = document.querySelector(`[data-list-id="${id}"] button.delete`);
                btn?.click();
            }""",
            task_list.id,
        )
        assert dialog_seen["value"] is True
        assert List.objects.filter(pk=task_list.pk).exists()

    def test_reorder_lists_via_sidebar_drag_finalize(self, page, base_url, seed_full):
        data = seed_full
        page.goto(base_url)
        page.locator(f'[data-list-id="{data["list1"].id}"]').wait_for()
        page.locator(f'[data-list-id="{data["list2"].id}"]').wait_for()

        page.evaluate(
            """(ids) => {
                const zone = document.querySelector('.list-dnd-zone');
                zone.dispatchEvent(new CustomEvent('finalize', {
                    bubbles: true,
                    detail: { items: ids.map((id) => ({ id })) }
                }));
            }""",
            [data["list2"].id, data["list1"].id],
        )
        page.wait_for_timeout(400)

        fresh_from_db(data["list1"])
        fresh_from_db(data["list2"])
        assert data["list2"].position < data["list1"].position

    def test_emoji_picker_search_by_keyword(self, page, base_url):
        page.goto(base_url)

        page.locator("form.create-form button.emoji").click()
        search = page.locator('.picker input[placeholder="Search emoji..."]')
        search.fill("launch")

        rocket = page.locator('.picker button[aria-label="rocket"]')
        expect(rocket).to_be_visible()
        rocket.click()

        expect(page.locator("form.create-form button.emoji")).to_have_text("🚀")

    def test_only_one_list_inline_editor_active_at_a_time(self, page, base_url, seed_full):
        data = seed_full
        list1 = data["list1"]
        list2 = data["list2"]
        page.goto(base_url)

        row1 = page.locator(f'[data-list-id="{list1.id}"]')
        row2 = page.locator(f'[data-list-id="{list2.id}"]')

        row1.dblclick()
        row1.locator("input").fill("Renamed First")
        row2.dblclick()

        expect(page.locator('#sidebar [data-list-id] input')).to_have_count(1)
        page.wait_for_timeout(400)
        list1.refresh_from_db()
        assert list1.name == "Renamed First"

    def test_double_click_sidebar_emoji_opens_picker_and_updates(self, page, base_url, seed_list):
        task_list, _ = seed_list
        page.goto(base_url)

        row = page.locator(f'[data-list-id="{task_list.id}"]')
        row.locator("button.emoji-btn").dblclick()
        search = page.locator('.picker input[placeholder="Search emoji..."]')
        search.fill("house")
        page.locator('.picker button[aria-label="house"]').click()
        page.wait_for_timeout(300)

        task_list.refresh_from_db()
        assert task_list.emoji == "🏠"

    def test_double_click_content_header_emoji_updates(self, page, base_url, seed_list):
        task_list, _ = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator("button.list-emoji-btn").dblclick()
        page.locator('.picker input[placeholder="Search emoji..."]').fill("rocket")
        page.locator('.picker button[aria-label="rocket"]').click()
        page.wait_for_timeout(300)

        task_list.refresh_from_db()
        assert task_list.emoji == "🚀"
        expect(page.locator("#center-panel")).to_contain_text("To Do")

    def test_double_click_content_header_title_updates(self, page, base_url, seed_list):
        task_list, _ = seed_list
        page.goto(base_url)
        page.locator(f'[data-list-id="{task_list.id}"]').click()

        page.locator(".list-name").dblclick()
        page.locator(".list-name-input").fill("Renamed From Header")
        page.locator(".list-name-input").press("Enter")
        page.wait_for_timeout(300)

        task_list.refresh_from_db()
        assert task_list.name == "Renamed From Header"
        expect(page.locator("#center-panel")).to_contain_text("To Do")
