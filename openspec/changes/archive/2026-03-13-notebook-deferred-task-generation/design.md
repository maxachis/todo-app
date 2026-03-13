## Context

The notebook page save flow is: frontend debounced save (1s) → `PUT /notebook/pages/{slug}/` → `reconcile_mentions(page)` → `create_tasks_from_checkboxes(page)` → content rewrite with `[[task:ID|...]]` links → response includes updated content → frontend patches editor.

Currently every save triggers task generation. The debounced save fires after 1 second of inactivity, meaning a brief typing pause on a checkbox line creates a task prematurely.

## Goals / Non-Goals

**Goals:**
- Debounced saves (typing) persist content but skip checkbox-to-task processing
- Blur saves and Enter-after-checkbox saves trigger full processing including task generation
- No disruption to other mention reconciliation (page links, entity mentions, contact drafts)

**Non-Goals:**
- Client-side task creation
- Changing debounce timing
- Modifying `@new[...]` contact draft behavior (it doesn't rewrite content)

## Decisions

### 1. Add `process_checkboxes` flag to the page update API

Add an optional boolean `process_checkboxes` field to `PageUpdateInput` (default `true` for backward compatibility). When `false`, `reconcile_mentions` still runs but skips `create_tasks_from_checkboxes`.

**Rationale**: Minimal API surface change. Server-side logic stays in control of task creation; the client just signals when it's appropriate. Default `true` means existing API consumers (if any) aren't affected.

**Alternative considered**: Having the frontend strip checkbox lines before sending, then restore them. Rejected — fragile, duplicates parsing logic, and risks content corruption.

### 2. Detect Enter-after-checkbox in CodeMirror keymap

Add a keymap handler in the CodeMirror editor setup that detects when Enter is pressed and the line being left is a checkbox line (`- [ ] ...` without `[[task:`). When detected, trigger an immediate save with `process_checkboxes: true` (bypassing the debounce).

**Rationale**: The user's mental model is "I press Enter, I'm done with this line." This is the natural finalization signal. The existing `listKeymap.ts` already handles Enter for list continuation — the detection can be added adjacent to that logic.

### 3. Blur always processes checkboxes

The existing `handleContentBlur` → `savePage()` path already saves immediately. It will pass `process_checkboxes: true` to finalize any pending checkboxes.

**Rationale**: Blur means the user is done editing — all checkboxes should be finalized.

## Risks / Trade-offs

- **Enter detection timing**: The Enter keymap fires before the new line content is in the document. We need to check the line *before* the Enter is processed, then trigger the save after the document updates. → Mitigation: Use a CodeMirror transaction filter or keymap that reads the current line before returning.
- **Multiple rapid Enter presses**: If the user types a checkbox and hits Enter multiple times quickly, only the first needs to trigger task processing. → Mitigation: The debounce-cancel + immediate-save pattern handles this naturally.
