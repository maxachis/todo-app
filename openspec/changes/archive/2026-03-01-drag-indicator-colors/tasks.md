## 1. Add drop-target style constant

- [x] 1.1 Add `dropTargetStyle` option with accent color (`{ outline: "rgba(180, 88, 40, 0.7) solid 2px" }`) to `DragContainer.svelte` — both the `use:dndzone` and `use:dragHandleZone` calls

## 2. Update direct dndzone call sites

- [x] 2.1 Add `dropTargetStyle` to `ListSidebar.svelte` `use:dndzone` call
- [x] 2.2 Add `dropTargetStyle` to `SectionList.svelte` `use:dragHandleZone` call
- [x] 2.3 Add `dropTargetStyle` to `PinnedSection.svelte` `use:dndzone` call

## 3. Verify

- [x] 3.1 Run `npm run check` in `frontend/` to confirm no type errors
