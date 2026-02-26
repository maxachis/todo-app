## Context

The `TypeaheadSelect` component supports two modes: action mode (fire-and-forget) and bound-value mode (form field). In bound-value mode, a `$effect` syncs `displayText` from the derived `selectedLabel` — but only when `selectedLabel` is truthy. When a parent form resets `value` to `null` after submission, `selectedLabel` becomes `''` (falsy), so the effect never fires and `displayText` retains the stale label.

The interactions page (`/interactions`) uses two TypeaheadSelect components in bound-value mode (person and type). After creating an interaction, it sets `newPersonId = null` and `newTypeId = null`, but the inputs still show the previous selections.

## Goals / Non-Goals

**Goals:**
- TypeaheadSelect clears `displayText` when bound `value` is externally set to `null`
- Fix applies generically in the component, not with a form-specific workaround
- E2E test covers consecutive interaction creation

**Non-Goals:**
- Changing TypeaheadSelect action mode behavior
- Refactoring the interactions page form structure
- Adding unit tests for TypeaheadSelect (E2E covers the user-facing behavior)

## Decisions

### 1. Fix the `$effect` condition to handle null values

**Decision**: Simplify the `$effect` on lines 52-56 to always assign `displayText = selectedLabel` in bound-value mode when the dropdown is closed, regardless of whether `selectedLabel` is truthy.

**Current code:**
```js
$effect(() => {
    if (isBoundMode && !isOpen && selectedLabel) {
        displayText = selectedLabel;
    }
});
```

**Fixed code:**
```js
$effect(() => {
    if (isBoundMode && !isOpen) {
        displayText = selectedLabel;
    }
});
```

**Rationale**: Removing the `selectedLabel` truthiness check means the effect fires when `value` becomes `null` (and `selectedLabel` is `''`), clearing `displayText`. This is the correct behavior — if the parent says the value is null, the display should be empty. The effect already guards on `isBoundMode` and `!isOpen`, which are the meaningful conditions.

**Alternatives considered:**
- Adding a separate `$effect` watching only `value` for null → more code, same result, two effects competing over `displayText`
- Clearing `displayText` from the parent form → leaks component internals, each consumer would need the workaround

### 2. E2E test for consecutive interaction creation

**Decision**: Add a pytest E2E test that creates two interactions in sequence, verifying the form clears and the second interaction appears in the list.

**Rationale**: This is the exact user scenario that's broken. The test will catch regressions in both the TypeaheadSelect reset logic and the form submission flow.

## Risks / Trade-offs

- **Risk**: Removing the truthiness check could cause `displayText` to be set to `''` during initial render before a value is selected → **Mitigation**: On initial render with no value, `selectedLabel` is already `''` and `displayText` is already `''`, so this is a no-op. When a value is pre-set on mount, `selectedLabel` resolves to the label, so `displayText` gets correctly populated.
- **Risk**: The effect firing on every close could overwrite user typing → **Mitigation**: The `!isOpen` guard means this only fires when the dropdown closes. During typing, `isOpen` is true, so the effect doesn't interfere.
