## 1. Dependencies

- [x] 1.1 Install `chrono-node` npm package in `frontend/` (`npm install chrono-node`)

## 2. Detection Logic

- [x] 2.1 Add detection state machine to `TaskCreateForm.svelte`: `detectionState` variable with LISTENING/SHOWING/DISMISSED states, `detectedDateText` for the badge label
- [x] 2.2 Add `oninput` handler on the title input that runs `chrono.parseDate(title)` when state is LISTENING or SHOWING, updates `dueDate` and `detectedDateText` when a date is found, transitions to SHOWING
- [x] 2.3 Handle SHOWING → DISMISSED transition: clicking ✕ clears `dueDate`, sets state to DISMISSED
- [x] 2.4 Handle manual picker override: add `oninput`/`onchange` handler on the date picker that hides the badge when the user interacts directly (distinguish programmatic vs manual changes)
- [x] 2.5 Reset detection state to LISTENING on form submission (alongside existing title/date reset)

## 3. Badge UI

- [x] 3.1 Add badge element to the form template between title input and date picker, conditionally rendered when `detectionState === 'SHOWING'`; display formatted date and ✕ button
- [x] 3.2 Update form grid layout to accommodate the badge column (`grid-template-columns: 1fr auto auto auto`)
- [x] 3.3 Style the badge: small chip appearance, muted colors, `var(--bg-surface)` background, `var(--border)` border, compact padding
- [x] 3.4 Hide the badge on mobile viewports (max-width 480px) via CSS `display: none`

## 4. Testing

- [ ] 4.1 Manually verify detection for each format category: natural language ("tomorrow", "next friday"), numeric ("1/15", "2026-03-01"), month names ("jan 15", "February 3rd")
- [ ] 4.2 Manually verify state transitions: LISTENING → SHOWING (type date), SHOWING → SHOWING (change date), SHOWING → DISMISSED (click ✕), form submit resets to LISTENING
- [ ] 4.3 Manually verify manual picker override: pick a date manually while badge is showing → badge hides, picker keeps manual value
- [ ] 4.4 Manually verify mobile: badge hidden, picker pre-fills correctly
