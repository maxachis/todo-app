## Context

The notebook feature has Page models with `created_at` (auto_now_add) and `updated_at` (auto_now) fields already in the database. These timestamps are included in the API response (`PageOut` and `PageListItem` schemas) but are not displayed anywhere in the frontend. The sidebar always sorts pages by `-updated_at` with no user control. This is a pure presentation change on the frontend with a minor backend enhancement.

## Goals / Non-Goals

**Goals:**
- Surface existing timestamps visually in the notebook sidebar and page editor
- Allow users to choose sort order for the page list
- Keep the implementation minimal — leverage existing data, no model changes

**Non-Goals:**
- Date range filtering or advanced search
- Manual drag-and-drop page ordering
- Separate sort preferences per page type (wiki vs daily)

## Decisions

### 1. Backend ordering parameter

Add an `ordering` query parameter to `GET /api/notebook/pages/` accepting values: `-updated_at` (default), `-created_at`, `title`. This is a simple Django `.order_by()` pass-through with an allowlist.

**Alternative considered**: Client-side sorting only. Rejected because the API already handles pagination-like patterns server-side and keeping sort at the API level is consistent with the rest of the app.

### 2. Timestamp display format

Use relative timestamps for sidebar items (e.g., "2h ago", "Mar 5") with full datetime on hover via `title` attribute. Use absolute format ("Mar 5, 2026 2:30 PM") in the page detail metadata area. No external date library — use `Intl.RelativeTimeFormat` and `Intl.DateTimeFormat` which are built into modern browsers.

**Alternative considered**: Using a library like `date-fns` or `timeago.js`. Rejected to avoid adding a dependency for a simple formatting task.

### 3. Sort selector placement

Place a small sort dropdown/button group at the top of the notebook sidebar, above the page list. This follows the pattern used in other list views in the app.

### 4. LocalStorage persistence for sort preference

Persist the selected sort order in localStorage (key: `notebook-sort-order`) so it survives page refreshes. This is consistent with how the app persists theme and panel width preferences.

## Risks / Trade-offs

- **[Minor] Relative time staleness**: Relative timestamps ("2h ago") become stale if the page stays open. Acceptable for a single-user app — timestamps refresh on navigation.
- **[Minor] Sort state not synced**: Sort preference lives in localStorage, not the backend. Fine for single-user, single-device usage.
