## 1. Backend: ContactDraft Model

- [x] 1.1 Create `network/models/contact_draft.py` with `ContactDraft` model: `name` (CharField 255), `quick_notes` (TextField, blank), `source_page` (FK → Page, nullable, SET_NULL), `promoted_to_person` (FK → Person, nullable, SET_NULL), `promoted_to_org` (FK → Organization, nullable, SET_NULL), `dismissed` (BooleanField, default False), `created_at` (DateTimeField, auto_now_add)
- [x] 1.2 Add `ContactDraft` import to `network/models/__init__.py`
- [x] 1.3 Create migration for the new model

## 2. Backend: `@new[Name](notes)` Parser

- [x] 2.1 Add `NEW_CONTACT_RE` regex to `notebook/mentions.py` matching `@new\[([^\]]+)\](?:\(([^)]*)\))?`
- [x] 2.2 Add `create_drafts_from_new_contacts(page)` function in `notebook/mentions.py` that: iterates regex matches, skips if a ContactDraft with same `name` and `source_page` exists, creates ContactDraft for new matches
- [x] 2.3 Call `create_drafts_from_new_contacts(page)` from `reconcile_mentions(page)` after checkbox processing and before mention reconciliation

## 3. Backend: Notebook Content Rewrite on Promotion

- [x] 3.1 Add `rewrite_new_contact_mentions(name, entity_type, entity_id)` function in `notebook/mentions.py` that: constructs escaped regex `@new\[{escaped_name}\](?:\([^)]*\))?`, finds all pages containing the pattern, rewrites to `@[person:ID|Name]` or `[[org:ID|Name]]` based on entity_type, saves each modified page
- [x] 3.2 Add `auto_dismiss_sibling_drafts(name, exclude_id)` function that sets `dismissed=True` on all other pending ContactDrafts with the same name (case-insensitive)

## 4. Backend: ContactDraft API Endpoints

- [x] 4.1 Create `network/api/contact_drafts.py` with router and schemas: `ContactDraftSchema` (id, name, quick_notes, source_page_id, source_page_slug, source_page_title, dismissed, created_at), `ContactDraftMatchesSchema` (people: list, organizations: list)
- [x] 4.2 Add `GET /contact-drafts/` endpoint: list pending drafts (both promotion FKs null, dismissed=False), ordered by `-created_at`, with source page info via select_related
- [x] 4.3 Add `GET /contact-drafts/:id/` endpoint: retrieve single draft
- [x] 4.4 Add `DELETE /contact-drafts/:id/` endpoint: hard delete, return 204
- [x] 4.5 Add `POST /contact-drafts/:id/dismiss/` endpoint: set `dismissed=True`, return updated draft
- [x] 4.6 Add `POST /contact-drafts/:id/promote/person/` endpoint: accept Person creation fields, create Person (reuse validation from existing people API), set `promoted_to_person`, use `quick_notes` as `notes` if no explicit notes provided, call `rewrite_new_contact_mentions`, call `auto_dismiss_sibling_drafts`, return created Person
- [x] 4.7 Add `POST /contact-drafts/:id/promote/org/` endpoint: accept Org creation fields (`name`, `org_type_id`, optional `notes`), create Organization, set `promoted_to_org`, call rewrite and auto-dismiss, return created Organization
- [x] 4.8 Add `POST /contact-drafts/:id/link/` endpoint: accept `{"person_id": ID}` or `{"org_id": ID}`, set appropriate FK, append `quick_notes` to existing record's notes (with `\n---\n` separator if notes exist), call rewrite and auto-dismiss, return updated draft
- [x] 4.9 Add `GET /contact-drafts/:id/matches/` endpoint: split draft name into tokens, query People (first_name/last_name icontains) and Organizations (name icontains), return matches
- [x] 4.10 Register contact_drafts router in `network/api/__init__.py` (or wherever routers are mounted)

## 5. Frontend: API Client & Types

- [x] 5.1 Add `ContactDraft` type to `frontend/src/lib/api/types.ts`: `id`, `name`, `quick_notes`, `source_page_id`, `source_page_slug`, `source_page_title`, `dismissed`, `created_at`
- [x] 5.2 Add `ContactDraftMatches` type: `people: {id, first_name, last_name}[]`, `organizations: {id, name}[]`
- [x] 5.3 Add contact draft API functions to `frontend/src/lib/api/client.ts`: `list()`, `get(id)`, `dismiss(id)`, `delete(id)`, `promoteToPerson(id, data)`, `promoteToOrg(id, data)`, `link(id, data)`, `matches(id)`

## 6. Frontend: CRM Layout — Inbox Tab

- [x] 6.1 Update `frontend/src/routes/crm/+layout.svelte` to add Inbox as first tab: `{ href: '/crm/inbox', label: 'Inbox' }` before People
- [x] 6.2 Add pending draft count badge to Inbox tab label (fetch count on layout mount, refresh after navigation)
- [x] 6.3 Update `frontend/src/routes/crm/+page.svelte` redirect from `/crm/people` to `/crm/inbox`

## 7. Frontend: CRM Inbox Page

- [x] 7.1 Create `frontend/src/routes/crm/inbox/+page.svelte` with two-panel CRM layout (reuse crm.css classes)
- [x] 7.2 Left panel: list of pending drafts showing name and truncated quick notes, ordered by most recent, with active selection state
- [x] 7.3 Right panel (no selection): empty state message — "No contacts to triage. Use @new[Name] in notebook pages to capture contacts."
- [x] 7.4 Right panel (selection): triage detail showing draft name (h2), quick notes (body text), source page link (clickable → `/notebook/{slug}`)

## 8. Frontend: Triage Actions — Match Hints

- [x] 8.1 On draft selection, fetch `matches(id)` and display "Possible matches" section if any results
- [x] 8.2 Each person match shows "→ Link to [First Last]" button; each org match shows "→ Link to [OrgName]" button
- [x] 8.3 Clicking a link button calls `link(id, {person_id})` or `link(id, {org_id})`, removes draft from list, auto-selects next draft

## 9. Frontend: Promote to Person Form

- [x] 9.1 Clicking "→ Person" toggles inline form in triage detail panel (replaces action buttons)
- [x] 9.2 Pre-fill `first_name` (first token of name), `last_name` (remaining tokens), `notes` (from quick_notes)
- [x] 9.3 Show optional fields: `middle_name`, `email`, `linkedin_url`, `follow_up_cadence_days` — all empty
- [x] 9.4 Submit calls `promoteToPerson(id, formData)`; on success, remove draft from list, auto-select next; on 409 (duplicate name), show error toast
- [x] 9.5 Cancel button returns to action buttons view

## 10. Frontend: Promote to Organization Form

- [x] 10.1 Clicking "→ Org" toggles inline form in triage detail panel
- [x] 10.2 Pre-fill `name` (full draft name), `notes` (from quick_notes)
- [x] 10.3 `org_type` field uses TypeaheadSelect with `onCreate` for inline type creation (same pattern as existing Orgs page)
- [x] 10.4 Submit calls `promoteToOrg(id, formData)`; on success, remove draft from list, auto-select next; on 409 (duplicate org name), show error toast
- [x] 10.5 Cancel button returns to action buttons view

## 11. Frontend: Dismiss Action

- [x] 11.1 "Dismiss" button calls `dismiss(id)`, removes draft from list, auto-selects next draft
- [x] 11.2 If last draft dismissed, show empty state

## 12. Testing: Backend

- [x] 12.1 Add tests for ContactDraft model creation and constraints in `network/tests/` (or existing test file)
- [x] 12.2 Add tests for `@new[Name](notes)` parser: single @new, multiple @new, without notes, idempotent re-save, same name on different pages
- [x] 12.3 Add tests for promotion endpoints: promote to person (creates Person, sets FK, rewrites pages), promote to org (creates Org, sets FK, rewrites pages)
- [x] 12.4 Add tests for link endpoint: links to existing person/org, appends quick_notes with separator
- [x] 12.5 Add tests for match hints endpoint: exact match, partial match, no match
- [x] 12.6 Add tests for auto-dismiss: sibling drafts dismissed after promotion
- [x] 12.7 Add tests for notebook rewrite: single page, multiple pages, regex-special characters in name

## 13. Testing: Frontend

- [x] 13.1 Verify CRM tab order shows Inbox first
- [x] 13.2 Verify inbox list loads and displays pending drafts
- [x] 13.3 Verify promote-to-person flow end-to-end (select draft → fill form → submit → draft removed)
- [x] 13.4 Verify promote-to-org flow end-to-end
- [x] 13.5 Verify link-to-existing flow via match hints
- [x] 13.6 Verify dismiss removes draft and auto-selects next
