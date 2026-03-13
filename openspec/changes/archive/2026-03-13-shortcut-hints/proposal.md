## Why

Pages with keyboard shortcuts (Tasks, Notebook) have no visible indication that shortcuts exist. Users must discover them by accident or read documentation. A small floating hint badge makes shortcuts discoverable without cluttering the UI.

## What Changes

- Add a shared `ShortcutHints.svelte` component that renders a floating `?` badge in the bottom-right corner of the page
- Clicking the badge toggles a popover listing the page's keyboard shortcuts
- Integrate the component on the Tasks page (9 shortcuts) and the Notebook page (1 shortcut)

## Non-goals

- Global shortcut overlay triggered by pressing `?` key
- Persistent/pinned hint bar
- Shortcuts for other pages (can be added later by reusing the component)

## Capabilities

### New Capabilities
- `shortcut-hints`: Floating badge + popover component for displaying keyboard shortcut hints on a per-page basis

### Modified Capabilities
<!-- None — this is purely additive UI with no changes to existing behavior -->

## Impact

- New component: `frontend/src/lib/components/shared/ShortcutHints.svelte`
- Modified pages: `frontend/src/routes/+page.svelte` (Tasks), `frontend/src/routes/notebook/+page.svelte` (Notebook)
- No API changes, no backend changes
