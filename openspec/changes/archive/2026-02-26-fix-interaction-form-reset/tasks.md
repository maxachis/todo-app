## 1. Fix TypeaheadSelect bound-value reset

- [x] 1.1 In `frontend/src/lib/components/shared/TypeaheadSelect.svelte`, update the `$effect` on lines 52-56: remove the `selectedLabel` truthiness check so `displayText` is set to `selectedLabel` (including empty string) whenever `isBoundMode && !isOpen`

## 2. E2E test for consecutive interaction creation

- [x] 2.1 Add an E2E test in `e2e/` that creates an interaction, verifies the form resets (TypeaheadSelect inputs cleared), then creates a second interaction and verifies both appear in the list
