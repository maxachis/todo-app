## 1. Fix hasExactMatch Comparison

- [x] 1.1 In `frontend/src/lib/components/shared/TypeaheadSelect.svelte`, change `hasExactMatch` derived state to compare `inputText.toLowerCase()` (untrimmed) instead of `inputText.trim().toLowerCase()` — keep the `inputText.trim() !== ''` empty-guard unchanged
- [ ] 1.2 Manually verify: open a bound-value TypeaheadSelect with `onCreate` (e.g., interaction type field), type an existing option name, then continue typing beyond it — input should not erase and "Create" option should appear

## 2. Verify No Regressions

- [ ] 2.1 Verify blur behavior: type "LinkedIn " (with trailing space) and blur — should auto-select "LinkedIn" via `handleBlur` trimmed match
- [ ] 2.2 Verify exact match suppresses Create: type exactly "LinkedIn" (no extra chars) — "Create" option should NOT appear
- [x] 2.3 Run `cd frontend && npm run check` to confirm no type errors
- [x] 2.4 Run E2E tests (`uv run python -m pytest e2e -q`) to confirm no regressions
