## Why

When a user tries to create a person or organization that already exists (matching the database unique constraints), the API returns a 500 error that is silently swallowed — leaving the user with no feedback about what went wrong. This should surface a clear, friendly toast notification instead of failing silently.

## What Changes

- Backend API endpoints for creating people and organizations will check for existing duplicates before attempting to insert, and return a 409 Conflict response with a descriptive message.
- Frontend creation handlers will catch duplicate errors and display a warning toast (e.g., "A person named John Smith already exists") instead of failing silently.
- Person duplicate detection: matching `first_name` + `last_name` (case-insensitive).
- Organization duplicate detection: matching `name` (case-insensitive).

## Non-goals

- Merge/deduplication workflows (suggesting the user link to the existing entity).
- Fuzzy/partial name matching (only exact match, case-insensitive).
- Duplicate detection on update/edit operations.

## Capabilities

### New Capabilities
- `duplicate-entity-detection`: Server-side duplicate checking on person and organization creation, returning structured 409 responses, with frontend toast alerts surfacing the conflict to the user.

### Modified Capabilities
_None — this adds new validation behavior without changing existing spec-level requirements._

## Impact

- **Backend**: `network/api/people.py` and `network/api/organizations.py` — add duplicate lookup before `create()`.
- **Frontend**: `frontend/src/routes/people/+page.svelte` and `frontend/src/routes/organizations/+page.svelte` — add error handling with toast notifications in creation handlers.
- **API contract**: New 409 response code on `POST /api/people/` and `POST /api/organizations/`.
- **No database changes** — leverages existing unique constraints.
