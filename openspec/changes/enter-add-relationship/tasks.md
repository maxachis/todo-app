## 1. Add Enter-to-submit on relationship create forms

- [x] 1.1 Add `onkeydown` handler to the person-person notes textarea in `frontend/src/routes/relationships/+page.svelte` — on Enter (no Shift), prevent default and call the existing `createPersonRelationship` submit logic if both person IDs are set
- [x] 1.2 Add `onkeydown` handler to the org-person notes textarea in the same file — on Enter (no Shift), prevent default and call the existing `createOrgRelationship` submit logic if both org and person IDs are set

## 2. Verify behavior

- [x] 2.1 Manual test: select two people, type a note, press Enter — relationship is created and form resets
- [x] 2.2 Manual test: select org + person, type a note, press Enter — relationship is created and form resets
- [x] 2.3 Manual test: press Enter with missing selections — form does not submit
- [x] 2.4 Manual test: Shift+Enter in notes textarea inserts a newline without submitting
