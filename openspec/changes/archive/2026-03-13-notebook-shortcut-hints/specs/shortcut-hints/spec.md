## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Popover displays page-specific shortcuts
The popover SHALL display the shortcuts provided by the host page. Each shortcut SHALL show a key combination and a description.

#### Scenario: Tasks page shortcuts displayed
- **WHEN** the popover is open on the Tasks page
- **THEN** the popover lists: ↑/k (Previous task), ↓/j (Next task), x (Complete task), Delete (Delete task), Tab (Indent), Shift+Tab (Outdent), Escape (Deselect), Ctrl+↑/↓ (Jump section), Ctrl+←/→ (Cycle lists)

#### Scenario: Notebook page shortcuts displayed
- **WHEN** the popover is open on the Notebook page
- **THEN** the popover displays two sections: a "Shortcuts" section with Ctrl+\ (Toggle sidebar), and a "Syntax" section with @Name (Mention person), @new[Name] (Draft new contact), [[ (Link to entity), - [ ] (Checkbox / task)
