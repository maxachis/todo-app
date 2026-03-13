## Why

The notebook editor renders internal links (page links, person mentions, task/org/project references) as styled chips, but they are not interactive — clicking them does nothing. Users must navigate via the backlinks section or sidebar instead. Ctrl+Click on a mention chip should navigate directly to the referenced entity, matching the expected behavior of link-like UI elements.

## What Changes

- Add Ctrl+Click (Cmd+Click on macOS) handler to mention chips in the CodeMirror editor
- For `[[page:ID|Label]]` links: navigate to that notebook page via `?p=slug`
- For `@[person:ID|Label]` mentions: navigate to `/crm/people` and select the person
- For `[[task:ID|Label]]` links: navigate to the Tasks route and select the task
- For `[[org:ID|Label]]` links: navigate to `/crm/orgs` and select the organization
- For `[[project:ID|Label]]` links: navigate to `/projects` and select the project
- Visual cursor affordance: mention chips show pointer cursor on Ctrl/Cmd hover

## Non-goals

- Regular click navigation (without modifier key) — this would interfere with editor cursor placement
- Opening links in new browser tabs
- Previewing linked entities on hover/tooltip

## Capabilities

### New Capabilities
- `notebook-link-click`: Ctrl+Click navigation from mention chips in the notebook editor to the referenced page or entity

### Modified Capabilities
<!-- No existing spec requirements are changing — this is purely additive behavior on existing mention widgets -->

## Impact

- **Frontend**: `mentionWidgets.ts` (click handling, cursor styling), `createEditor.ts` (event wiring), `+page.svelte` (navigation callback)
- **Routing**: Uses existing SvelteKit `goto()` for in-app navigation
- **No backend changes**: All entity IDs and types are already embedded in the mention syntax
