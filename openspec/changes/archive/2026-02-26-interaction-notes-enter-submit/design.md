## Context

The interaction create form (`frontend/src/routes/interactions/+page.svelte`, lines 140–155) has four fields: Person (TypeaheadSelect), Interaction type (TypeaheadSelect), Date (input), and Notes (textarea), followed by a "+ Interaction" submit button. Currently the only way to submit is clicking the button. The notes textarea treats Enter as a newline character.

Other forms in the app already use Enter-to-submit (e.g., project name inline editing in `frontend/src/routes/projects/+page.svelte`). The TypeaheadSelect component already intercepts Enter when its dropdown is open to select an option, so it won't conflict.

## Goals / Non-Goals

**Goals:**
- Enable Enter key in the notes textarea to submit the interaction create form
- Preserve multi-line note entry via Shift+Enter

**Non-Goals:**
- Changing the edit/detail panel form (right panel) — it uses a separate Save button and auto-save on blur
- Adding Enter-to-submit on the People page "Quick Log Interaction" form
- Adding markdown rendering to the notes field

## Decisions

### 1. Handle keydown on the textarea element directly

**Decision**: Add an `onkeydown` handler to the `<textarea>` in the create form (line 153).

**Rationale**: This is the simplest approach — a single event handler on the specific element. No need for a form-level listener or a Svelte action. This matches the pattern used in the projects page for inline editing.

**Alternatives considered**:
- **Svelte action**: Overkill for a single element with one handler
- **Form-level keydown**: Would need to distinguish which field the user is in, adding unnecessary complexity

### 2. Enter submits, Shift+Enter inserts newline

**Decision**: On keydown, if `key === 'Enter'` and `!shiftKey`, call `preventDefault()` and programmatically submit the form by calling `createInteraction()` directly.

**Rationale**: This is the standard UX convention for chat-like inputs. Shift+Enter naturally inserts a newline in a textarea without any extra code — we just need to avoid intercepting it.

### 3. Call createInteraction() directly rather than form.submit()

**Decision**: Call the `createInteraction` function directly from the keydown handler, passing a synthetic event or using the existing form reference.

**Rationale**: The `createInteraction` function already handles `preventDefault()` and validation. Calling it directly keeps the logic in one place. We'll use `form.requestSubmit()` to trigger the form's `onsubmit` handler naturally, which is cleaner than passing a synthetic event.

## Risks / Trade-offs

- **Multi-line notes friction**: Users who frequently write multi-line notes will need to use Shift+Enter. This is a well-understood convention (Slack, Discord, etc.) and the trade-off favors speed of entry. → Mitigation: Shift+Enter behavior is intuitive and widely known.
- **No visual hint**: There's no visible indicator that Enter submits. → Acceptable for a single-user app; the behavior is discoverable and matches modern form conventions.
