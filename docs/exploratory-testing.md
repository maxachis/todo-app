# Exploratory Testing Report

**Date:** 2026-03-15
**Environment:** Devcontainer (Django 0.0.0.0:8000, SvelteKit dev 0.0.0.0:5173)
**Testing method:** API-level (curl), automated test suites (pytest, E2E), and interactive browser testing via Playwright MCP
**Database:** SQLite with live data (20 lists, 70+ people, 24 orgs, 22 interactions)

---

## Summary

| Area | Status | Notes |
|------|--------|-------|
| Task CRUD | Pass | Create, complete, uncomplete, pin, move, delete all work |
| Lists & Sections | Pass | List/section CRUD works correctly |
| Dashboard / Upcoming | Pass | Upcoming tasks with grouping works |
| Dashboard Trends | Pass | Interactions per week, follow-ups due both work |
| Projects | Pass | CRUD and linked lists work |
| Timesheet | Pass | Entry creation, weekly summaries work |
| Search | Pass | Full-text search with proper response structure |
| Export (JSON/CSV/MD) | Pass | All three formats return valid data |
| Full Backup Export | **Fail** | Round-trip test fails (lists_created count mismatch) |
| CRM People | Pass (partial) | List/detail work; missing person returns 500 |
| CRM Orgs | Pass | List/detail/404 all work correctly |
| CRM Interactions | Pass | List/detail/404 all work correctly |
| CRM Leads | Pass | List endpoint works |
| CRM Relationships | Pass | All three sub-types (people, orgs, org-org) work |
| Network Graph | Pass | Returns nodes (99) and edges (74) |
| Notebook | **Fail** | SSR crash: `document is not defined` |
| Contact Drafts | Pass | List endpoint works |
| Frontend Build | Pass | Production build succeeds, 0 errors, 9 warnings |
| Frontend Type Check | Pass | 0 errors, 9 warnings |
| Input Validation | **Fail** | Empty names/titles cause 500 instead of 422 |
| E2E Tests | Partial | 81 passed, 7 failed |
| Backend API Tests | Partial | 225 passed, 4 real failures (excluding 65 legacy HTMX) |

---

## Bugs Found

### BUG-1: Notebook page SSR crash (Severity: High)

**Route:** `/notebook`
**Error:** `ReferenceError: document is not defined` at `+page.svelte:149`
**Cause:** `onDestroy` callback references `document.removeEventListener()` which doesn't exist during server-side rendering.
**Impact:** Page returns HTTP 500; completely inaccessible via direct URL navigation or page refresh. Works only via client-side navigation from another page.
**Fix:** Guard with `if (typeof document !== 'undefined')` or use `browser` import from `$app/environment`.

### BUG-2: Missing person returns 500 instead of 404 (Severity: Medium)

**Endpoint:** `GET /api/people/{id}/`
**Steps:** Request a non-existent person ID (e.g., `/api/people/99999/`)
**Expected:** HTTP 404 with `{"detail": "Not Found"}`
**Actual:** HTTP 500 with unhandled `Person.DoesNotExist` traceback
**Cause:** `get_person()` in `network/api/people.py:90` uses `.get(pk=person_id)` directly instead of `get_object_or_404()` (unlike `update_person` at line 96 which correctly uses it).
**Impact:** Exposes internal stack trace to client; inconsistent with other endpoints (orgs, interactions return proper 404).

### BUG-3: Empty required fields cause 500 instead of validation error (Severity: Medium)

**Endpoints:** `POST /api/people/`, `POST /api/sections/{id}/tasks/`, `POST /api/lists/`
**Steps:** Send empty string for required fields (empty `first_name`/`last_name`, empty `title`, empty `name`)
**Expected:** HTTP 422 with validation error
**Actual:** HTTP 500 server error
**Impact:** Frontend would need to handle 500 errors for simple validation failures; bad UX if user submits empty forms.

### BUG-4: Full backup round-trip assertion failure (Severity: Medium)

**Test:** `FullBackupRoundTripTests.test_round_trip`
**Error:** `AssertionError: 2 != 1` on `stats["lists_created"]` vs `counts["lists"]`
**Cause:** Import creates more lists than expected — likely the system Inbox list is being auto-created in addition to the imported list, or a duplicate is created.

### BUG-5: People API tests fail — Interaction model mismatch (Severity: Low)

**Tests:** `PeopleLastInteractionTests` (3 failures)
**Error:** `TypeError: Interaction() got unexpected keyword arguments: 'person'`
**Cause:** Tests use `Interaction(person=...)` but the model uses `people` as a ManyToManyField. Tests are out of date with the model schema change from FK to M2M.

### BUG-6: XSS in task titles stored unsanitized (Severity: Low)

**Endpoint:** `POST /api/sections/{id}/tasks/`
**Steps:** Create task with title `<script>alert(1)</script>`
**Result:** Script tag stored verbatim in database and returned in API responses
**Mitigation:** Svelte auto-escapes in templates by default, so this is not exploitable in the current frontend. However, any future raw HTML rendering (e.g., `{@html}`) or third-party consumer could be affected. Consider server-side sanitization as defense-in-depth.

### BUG-7: Raw mention syntax displayed on Projects page (Severity: Low)

**Route:** `/projects`
**Steps:** View a project that has Notebook Mentions
**Expected:** Mentions rendered as readable names (e.g., "Max Chis", "Test Project")
**Actual:** Raw mention syntax shown: `@[person:1|Max Chis] [[org:2|f]] [[project:1|Test Project]]`
**Impact:** Cosmetic — the mention links are not parsed/rendered in the project card context.

### BUG-8: Console errors on every page load (Severity: Low)

**Errors (5 on every page):**
1. `Failed to load resource: net::ERR_ADDRESS_UNREACHABLE` — Google Fonts CSS (no external network in devcontainer)
2. `404 Not Found` — `/static/manifest.json` missing
3. `Manifest fetch failed, code 404` — PWA manifest not found
4. `Failed to register ServiceWorker` — `/static/service-worker.js` returns 404
5. `A bad HTTP response code (404) was received when fetching the script`

**Impact:** Items 2-5 indicate the PWA manifest and service worker are referenced in HTML but the files don't exist in the dev server's static directory. Font failure is expected without external network access.

---

## E2E Test Failures

| Test | Failure Reason |
|------|----------------|
| `test_can_create_two_interactions_in_sequence` | Pre-existing timing issue with typeahead |
| `test_tab_indent_shift_tab_outdent` | Keyboard handling issue |
| `test_click_to_edit_and_render` | Markdown editor interaction |
| `test_xss_is_sanitized` | Markdown XSS sanitization |
| `test_supported_markdown_syntax_renders` | Markdown rendering |
| `test_network_tabs_navigate_to_correct_routes` | URL assertion mismatch — expects `/crm/people` |
| `test_empty_state_when_no_upcoming_tasks` | Text changed: expects "No tasks with due dates..." but page shows "No upcoming or pinned tasks..." |

The last two are likely stale assertions from recent UI changes.

---

## Warnings (from `svelte-check`)

| Warning | File | Note |
|---------|------|------|
| `state_referenced_locally` | `NotesEditor.svelte:16` | Captures initial `value` instead of reactive reference |
| `a11y_label_has_associated_control` (x4) | `TaskDetail.svelte` | Labels not associated with form controls |
| `a11y_label_has_associated_control` | `dashboard/+page.svelte:355` | Label not associated with control |
| `css_unused_selector` (x2) | `network/graph/+page.svelte` | `.search-results .result` and `:hover` selectors unused |
| `a11y_autofocus` | `timesheet/+page.svelte:214` | Autofocus usage flagged |

---

## Design Observations

1. **Timesheet "hours" are entry counts** — `TimeEntry` has no `hours` field; the API counts entries as hours. Each entry = 1 hour. The `hours` field in create payload is silently ignored.

2. **Legacy HTMX tests remain** — `tasks/tests/test_views.py` and `tasks/tests/test_integration.py` contain 65 tests for removed HTMX views that all fail with `NoReverseMatch`. These should be deleted or marked as skip.

3. **Network sub-tab routing** — CLAUDE.md says "Network has sub-tabs (Relationships, Graph)" but Relationships lives under CRM (`/crm/relationships`), not Network. The Network route (`/network`) just redirects to `/network/graph`.

4. **CSRF protection works** — POST/PUT/DELETE endpoints correctly require CSRF tokens. The health endpoint provides tokens via cookies.

---

## UI Testing (Playwright Browser)

Pages visually tested at 1280x800 (desktop) and 390x844 (mobile):

| Page | Desktop | Mobile | Notes |
|------|---------|--------|-------|
| Tasks (three-panel) | Good | Good | Sidebar toggle, list selection, task detail all work |
| Dashboard - Upcoming | Good | — | Pinned/Overdue/Later groupings render correctly |
| Dashboard - Trends | Good | — | Bar charts and follow-up compliance display well |
| CRM - Inbox | Good | — | Contact draft triage layout works |
| CRM - People | Good | — | List/detail split, filter/sort, tag badges, follow-up cadence |
| CRM - Orgs | Good | — | — |
| Network - Graph | Good | — | D3 graph with clusters, filters, layout sliders all functional |
| Notebook | Good (client nav) | — | Works via SPA navigation; crashes on direct load (BUG-1) |
| Projects | Good | — | Card layout; raw mention syntax in Notebook Mentions (BUG-7) |
| Timesheet | Good | — | Week navigation, per-project summaries |

**Dark mode:** Theme toggle cycles light/system/dark correctly. All pages render well in dark mode. Minor note: the network graph SVG canvas background doesn't change with theme.

**Mobile:** Bottom tab navigation, hamburger sidebar, and responsive layout all work correctly. Tab labels truncate gracefully on small screens.

**Search:** Live typeahead dropdown appears with results grouped by list, showing section and tags.

**Screenshots:** Saved to `docs/screenshots/` (01-17).

---

## Test Coverage Summary

**Backend (excluding legacy):** 225 passed, 4 failed
**Frontend type check:** 0 errors, 9 warnings
**Frontend build:** Success (7.5s)
**E2E:** 81 passed, 7 failed
**All frontend routes respond (HTTP 200):** Yes, except `/notebook` (500 on direct load only)
