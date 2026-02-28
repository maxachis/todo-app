## Context

People and organizations have database-level unique constraints (`unique_person_name` on `first_name`+`last_name`, `unique_org_name` on `name`). Currently, attempting to create a duplicate causes an unhandled `IntegrityError` that surfaces as a 500 to the frontend, which is silently swallowed — no feedback reaches the user.

The toast system (`frontend/src/lib/stores/toast.ts`) already exists but is not wired into people or organization creation flows.

## Goals / Non-Goals

**Goals:**
- Return a structured 409 Conflict response when a duplicate person or organization is detected.
- Display a warning toast on the frontend with a human-readable message identifying the conflict.
- Keep the form populated (don't clear it) so the user can adjust their input.

**Non-Goals:**
- Fuzzy matching or "did you mean?" suggestions.
- Merge/link-to-existing workflows.
- Duplicate detection on update operations.

## Decisions

### 1. Check before insert (application-level) vs. catch IntegrityError

**Decision**: Check with a query before calling `create()`, and return 409 if a match is found.

**Why**: Catching `IntegrityError` is fragile — SQLite wraps the transaction and the error message format varies across databases. An explicit `exists()` query is clear, testable, and gives us control over the error message. The race-condition risk is irrelevant for a single-user app.

**Alternative considered**: Wrapping `create()` in `try/except IntegrityError` — rejected due to opaque error messages and transaction handling complexity.

### 2. Case-insensitive matching

**Decision**: Use `iexact` lookups for duplicate checks (`first_name__iexact`, `last_name__iexact`, `name__iexact`).

**Why**: Users shouldn't be able to create "John Smith" and "john smith" as separate people. The database constraint is case-sensitive, but the application-level check should be case-insensitive to catch near-duplicates before the DB constraint fires.

### 3. 409 response format

**Decision**: Return `{ "detail": "<human-readable message>" }` with HTTP 409.

**Why**: Matches the existing `HttpError` pattern used elsewhere in the API. The frontend can extract `detail` for the toast message without special parsing.

### 4. Frontend error handling location

**Decision**: Handle in each page component's `createPerson()`/`createOrganization()` function by catching the API error and checking for 409 status.

**Why**: State is managed locally in the page components (no dedicated stores), so error handling belongs there too. The existing `apiRequest` function throws on non-OK responses, so we catch and inspect the error.

## Risks / Trade-offs

- **[Race condition on concurrent requests]** → Not a real risk: single-user app. The DB constraint remains as a safety net regardless.
- **[Case-insensitive check may not match DB constraint behavior exactly]** → Acceptable: the app-level check is stricter (catches more), and the DB constraint is the final guard.
- **[Extra query per create request]** → Negligible: one `SELECT ... WHERE ... LIMIT 1` on an indexed field before each insert.
