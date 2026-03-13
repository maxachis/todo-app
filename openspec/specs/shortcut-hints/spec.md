### Requirement: Shortcut hints badge is visible on pages with shortcuts
The system SHALL display a floating `?` badge in the bottom-right corner of any page that includes the ShortcutHints component. The badge SHALL be visible at all times regardless of scroll position.

#### Scenario: Badge visible on Tasks page
- **WHEN** user navigates to the Tasks page
- **THEN** a `?` badge is visible in the bottom-right corner of the viewport

#### Scenario: Badge visible on Notebook page
- **WHEN** user navigates to the Notebook page
- **THEN** a `?` badge is visible in the bottom-right corner of the viewport

#### Scenario: Badge not visible on other pages
- **WHEN** user navigates to a page without the ShortcutHints component (e.g., Dashboard, CRM)
- **THEN** no `?` badge is displayed

### Requirement: Clicking the badge toggles a shortcut popover
The system SHALL toggle a popover listing keyboard shortcuts when the user clicks the `?` badge. The popover SHALL open upward from the badge position.

#### Scenario: Open popover
- **WHEN** user clicks the `?` badge and the popover is closed
- **THEN** a popover appears above the badge listing all keyboard shortcuts for that page

#### Scenario: Close popover by clicking badge again
- **WHEN** user clicks the `?` badge and the popover is open
- **THEN** the popover closes

#### Scenario: Close popover by clicking outside
- **WHEN** the popover is open and user clicks anywhere outside the popover and badge
- **THEN** the popover closes

### Requirement: Popover displays page-specific shortcuts
The popover SHALL display the shortcuts provided by the host page. Each shortcut SHALL show a key combination and a description.

#### Scenario: Tasks page shortcuts displayed
- **WHEN** the popover is open on the Tasks page
- **THEN** the popover lists: ↑/k (Previous task), ↓/j (Next task), x (Complete task), Delete (Delete task), Tab (Indent), Shift+Tab (Outdent), Escape (Deselect), Ctrl+↑/↓ (Jump section), Ctrl+←/→ (Cycle lists)

#### Scenario: Notebook page shortcuts displayed
- **WHEN** the popover is open on the Notebook page
- **THEN** the popover displays two sections: a "Shortcuts" section with Ctrl+\ (Toggle sidebar), and a "Syntax" section with @Name (Mention person), @new[Name] (Draft new contact), [[ (Link to entity), - [ ] (Checkbox / task)

### Requirement: Shortcut hints respect theme
The component SHALL use existing CSS custom properties so it renders correctly in light, dark, and system theme modes.

#### Scenario: Dark mode rendering
- **WHEN** the app is in dark mode and the popover is open
- **THEN** the badge and popover use dark mode colors via CSS custom properties

### Requirement: ShortcutHints supports grouped sections
The ShortcutHints component SHALL accept an optional `sections` prop containing an array of `{ title: string, shortcuts: Shortcut[] }`. When `sections` is provided, the popover SHALL render each group with a section heading followed by its shortcuts.

#### Scenario: Grouped sections rendered
- **WHEN** the component receives a `sections` prop with two groups
- **THEN** the popover displays each group's title as a heading followed by its shortcut rows

#### Scenario: Flat shortcuts still work
- **WHEN** the component receives only a `shortcuts` prop (no `sections`)
- **THEN** the popover renders shortcuts without section headings, identical to previous behavior

### Requirement: Notebook hints include typing syntax prompts
The Notebook page's ShortcutHints SHALL include a "Syntax" section listing the special typing triggers available in the editor.

#### Scenario: Notebook popover shows syntax section
- **WHEN** the user clicks the `?` badge on the Notebook page
- **THEN** the popover displays a "Syntax" section listing: `@Name` (Mention person), `@new[Name]` (Draft new contact), `[[` (Link to entity), `- [ ]` (Checkbox / task)
