## Context

The notebook editor uses CodeMirror 6 with custom `WidgetType` extensions to render mention chips for internal links (`[[page:ID|Label]]`, `@[person:ID|Label]`, `[[task:ID|Label]]`, etc.). These chips are purely visual — they have no click handlers. Navigation to referenced entities currently requires using the backlinks section below the editor or the sidebar.

The mention widget classes (`MentionWidget`, `NewContactWidget`) already set `ignoreEvent()` to return `false`, allowing DOM events to propagate through them. The checkbox widgets demonstrate the pattern for handling clicks on CodeMirror widgets via `mousedown` event listeners.

## Goals / Non-Goals

**Goals:**
- Ctrl+Click (Cmd+Click on macOS) on any mention chip navigates to the referenced entity
- Visual feedback: pointer cursor when Ctrl/Cmd is held over a chip
- Seamless in-app navigation using SvelteKit's `goto()`

**Non-Goals:**
- Plain click navigation (would conflict with editor cursor placement)
- Hover tooltips or entity previews
- New tab/window navigation
- Navigation from raw markdown source (only rendered chips)

## Decisions

### 1. Modifier key: Ctrl/Cmd + Click

**Choice**: Require Ctrl (or Cmd on macOS) modifier for navigation clicks.

**Why**: Plain clicks in a CodeMirror editor position the cursor. Using a modifier key is the established convention for "follow link" in code editors (VS Code, IntelliJ, etc.). This avoids interfering with text editing.

**Alternative considered**: Double-click — rejected because CodeMirror uses double-click for word selection.

### 2. Handle clicks via EditorView.domEventHandlers

**Choice**: Register a `click` handler in `EditorView.domEventHandlers` within `createEditor.ts`, detecting clicks on `.cm-mention-chip` elements and extracting entity type/ID from data attributes.

**Why**: This is simpler than adding individual event listeners per widget instance. CodeMirror widgets are replaced during view updates, so per-widget listeners would need re-attachment. A single delegated handler on the editor view is more robust.

**Implementation**:
- Add `data-entity-type` and `data-entity-id` attributes to mention chip DOM elements in `mentionWidgets.ts`
- For page mentions, also add `data-entity-slug` (pages navigate by slug, not ID)
- The click handler checks for modifier key, finds the closest `.cm-mention-chip`, reads data attributes, and calls a navigation callback

### 3. Navigation callback passed to createEditor

**Choice**: Add an `onNavigate(type: string, id: number)` callback to the `createEditor` options, called by the click handler.

**Why**: The editor module shouldn't know about SvelteKit routing. The notebook page component (`+page.svelte`) owns the navigation logic and can handle each entity type appropriately:
- `page` → `openPage(slug)` (already exists)
- `person` → `goto('/crm/people?id=ID')`
- `task` → `goto('/?task=ID')`
- `org` → `goto('/crm/orgs?id=ID')`
- `project` → `goto('/projects?id=ID')`

### 4. Cursor affordance via CSS + JS

**Choice**: Use a `keydown`/`keyup` listener on the editor to toggle a CSS class (`cm-ctrl-held`) on the editor container when Ctrl/Cmd is pressed. CSS rules apply `cursor: pointer` and underline to `.cm-mention-chip` when this class is present.

**Why**: Pure CSS `:hover` can't detect modifier keys. A lightweight class toggle avoids per-chip event handling while providing immediate visual feedback.

## Risks / Trade-offs

- **[Widget replacement clears data attributes]** → Data attributes are set in `toDOM()` which runs on every widget creation, so replacement is safe.
- **[Ctrl+Click conflicts with browser behavior]** → Ctrl+Click in most browsers opens links in new tabs, but mention chips are `<span>` elements, not `<a>` tags, so no browser default to conflict with.
- **[Page slug not available in mention syntax]** → The `[[page:ID|Label]]` syntax stores ID, not slug. We need slug for navigation. Options: (a) store slug in a data attribute by looking it up from the pages list passed to the editor, or (b) add an API endpoint to get slug by ID. Choice: pass the pages list and look up slug client-side — pages are already loaded for autocomplete.
