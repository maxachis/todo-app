## Context

The `TypeaheadSelect` component has a `hasExactMatch` derived state that determines whether the typed text exactly matches an existing option. It's used to suppress the "Create" dropdown item when the user has typed a name identical to an existing option.

Currently, `hasExactMatch` trims whitespace from the input before comparing:

```typescript
const hasExactMatch = $derived(
    inputText.trim() !== '' &&
        options.some((o) => o.label.toLowerCase() === inputText.trim().toLowerCase())
);
```

However, `filtered` (which controls which options appear in the dropdown) uses the **untrimmed** `inputText`:

```typescript
const filtered = $derived(
    inputText
        ? options.filter((o) => o.label.toLowerCase().includes(inputText.toLowerCase()))
        : options
);
```

This mismatch causes a bug: when the user types "LinkedIn " (with a trailing space), `hasExactMatch` is `true` (because trimmed text matches) but `filtered` is empty (because no label contains "linkedin " as a substring). Since `showCreateOption` requires `!hasExactMatch`, it stays `false`. With `filtered` empty and `showCreateOption` false, `handleInput` sets `isOpen = false`, triggering the `$effect` that overwrites `displayText` with `selectedLabel` (empty if nothing was previously selected), erasing the input.

## Goals / Non-Goals

**Goals:**
- Allow users to type beyond an existing option name (e.g., "LinkedIn" → "LinkedIn Connection") without the input being erased.
- Preserve the "Create" option in the dropdown when the user is still typing.

**Non-Goals:**
- Changing blur behavior — on blur, trimmed-text exact-match auto-select is correct and intentional.
- Modifying the `$effect` that syncs `displayText` when the dropdown closes — the fix targets the root cause (premature dropdown close), not the symptom.

## Decisions

**Use untrimmed comparison in `hasExactMatch`**: Change `inputText.trim().toLowerCase()` to `inputText.toLowerCase()` in the comparison (keep `inputText.trim() !== ''` for the empty check). This means "LinkedIn " won't be an exact match for "LinkedIn", so `showCreateOption` remains `true` and the dropdown stays open.

Alternative considered: Adding a separate guard in `handleInput` to keep the dropdown open when `hasExactMatch` is true but `filtered` is empty. Rejected because it treats the symptom (dropdown closing) rather than the root cause (`hasExactMatch` incorrectly returning `true` for partial input).

Alternative considered: Guarding the `$effect` to skip when the input is focused. Rejected because it adds complexity and the effect behavior is correct — the real issue is `isOpen` being set to `false` prematurely.

## Risks / Trade-offs

- **Trimmed-input edge case**: A user who types "LinkedIn " (with trailing space) will now see a "Create" option instead of the dropdown closing. On blur, the `handleBlur` function still uses trimmed text to find an exact match, so tabbing away will correctly auto-select "LinkedIn". → Acceptable behavior: the user sees the Create option while typing but gets the right thing on blur.
- **Minimal blast radius**: Only `hasExactMatch` changes; `filtered`, `handleBlur`, and `selectOption` remain unchanged. All other TypeaheadSelect behaviors (action mode, keyboard nav, blur logic) are unaffected.
