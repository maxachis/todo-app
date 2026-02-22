## 1. TypeaheadSelect Component

- [x] 1.1 Create `frontend/src/lib/components/shared/TypeaheadSelect.svelte` with text input, filtered dropdown, and highlight state
- [x] 1.2 Implement client-side filtering (case-insensitive substring match on option labels)
- [x] 1.3 Implement keyboard navigation: ArrowDown/ArrowUp to move highlight, Enter to select, Escape to close
- [x] 1.4 Implement action mode: `onSelect` callback fires on selection, input clears after
- [x] 1.5 Implement bound-value mode: `value` prop binding, display selected label, revert on Escape
- [x] 1.6 Add click-outside dismissal for the dropdown
- [x] 1.7 Prevent Enter from submitting parent forms when dropdown is open
- [x] 1.8 Add ARIA attributes: `role="combobox"`, `aria-expanded`, `aria-activedescendant`, `role="listbox"`/`role="option"` on dropdown items
- [x] 1.9 Style the component to match existing form element styles (border, radius, font from CSS custom properties)

## 2. LinkedEntities Integration

- [x] 2.1 Update `frontend/src/lib/components/shared/LinkedEntities.svelte` — replace `<select>` + `<button>` add-row with TypeaheadSelect in action mode
- [x] 2.2 Pass pre-filtered `available` entities as options with appropriate labels and placeholder text
- [x] 2.3 Verify task detail panel: adding/removing people and organizations still works via typeahead

## 3. Interactions Page Integration

- [x] 3.1 Update `frontend/src/routes/interactions/+page.svelte` — replace person `<select>` in create form with TypeaheadSelect in bound-value mode
- [x] 3.2 Replace interaction-type `<select>` in create form with TypeaheadSelect in bound-value mode
- [x] 3.3 Replace person `<select>` in edit form with TypeaheadSelect in bound-value mode
- [x] 3.4 Replace interaction-type `<select>` in edit form with TypeaheadSelect in bound-value mode
- [x] 3.5 Verify create and edit flows still submit correctly with typeahead-selected values

## 4. Organizations Page Integration

- [x] 4.1 Update `frontend/src/routes/organizations/+page.svelte` — replace org-type `<select>` in create form with TypeaheadSelect in bound-value mode
- [x] 4.2 Replace org-type `<select>` in edit form with TypeaheadSelect in bound-value mode
- [x] 4.3 Verify create and edit flows still submit correctly with typeahead-selected values

## 5. Testing and Verification

- [x] 5.1 Run `cd frontend && npm run check` to verify no TypeScript/lint errors
- [x] 5.2 Update E2E tests in `e2e/` that interact with entity selection dropdowns to use typeahead input selectors
- [ ] 5.3 Run `uv run python -m pytest e2e -q` to verify E2E tests pass (BLOCKED: Node.js preview server won't bind in devcontainer — pre-existing environment issue)
- [ ] 5.4 Manual smoke test: create interaction with typeahead person/type selection, edit organization with typeahead org-type, link person/org to task via typeahead in task detail
