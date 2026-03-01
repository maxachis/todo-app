## Why

16 E2E tests are failing because the test selectors and URLs have drifted from the current frontend implementation. UI components were refactored (custom checkbox, TypeaheadSelect for tags, additional form fields on interactions) and routes were renamed (`/upcoming` → `/dashboard`), but the corresponding E2E tests were not updated.

## What Changes

- Update 5 `test_upcoming.py` tests to use `/dashboard` route instead of `/upcoming`
- Fix 3 `test_task_completion.py` tests to click the visible checkbox element (`.checkbox-wrap` or `.checkbox-custom`) instead of the hidden `input[type="checkbox"]`
- Fix 3 `test_recurrence.py` tests to scope `get_by_text("Test List")` to the sidebar to avoid strict mode violations (2 elements match)
- Rewrite `test_tags.py::test_add_tag` to use TypeaheadSelect interaction pattern (`.typeahead-input` + Enter/click) instead of the removed `#tag-input` / `form.tag-form`
- Fix `test_markdown.py::test_click_to_edit_and_render` to handle empty notes (click `.block-placeholder` instead of `.block-render`, or seed task with notes)
- Fix `test_interactions.py` to account for new org and medium TypeaheadSelect fields (type is now at index 2, not index 1)
- Fix `test_network_links.py::TestPersonTaskLinking` timing/selector issues for linked tasks section

## Non-goals

- No changes to application code — only E2E test files are modified
- No new test coverage — just fixing existing tests to match current UI
- Not addressing `test_search.py` flakiness (passes when run solo)

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

(none — this is a test-only change with no requirement or spec-level modifications)

## Impact

- **Files changed**: `e2e/test_upcoming.py`, `e2e/test_task_completion.py`, `e2e/test_recurrence.py`, `e2e/test_tags.py`, `e2e/test_markdown.py`, `e2e/test_interactions.py`, `e2e/test_network_links.py`
- **No application code changes**
- **No API changes**
- **No dependency changes**
