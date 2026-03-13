## 1. Create Notes Editor

- [x] 1.1 Create `frontend/src/lib/components/shared/createNotesEditor.ts` — slim CodeMirror factory reusing `livePreview`, `checkboxWidgets`, `listKeymap`, `notebookTheme` from notebook modules, with `onChange` and `onBlur` callbacks, no mentions or autocompletion
- [x] 1.2 Create `frontend/src/lib/components/shared/NotesEditor.svelte` — Svelte wrapper component with `value` and `onSave` props, manages CodeMirror lifecycle (mount, content sync on prop change, destroy), calls `onSave` on blur

## 2. Integrate into Task Detail

- [x] 2.1 Replace `<MarkdownEditor>` with `<NotesEditor>` in `frontend/src/lib/components/tasks/TaskDetail.svelte`, keeping the same `value={notesValue}` and `onSave={saveNotes}` interface

## 3. Verify

- [x] 3.1 Run `cd frontend && npm run check` to verify no TypeScript or Svelte errors
