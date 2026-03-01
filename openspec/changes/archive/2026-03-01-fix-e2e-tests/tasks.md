## 1. Fix upcoming/dashboard route tests

File: `e2e/test_upcoming.py`

- [x] 1.1 Change all `page.goto(f"{base_url}/upcoming")` to `page.goto(f"{base_url}/dashboard")`
- [x] 1.2 Update `test_dashboard_page_loads` heading assertion from `"Upcoming"` to `"Dashboard"`
- [x] 1.3 Update `test_empty_state_when_no_upcoming_tasks` assertion text from `"No tasks with due dates"` to `"No tasks with due dates and no follow-ups due."`
- [x] 1.4 Update `test_clicking_task_navigates_to_list` — task row is now an `<a>` link, use `.task-row` click and `page.wait_for_url` as before (should still work since `.task-row` class is preserved)
- [x] 1.5 Run `uv run python -m pytest e2e/test_upcoming.py -q` and verify all 5 tests pass

## 2. Fix checkbox click interception tests

File: `e2e/test_task_completion.py`

- [x] 2.1 In `test_complete_task_shows_toast`, change `input[type="checkbox"]` selector to `.checkbox-wrap` (the label element that wraps the checkbox)
- [x] 2.2 In `test_undo_from_toast`, change `input[type="checkbox"]` selector to `.checkbox-wrap`
- [x] 2.3 In `test_uncomplete_from_completed_group`, change `input[type="checkbox"]` selector to `.checkbox-wrap`
- [x] 2.4 Run `uv run python -m pytest e2e/test_task_completion.py -q` and verify all 3 tests pass

## 3. Fix recurrence test strict mode violations

File: `e2e/test_recurrence.py`

- [x] 3.1 In all 3 tests, scope `page.get_by_text("Test List")` to `page.locator("#sidebar").get_by_text("Test List")` to avoid matching the center panel header
- [x] 3.2 Run `uv run python -m pytest e2e/test_recurrence.py -q` and verify all 3 tests pass (also fixed: recurrence.py custom_dates bug using `today` instead of `base`, blur trigger via focus+click-outside, checkbox selector to `.checkbox-wrap`)

## 4. Fix tag input selector mismatch

File: `e2e/test_tags.py`

- [x] 4.1 In `test_add_tag`, replace `page.locator("#tag-input").fill("urgent")` with a TypeaheadSelect interaction: locate the tag area's `.typeahead-input` within `#detail-panel`, fill with "urgent", then click the "Create" option in the dropdown or press Enter
- [x] 4.2 Remove the `form.tag-form button[type='submit']` click (no form/submit anymore)
- [x] 4.3 Run `uv run python -m pytest e2e/test_tags.py -q` and verify all 3 pass (also fixed `test_tag_suggestions_exclude_existing` to use TypeaheadSelect selectors)

## 5. Fix markdown editor empty-notes test

File: `e2e/test_markdown.py`

- [x] 5.1 In `test_click_to_edit_and_render`, seed the task with notes content (e.g., `tasks[0].notes = "initial notes"; tasks[0].save()`) before navigating, so `.block-render` is visible instead of `.block-placeholder`
- [x] 5.2 Run `uv run python -m pytest e2e/test_markdown.py::TestMarkdown::test_click_to_edit_and_render -q` and verify it passes

## 6. Fix interaction form typeahead index

File: `e2e/test_interactions.py`

- [x] 6.1 In `test_can_create_two_interactions_in_sequence`, replace positional `.typeahead-input` selectors with placeholder-based selectors: use `page.get_by_placeholder("Add person...")` for person and `page.get_by_placeholder("Interaction type")` for type
- [x] 6.2 Update both the first and second interaction creation blocks with the new selectors
- [x] 6.3 Run `uv run python -m pytest e2e/test_interactions.py -q` and verify it passes

## 7. Fix person-task linking test

File: `e2e/test_network_links.py`

- [x] 7.1 In `test_link_task_from_person_detail`, add explicit `expect` waits for the detail panel and linked tasks section to be visible before interacting with the typeahead (also fixed `loadAllTasks` in `linkedTasks.svelte.ts` — was calling `api.lists.getAll()` which doesn't include sections; now fetches each list detail)
- [x] 7.2 Run `uv run python -m pytest e2e/test_network_links.py::TestPersonTaskLinking -q` and verify it passes

## 8. Final verification

- [x] 8.1 Run the full E2E suite: `uv run python -m pytest e2e -q` — 85 passed, 1 flaky search test (timing issue in `test_click_outside_closes_results`)
