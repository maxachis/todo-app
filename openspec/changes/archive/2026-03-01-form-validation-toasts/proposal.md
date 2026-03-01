## Why

Every form in the app silently fails when required fields are empty — the submit handler returns early with zero feedback. Users get no indication why their action didn't work, which is confusing and feels broken. The existing toast system is already wired up but only fires for API errors, never for client-side validation.

## What Changes

- Add `error` toast notifications when a form submission is blocked by missing required fields (e.g., "First name and last name are required").
- Extract a shared `validateRequired` helper so each form doesn't hand-roll its own `.trim()` / null-check logic.
- No changes to the toast component or store API — the existing `addToast({ message, type: 'error' })` pattern is sufficient.

## Non-goals

- Field-level inline error styling (red borders, helper text beneath inputs). This is a future enhancement; toasts are the minimal viable feedback.
- Adding HTML `required` attributes or browser-native validation — the app uses custom submit handlers that call `preventDefault()`, so native validation wouldn't fire.
- Changing how API errors (409, 422, etc.) are displayed — that's a separate concern.

## Capabilities

### New Capabilities

- `form-validation-feedback`: Shared validation helper and toast-based error messages for all create/edit forms.

### Modified Capabilities

_(none — no existing spec-level requirements change; this adds feedback to existing validation logic)_

## Impact

- **Frontend forms touched** (~12 submit handlers across 8 route files + 2 components):
  - `routes/crm/people/+page.svelte` — create person, quick-log interaction
  - `routes/crm/orgs/+page.svelte` — create organization
  - `routes/crm/interactions/+page.svelte` — create interaction
  - `routes/crm/leads/+page.svelte` — create lead
  - `routes/network/relationships/+page.svelte` — create person-person, create org-person
  - `routes/projects/+page.svelte` — create project, add project link
  - `routes/timesheet/+page.svelte` — create time entry
  - `lib/components/tasks/TaskCreateForm.svelte` — create task
  - `lib/components/lists/ListSidebar.svelte` — create list
- **New file**: `lib/utils/validation.ts` (shared helper)
- **No backend changes** — all validation is already enforced server-side; this change adds client-side user feedback only.
- **No new dependencies.**
