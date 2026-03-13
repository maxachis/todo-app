## 1. Add data attributes to mention chip DOM

- [x] 1.1 Update `MentionWidget.toDOM()` in `frontend/src/lib/components/notebook/mentionWidgets.ts` to set `data-entity-type` and `data-entity-id` attributes on the chip `<span>` element
- [x] 1.2 Pass pages list to `MentionWidget` so page mentions can also set `data-entity-slug` by looking up the slug from the page ID
- [x] 1.3 Thread the pages list through from `createEditor.ts` options to the mention widgets decoration builder

## 2. Add Ctrl/Cmd hover cursor affordance

- [x] 2.1 Add `keydown`/`keyup` event handlers in `createEditor.ts` that toggle a `cm-ctrl-held` CSS class on the editor container when Ctrl (or Meta on macOS) is pressed/released
- [x] 2.2 Add CSS rules in `frontend/src/lib/components/notebook/theme.ts` for `.cm-ctrl-held .cm-mention-chip` with `cursor: pointer` and underlined label text
- [x] 2.3 Handle `blur`/`visibilitychange` to remove the `cm-ctrl-held` class when the editor loses focus

## 3. Add Ctrl+Click navigation handler

- [x] 3.1 Add `onNavigate?: (type: string, id: number, slug?: string) => void` callback to `createEditor()` options in `createEditor.ts`
- [x] 3.2 Register a `click` handler in `EditorView.domEventHandlers` that checks for Ctrl/Meta modifier, finds closest `.cm-mention-chip`, reads data attributes, and calls `onNavigate`
- [x] 3.3 Implement the `onNavigate` callback in `frontend/src/routes/notebook/+page.svelte` that routes to the appropriate page: `openPage()` for pages, `goto()` for people/tasks/orgs/projects

## 4. Verify and test

- [x] 4.1 Run `cd frontend && npm run check` to verify TypeScript compiles cleanly
- [x] 4.2 Manual verification: confirm Ctrl+Click navigates for each entity type (page, person, task, org, project)
- [x] 4.3 Manual verification: confirm plain click still positions cursor without navigating
