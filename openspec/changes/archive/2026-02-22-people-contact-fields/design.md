## Context

The Person model currently stores `first_name`, `middle_name`, `last_name`, `notes`, and `follow_up_cadence_days`. There's no structured way to store contact info — users must put emails and LinkedIn URLs in the free-text notes field.

The People page has a create form (left panel) and an edit form (right detail panel). Both forms map directly to the API schemas (`PersonCreateInput`, `PersonUpdateInput`, `PersonSchema`).

## Goals / Non-Goals

**Goals:**
- Add `email` and `linkedin_url` as dedicated fields on Person
- Expose both in API create/update/response schemas
- Add input fields to both the create and edit forms
- Display email as `mailto:` link and LinkedIn as clickable URL in the detail panel

**Non-Goals:**
- Email validation beyond basic format (no MX lookup, no verification)
- LinkedIn URL normalization (accept whatever the user types)
- Adding contact fields to Organizations or other entities (separate change)
- Showing contact fields in the People list panel (only in detail)

## Decisions

### 1. Optional text fields, no custom validation
Both fields are `CharField(blank=True)` with no custom validators. Email format is only lightly checked client-side via `type="email"` on the input. LinkedIn is a plain text field — the user may paste a full URL or just a username. This keeps it simple and avoids frustrating edge cases.

### 2. Fields placed between name fields and follow-up cadence
In both create and edit forms, email and LinkedIn inputs go after the name fields but before follow-up cadence and notes. This groups contact info logically.

### 3. Clickable links in detail view only
The detail panel renders email as a `mailto:` link and LinkedIn as an external link (opens in new tab). The list panel (left side) does not show these fields to keep the list compact.

## Risks / Trade-offs

- **[Risk] LinkedIn URL inconsistency** → Users may enter full URLs, partial paths, or usernames. We accept any text without normalization. This is a conscious tradeoff for simplicity.
- **[Risk] Migration on existing data** → Both fields default to empty string, so the migration is safe with no data loss.
