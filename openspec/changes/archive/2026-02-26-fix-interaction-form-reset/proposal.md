## Why

After successfully creating an interaction, the form resets its bound values (`newPersonId`, `newTypeId`, etc.) to `null`, but the TypeaheadSelect component does not clear its `displayText` when the bound `value` changes to `null` externally. This leaves stale text in the person and type fields, making it appear the form hasn't reset and preventing users from adding a second interaction without a page refresh.

## What Changes

- Fix the `$effect` in `TypeaheadSelect.svelte` (bound-value mode) so that when `value` becomes `null` externally, `displayText` is cleared
- Add an E2E test that creates two interactions in sequence to prevent regression

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `typeahead-selector`: Add requirement that bound-value mode clears display text when the external `value` prop is set to `null`

## Impact

- **Code**: `frontend/src/lib/components/shared/TypeaheadSelect.svelte` — `$effect` on lines 52-56
- **Affected forms**: Any form using TypeaheadSelect in bound-value mode that resets `value` to `null` after submission (interactions page, potentially others)
- **Tests**: New E2E test for consecutive interaction creation
