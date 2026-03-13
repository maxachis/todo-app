## Why

The browser tab currently shows a static "Nexus" title with no indication of pending work. Showing a count of overdue + due-today tasks in the tab title (e.g., `(3) Nexus`) provides an at-a-glance signal of how many items need attention without switching to the app.

## What Changes

- Add a reactive document title that displays a badge count of actionable tasks (overdue + due today)
- The title updates live as tasks are completed, added, or rescheduled
- When the count is zero, the title reverts to plain "Nexus"
- Format: `(N) Nexus` where N = number of overdue + due-today incomplete tasks

## Non-goals

- Showing inbox count (may be added later)
- Desktop notifications or favicon badges
- Per-page title changes (e.g., "Dashboard - Nexus")

## Capabilities

### New Capabilities
- `tab-due-count`: Reactive browser tab title showing count of overdue and due-today tasks

### Modified Capabilities

## Impact

- **Frontend**: `+layout.svelte` (or a new reactive store) to set `document.title`
- **Backend**: Existing `/api/upcoming/` endpoint already returns due tasks with dates; may need a lightweight count endpoint or reuse existing data
- **No breaking changes**: purely additive UI enhancement
