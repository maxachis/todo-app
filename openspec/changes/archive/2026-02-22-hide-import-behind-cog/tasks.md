## 1. Remove Import from navigation tabs

- [x] 1.1 Remove the `{ href: '/import', label: 'Import' }` entry from the `tabs` array in `frontend/src/routes/+layout.svelte`

## 2. Add cog button and dropdown menu

- [x] 2.1 Add `settingsOpen` state variable to `+layout.svelte`
- [x] 2.2 Add a cog button (gear emoji) next to the theme toggle button, wired to toggle `settingsOpen`
- [x] 2.3 Add a dropdown menu that renders when `settingsOpen` is true, containing an "Import" link to `/import` with active state styling when on the import route
- [x] 2.4 Wrap the cog button and dropdown in a positioned container div for absolute dropdown positioning

## 3. Dropdown dismissal behavior

- [x] 3.1 Add click-outside handler to close the dropdown when clicking outside the cog button and menu
- [x] 3.2 Add Escape keydown handler to close the dropdown
- [x] 3.3 Close the dropdown on navigation by reacting to `$page.url.pathname` changes

## 4. Styling

- [x] 4.1 Style the cog button to match the existing `.theme-toggle` button (border, padding, hover state)
- [x] 4.2 Style the dropdown menu: dark background matching `--bg-nav`, border, border-radius, shadow, right-aligned below the cog button
- [x] 4.3 Style dropdown links to match nav tab styling (color, hover, active states)

## 5. Verification

- [x] 5.1 Verify Import tab no longer appears in desktop nav or mobile bottom tabs
- [x] 5.2 Verify cog button is visible on desktop and mobile viewports
- [x] 5.3 Verify clicking Import in dropdown navigates to `/import` and the page works correctly
- [x] 5.4 Verify dropdown closes on outside click, Escape, and navigation
- [x] 5.5 Run `cd frontend && npm run check` to verify no TypeScript/lint errors
