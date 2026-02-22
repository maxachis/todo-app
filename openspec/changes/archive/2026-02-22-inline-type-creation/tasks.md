## 1. TypeaheadSelect Component Enhancement

- [x] 1.1 Add optional `onCreate` prop (`(name: string) => Promise<{ id: number; label: string }>`) to TypeaheadSelect component (`frontend/src/lib/components/shared/TypeaheadSelect.svelte`)
- [x] 1.2 Add `hasExactMatch` derived that checks if any option label matches the trimmed input text exactly (case-insensitive)
- [x] 1.3 Add `showCreateOption` derived: true when `onCreate` is provided, input is non-empty after trimming, and `hasExactMatch` is false
- [x] 1.4 Update the dropdown open logic so the dropdown stays open when `showCreateOption` is true even if `filtered` is empty
- [x] 1.5 Render a "Create [typed text]" item at the bottom of the dropdown when `showCreateOption` is true, styled distinctly from regular options
- [x] 1.6 Make the create item participate in keyboard navigation (ArrowDown/ArrowUp/Enter) alongside regular filtered options
- [x] 1.7 When the create item is selected (click or Enter), call `onCreate` with the trimmed text, await the result, and select the returned `{ id, label }` as the current value (bound-value mode) or fire `onSelect` (action mode)

## 2. Organizations Page Wiring

- [x] 2.1 Remove the standalone "Create Org Type" form (the `createOrgType` function, `newTypeName` state, and the `<form>` with input + `+ Type` button) from `frontend/src/routes/organizations/+page.svelte`
- [x] 2.2 Add an `onCreate` handler for the org type TypeaheadSelect in the create form that calls `api.orgTypes.create({ name })`, appends to `orgTypes`, and returns `{ id, label }`
- [x] 2.3 Add the same `onCreate` handler for the org type TypeaheadSelect in the edit/detail form

## 3. Interactions Page Wiring

- [x] 3.1 Remove the standalone "Create Interaction Type" form (the `createInteractionType` function, `newTypeName` state, and the `<form>` with input + `+ Type` button) from `frontend/src/routes/interactions/+page.svelte`
- [x] 3.2 Add an `onCreate` handler for the interaction type TypeaheadSelect in the create form that calls `api.interactionTypes.create({ name })`, appends to `interactionTypes`, and returns `{ id, label }`
- [x] 3.3 Add the same `onCreate` handler for the interaction type TypeaheadSelect in the edit/detail form

## 4. Verification

- [x] 4.1 Verify org type inline creation works on Organizations page (create form): type a new name, see "Create" option, select it, confirm type is created and selected
- [x] 4.2 Verify org type inline creation works on Organizations page (edit form): same flow in the detail panel
- [x] 4.3 Verify interaction type inline creation works on Interactions page (create form): same flow
- [x] 4.4 Verify interaction type inline creation works on Interactions page (edit form): same flow
- [x] 4.5 Verify "Create" option does NOT appear when an exact match exists
- [x] 4.6 Verify keyboard navigation works through filtered options and the "Create" item
- [x] 4.7 Run `cd frontend && npm run check` to verify no type errors
