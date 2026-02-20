"""E2E tests for global search interactions."""

from playwright.sync_api import expect


class TestSearch:
    def test_search_shows_results(self, page, base_url, seed_list_with_tasks):
        page.goto(base_url)

        page.locator(".search-input").fill("groceries")
        expect(page.locator(".results-dropdown")).to_contain_text("Buy groceries")

    def test_click_result_navigates_to_task(self, page, base_url, seed_full):
        page.goto(base_url)

        page.locator(".search-input").fill("Review PRs")
        expect(page.locator(".results-dropdown .result")).to_contain_text("Review PRs")
        page.locator('.results-dropdown .result:has-text("Review PRs")').click()

        expect(page.locator("#center-panel")).to_contain_text("Work")
        expect(page.locator("#detail-title")).to_have_value("Review PRs")

    def test_click_outside_closes_results(self, page, base_url, seed_list_with_tasks):
        page.goto(base_url)

        page.locator(".search-input").fill("groceries")
        expect(page.locator(".results-dropdown")).to_be_visible()
        page.locator("#center-panel").click()
        expect(page.locator(".results-dropdown")).to_have_count(0)
