## 1. Implementation

- [x] 1.1 Add `$effect` in `frontend/src/routes/+layout.svelte` that watches `$selectedListStore` and sets `sidebarOpen = false` when it changes

## 2. Verification

- [x] 2.1 Test on mobile viewport: open sidebar, tap a list, confirm sidebar closes and tasks are visible
- [x] 2.2 Test on desktop viewport: confirm sidebar remains visible after selecting a list
- [x] 2.3 Test list creation on mobile: create a new list, confirm sidebar closes
- [x] 2.4 Run `cd frontend && npm run check` to verify no type errors
