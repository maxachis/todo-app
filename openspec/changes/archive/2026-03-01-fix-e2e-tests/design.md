## Context

16 E2E tests are failing due to selector and URL drift between the Playwright tests and the current SvelteKit frontend. The application code is correct — only the test files need updating. The root causes were identified through investigation and fall into 7 categories.

## Goals / Non-Goals

**Goals:**
- All 16 failing E2E tests pass against the current UI
- Tests use resilient selectors that match the actual component structure

**Non-Goals:**
- No application code changes
- Not adding new test coverage
- Not addressing the flaky `test_search.py` (passes solo, occasionally fails in batch)

## Decisions

### 1. Checkbox clicks: use `.checkbox-wrap` label selector
The native `input[type="checkbox"]` is visually hidden (1×1px, `clip-path: inset(50%)`) with a custom `.checkbox-custom` + SVG overlay. Clicking the wrapping `<label class="checkbox-wrap">` is the most reliable approach — it mirrors real user behavior and triggers the native input's `onchange` via label association.

**Alternative considered**: `force: true` on the hidden input click — rejected because it bypasses actionability checks and doesn't reflect real user interaction.

### 2. Strict mode: scope selectors to `#sidebar`
`get_by_text("Test List")` matches both the sidebar list name and a center panel header button. Scoping to `page.locator("#sidebar").get_by_text("Test List")` eliminates ambiguity.

### 3. Tag input: use TypeaheadSelect interaction pattern
Tags switched from a dedicated `#tag-input` + form submit to the shared `TypeaheadSelect` component. Tests should type into the tag-area `.typeahead-input`, then either press Enter or click the dropdown option to add.

### 4. Markdown editor: seed task with notes or click placeholder
When notes are empty, MarkdownEditor renders `.block-placeholder` not `.block-render`. Seeding the task with notes content is the cleanest fix — it tests the intended flow (editing existing notes).

### 5. Interaction form: use placeholder-based selectors
The form now has 4 TypeaheadSelect fields (person, org, type, medium). Using `page.get_by_placeholder("Interaction type")` is more resilient than positional `.nth(N)` indexing.

### 6. Upcoming route: update path from `/upcoming` to `/dashboard`
Straightforward URL update. Also verify the page heading and CSS class names still match.

### 7. Person-task linking: add explicit waits
The linked tasks section loads asynchronously. Adding `expect(...).to_be_visible()` waits before interacting will handle the timing issue.

## Risks / Trade-offs

- [Risk] Dashboard page content (H1, class names) may have changed beyond just the URL → Mitigation: verify selectors against current `dashboard/+page.svelte` during implementation
- [Risk] TypeaheadSelect interaction timing in tag test → Mitigation: use Playwright's built-in auto-waiting via `expect` assertions before acting
