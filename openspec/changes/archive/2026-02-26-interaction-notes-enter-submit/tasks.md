## 1. Implementation

- [x] 1.1 Add `onkeydown` handler to the create form's notes `<textarea>` in `frontend/src/routes/interactions/+page.svelte` (line 153): on Enter without Shift, call `preventDefault()` and submit the form via the closest form's `requestSubmit()`
- [x] 1.2 Verify Shift+Enter still inserts a newline in the notes textarea (no code change needed — just confirm default behavior is preserved)
- [x] 1.3 Verify the edit/detail panel's notes textarea (line 201) is unaffected — Enter still inserts a newline there

## 2. Testing

- [ ] 2.1 Manually test: fill all required fields, type a note, press Enter — interaction is created and form clears
- [ ] 2.2 Manually test: press Enter with a required field missing — form does not submit
- [ ] 2.3 Manually test: press Shift+Enter in notes — newline is inserted, no submission
- [ ] 2.4 Manually test: press Enter in the edit panel's notes textarea — newline inserted, no submission
