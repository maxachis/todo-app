## 1. Auto-create on blur in bound-value mode

- [x] 1.1 In `TypeaheadSelect.svelte`, update `handleClickOutside` to call `handleCreate()` when in bound-value mode with `onCreate`, unmatched non-empty `inputText`, and not already `creating`
- [x] 1.2 In `TypeaheadSelect.svelte`, update the `Tab` case in `handleKeydown` to apply the same auto-create-on-blur logic before closing
- [x] 1.3 Add blur-with-exact-match auto-select: in `handleClickOutside` and `Tab`, if `inputText` exactly matches (case-insensitive) an existing option, call `selectOption` with that option

## 2. Revert with toast when no onCreate

- [x] 2.1 Accept an optional `onUnmatched` callback prop (or import `addToast` directly) to show a toast when blur discards unmatched text in bound-value mode without `onCreate`
- [x] 2.2 In `handleClickOutside` and `Tab` handler, when no `onCreate` and `inputText` is non-empty and unmatched, call the toast/callback before reverting

## 3. Guard against no-op creates

- [x] 3.1 Ensure auto-create on blur does NOT fire when `inputText` is empty or whitespace-only
- [x] 3.2 Ensure auto-create on blur does NOT fire when `creating` is already true (prevent double-create)
- [x] 3.3 Ensure the `$effect` that restores `displayText` still works correctly after auto-create completes (value updates → selectedLabel updates → displayText syncs)

## 4. Testing

- [ ] 4.1 Manually verify on Organizations page: type a new org type, click away → org type is auto-created and selected
- [ ] 4.2 Manually verify on Relationships page: type a non-existent organization name, click away → toast appears, field reverts
- [ ] 4.3 Manually verify Tab key triggers the same behavior as click-outside
- [ ] 4.4 Manually verify Escape still reverts without creating
- [ ] 4.5 Verify that typing an exact match and blurring auto-selects the matching option
