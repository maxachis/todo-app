## Context

The `TaskCreateForm` component currently renders a text input and a "+" submit button. It sends `{ title, parent_id? }` to `POST /sections/{section_id}/tasks/`. Due dates can only be set after creation via the task detail panel's date input, which calls `PATCH /tasks/{task_id}/`.

The Task model already has `due_date` (DateField, nullable) and `due_time` (TimeField, nullable). The update endpoint and detail panel already handle these fields. The creation path simply doesn't expose them yet.

## Goals / Non-Goals

**Goals:**
- Allow setting an optional due date inline when creating a task
- Preserve the existing fast "type and press Enter" workflow — the date field must not get in the way
- Keep the UI compact, especially on mobile where the form is already tight

**Non-Goals:**
- Adding inline due *time* selection (can still be set in the detail panel)
- Adding recurrence settings at creation time
- Replacing or modifying the detail panel's date picker
- Custom date picker component — native `<input type="date">` is sufficient and consistent with the detail panel

## Decisions

### 1. Native `<input type="date">` element
**Choice**: Use the browser's native date input, same as the detail panel.
**Rationale**: No new dependencies, consistent UX, good mobile support with native date picker dialogs. The detail panel already uses this pattern (`TaskDetail.svelte:163`).
**Alternative considered**: A custom calendar dropdown — rejected as over-engineered for a single-user app with no special date-picking needs.

### 2. Date input positioned between text input and "+" button
**Choice**: Place the date input to the right of the title field, left of the submit button: `[title] [date] [+]`.
**Rationale**: Keeps the natural left-to-right flow (type title → optionally pick date → submit). The date input is visually secondary to the title.

### 3. Date field included in the create API payload
**Choice**: Add optional `due_date: date | None` to `TaskCreateInput` schema and pass it through to `Task.objects.create()`.
**Rationale**: Single round-trip instead of create-then-update. The field is already on the model; we're just exposing it at creation time. No migration needed.
**Alternative considered**: Create task then immediately PATCH the date — rejected as unnecessary complexity with two API calls.

### 4. Date field clears after submission
**Choice**: Reset the date input to empty after each task is created (same as the title field).
**Rationale**: Each new task should start fresh. If a user is batch-creating tasks for the same date, they can set it each time — this is simpler than "sticky date" behavior which would need additional UX to clear.

### 5. Compact styling with placeholder text
**Choice**: Style the date input to be compact with reduced width. When empty, native date inputs show a placeholder format (e.g., "mm/dd/yyyy").
**Rationale**: The form row needs to stay single-line. The date input should be visually lightweight when unused so it doesn't clutter the quick-add experience.

## Risks / Trade-offs

- **Slightly wider form row** → On very narrow screens the three elements may feel cramped. Mitigation: use CSS to give the date input a constrained max-width and allow the title input to flex.
- **Native date input styling varies by browser** → Acceptable trade-off for a single-user app; the detail panel already accepts this variance.
- **No "sticky date" for batch entry** → Users adding many tasks for the same date must re-select it each time. This keeps the UX simpler and can be revisited if it becomes a pain point.
