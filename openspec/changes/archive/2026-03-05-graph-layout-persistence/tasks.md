## 1. Add localStorage save/load helpers

- [x] 1.1 Add `loadGraphSettings()` function that reads `graph-layout-settings` from localStorage and returns an object with slider values and checkbox states, falling back to defaults on error or missing data (`frontend/src/routes/network/graph/+page.svelte`)
- [x] 1.2 Add `saveGraphSettings()` function that writes current slider values and checkbox states to localStorage under `graph-layout-settings` (`frontend/src/routes/network/graph/+page.svelte`)

## 2. Initialize inputs from saved state

- [x] 2.1 In `onMount`, before `initGraph()`, call `loadGraphSettings()` and apply saved values to slider inputs (`.value`) and checkbox inputs (`.checked`) (`frontend/src/routes/network/graph/+page.svelte`)

## 3. Persist on change

- [x] 3.1 Call `saveGraphSettings()` inside the existing `attachInput` event handlers so settings are saved whenever any slider or checkbox changes (`frontend/src/routes/network/graph/+page.svelte`)

## 4. Verify

- [x] 4.1 Run `cd frontend && npm run check` to confirm no type errors
- [ ] 4.2 Manual verification: adjust sliders and checkboxes, reload page, confirm values persist
