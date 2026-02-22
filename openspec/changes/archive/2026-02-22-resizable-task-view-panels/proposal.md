## Why

The three-panel Task view layout uses fixed widths for the sidebar (300px) and detail panel (320px). Users with different screen sizes, workflows, or content density preferences cannot adjust how much space each panel occupies. Adding draggable resize handles between panels lets users allocate screen real estate to suit their current task — wider detail panel when editing notes, wider task list when scanning many tasks, or a narrower sidebar when lists are short.

## What Changes

- Add a draggable resize handle between the sidebar and the center panel
- Add a draggable resize handle between the center panel and the detail panel
- Persist user-chosen panel widths across sessions (localStorage)
- Enforce minimum widths per panel so content remains usable
- Resize handles are only active on desktop (>1024px); mobile layout is unchanged

### Non-goals

- Collapsible/hideable panels (toggle sidebar or detail panel to zero width) — out of scope
- Resizable panels on non-Tasks routes (Projects, Timesheet, etc.) — these use a single-panel layout
- Vertical resizing of any panels

## Capabilities

### New Capabilities

- `resizable-panels`: Drag-to-resize behavior for the three-panel Task view, including handle rendering, pointer tracking, width constraints, and localStorage persistence

### Modified Capabilities

- `svelte-frontend`: The three-panel layout requirement changes from fixed `grid-template-columns: 300px 1fr 320px` to dynamic column widths driven by user drag input, while preserving the existing panel structure, styling, and responsive breakpoint behavior

## Impact

- **Frontend layout** (`frontend/src/routes/+layout.svelte`): Grid column definitions change from fixed to variable; resize handle elements inserted between panels
- **New component or action**: A `ResizeHandle` component (or Svelte action) for drag interaction logic
- **localStorage**: New key(s) for persisted panel widths
- **CSS**: Minor additions for handle styling and cursor feedback
- **No backend changes** — purely a frontend concern
- **No API changes**
- **E2E tests**: May need adjustment if selectors or layout assumptions change
