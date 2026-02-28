## Context

TypeaheadSelect operates in two modes: action mode (`onSelect` callback, clears on select) and bound-value mode (`bind:value`, displays selected label). In bound-value mode, when the dropdown closes (blur/click-outside/Tab), an `$effect` restores `displayText` to `selectedLabel`. If no value was previously selected, `selectedLabel` is `''`, silently erasing whatever the user typed.

This affects every bound-value TypeaheadSelect across the app: org type selectors (Organizations, Interactions), person/org selectors (Relationships, Leads), and interaction type selectors (People quick-log).

## Goals / Non-Goals

**Goals:**
- When `onCreate` is available and the user blurs with unmatched text, auto-create the item rather than discarding input
- When `onCreate` is NOT available and the user blurs with unmatched text, revert to the previous selection (if any) or clear the field, but do so in a way that doesn't feel like input was "eaten" — show a brief toast notification
- Keep Escape behavior unchanged (explicit cancel intent)

**Non-Goals:**
- Supporting free-text values in TypeaheadSelect — it remains a selector
- Changing action mode blur behavior
- Modifying dropdown filtering, keyboard navigation, or creation flow

## Decisions

### Decision 1: Auto-create on blur when `onCreate` is available

When the user types unmatched text and blurs a TypeaheadSelect that has `onCreate`, the component will automatically call `onCreate` with the trimmed text. This matches user intent — they typed a value and moved on, expecting it to stick.

**Alternative considered**: Preserve text with a warning style. Rejected because the user's clear intent is to use the typed value, and requiring them to explicitly click "Create" is an unnecessary extra step. The "Create" option in the dropdown is still available for users who prefer explicit confirmation.

### Decision 2: Revert with toast when no `onCreate` available

When `onCreate` is NOT provided and the user blurs with unmatched text, the component reverts to the previous selection (or empty). A toast notification ("No match found for '[text]'") informs the user their input wasn't accepted, preventing the silent-erasure confusion.

**Alternative considered**: Keep the unmatched text in the input with a red border. Rejected because the component is a selector — displaying unresolvable text creates an inconsistent state where `value` and `displayText` disagree.

### Decision 3: Modify the `$effect` and blur handlers, not the architecture

The fix is localized to `TypeaheadSelect.svelte`:
- `handleClickOutside` and Tab in `handleKeydown`: add auto-create logic before falling through to close
- The `$effect` that restores `displayText` remains — it correctly syncs display with the bound value after close

No changes needed to parent components since the auto-create uses the existing `onCreate` contract.

## Risks / Trade-offs

- **Auto-create on accidental blur** → Mitigation: This matches the user's intent in the vast majority of cases. The created item is visible in the dropdown and can be managed. In this single-user app, accidental creation is low-cost.
- **Toast noise on blur without `onCreate`** → Mitigation: Only show toast when `inputText` differs from previous selection. Normal blur (no typing) won't trigger it.
- **Race condition if user blurs during ongoing create** → Mitigation: The existing `creating` guard prevents duplicate calls. The `$effect` will sync display text once the create completes and `value` updates.
