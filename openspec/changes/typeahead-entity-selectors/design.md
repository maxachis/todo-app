## Context

The app currently uses native HTML `<select>` elements for all entity selection: people and organizations in LinkedEntities.svelte (task detail panel), person and interaction-type selectors in the Interactions page, and org-type selector in the Organizations page. All entity data is loaded upfront via `getAll()` API calls and filtered client-side. The dataset is small (single-user app), so server-side search is unnecessary.

The current `<select>` elements provide no filtering — users must scroll through full lists. As entity counts grow, this becomes increasingly slow and cumbersome.

## Goals / Non-Goals

**Goals:**
- Replace native `<select>` entity selectors with a typeahead component across three contexts: LinkedEntities (task detail), Interactions page forms, Organizations page forms
- Provide keyboard-driven selection: type to filter, arrow keys to navigate, Enter to select, Escape to dismiss
- Maintain existing behavior: entity exclusion (already-linked items hidden), immediate API calls on selection, same visual weight
- Keep the component reusable for any `{ id, label }` option list

**Non-Goals:**
- Server-side search or API-backed filtering (all data remains client-side)
- Replacing priority dropdown, tag input, or project selector
- Adding inline entity creation ("create new" from typeahead)
- Debouncing or async option loading
- Third-party library dependencies (e.g., svelte-select)

## Decisions

### 1. Single reusable TypeaheadSelect component

**Decision:** Create one `TypeaheadSelect.svelte` component in `frontend/src/lib/components/shared/` that handles all typeahead behavior.

**Rationale:** All six replacement points (LinkedEntities add-person, add-org; Interactions create/edit person, create/edit type; Organizations create/edit org-type) share identical interaction patterns. A single component avoids duplication and ensures consistent behavior.

**Alternatives considered:**
- Enhance LinkedEntities directly — rejected because Interactions/Organizations pages use standalone `<select>` elements, not LinkedEntities
- Use HTML `<datalist>` (like tag input) — rejected because `<datalist>` has limited styling control, no keyboard-highlighted item state, and inconsistent behavior across browsers

### 2. Component API design

**Decision:** The component accepts a flat array of options, a placeholder, and fires events on selection:

```typescript
props: {
  options: { id: number; label: string }[];  // filtered externally
  placeholder?: string;                       // e.g. "Add person..."
  onSelect: (id: number) => void;            // fired on Enter or click
  value?: number | null;                      // for bound-value mode (forms)
}
```

Two usage modes:
- **Action mode** (LinkedEntities): `onSelect` fires, input clears, no persistent value. Parent passes pre-filtered options (excluding already-linked entities).
- **Bound-value mode** (Interactions/Organizations forms): `value` is bound to a form variable. Selecting an option updates `value` and displays the selected label. Used where the select controls a form field rather than triggering an immediate action.

**Rationale:** LinkedEntities needs fire-and-forget selection (add a link). Form selects need persistent value binding (person_id for an interaction). Supporting both in one component keeps things simple.

**Alternatives considered:**
- Two separate components — rejected, the logic overlap is ~90%
- Always use `onSelect` and let parents manage display — more boilerplate in form contexts

### 3. Client-side filtering with case-insensitive substring match

**Decision:** Filter options using case-insensitive substring match on the label. No fuzzy matching.

**Rationale:** The dataset is small (single-user, likely <500 entities). Substring match is simple, predictable, and sufficient. Fuzzy matching adds complexity without clear benefit at this scale.

### 4. Keyboard navigation

**Decision:** Standard typeahead keyboard interactions:
- **ArrowDown/ArrowUp**: Move highlight through filtered results
- **Enter**: Select highlighted item (or first item if none highlighted)
- **Escape**: Close dropdown, clear input (action mode) or revert to selected label (bound-value mode)
- **Tab**: Close dropdown without selecting (preserve form navigation)

The dropdown opens when the input receives focus and has options available.

**Rationale:** This follows established typeahead conventions (e.g., GitHub issue references, VS Code command palette).

### 5. Integration approach for LinkedEntities

**Decision:** Replace the `<select>` + `<button>` add-row in LinkedEntities.svelte with a single TypeaheadSelect in action mode. The parent component (LinkedEntities) continues to handle filtering out already-linked entities and passing the `onAdd` callback.

**Rationale:** LinkedEntities already manages the available/linked split. TypeaheadSelect just needs to present the filtered list and fire `onSelect`. The "+" button is no longer needed since Enter/click in the typeahead directly triggers the action.

### 6. Integration approach for Interactions / Organizations pages

**Decision:** Replace each standalone `<select>` with a TypeaheadSelect in bound-value mode. The `value` prop binds to the same state variables (`newPersonId`, `editPersonId`, `newTypeId`, `editTypeId`, `newOrgTypeId`, `editOrgTypeId`).

**Rationale:** This is a drop-in replacement — the parent form logic stays identical, only the selector element changes.

## Risks / Trade-offs

- **Accessibility gap vs. native `<select>`**: Native selects get free screen-reader support. The typeahead needs manual ARIA attributes (`role="combobox"`, `aria-expanded`, `aria-activedescendant`, `listbox`/`option` roles) → Mitigated by including ARIA attributes in the component spec.
- **Click-outside dismissal**: Dropdown must close when clicking outside. Using a Svelte action or window click handler could interfere with other components → Mitigated by scoping the listener to the component lifecycle.
- **Form submission with Enter**: In bound-value mode inside a `<form>`, pressing Enter to select a typeahead option could also submit the form → Mitigated by calling `event.preventDefault()` on keydown when the dropdown is open.
- **E2E test breakage**: Tests that interact with `<select>` elements will break → Expected and documented. Tests need updating to type into inputs and select from the dropdown.
