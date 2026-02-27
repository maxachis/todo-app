## MODIFIED Requirements

### Requirement: TypeaheadSelect component
The system SHALL provide a reusable TypeaheadSelect Svelte component that replaces native `<select>` elements with a text input that filters a list of options as the user types and presents matching results in a dropdown.

#### Scenario: Component renders a text input
- **WHEN** the TypeaheadSelect component is rendered
- **THEN** it displays a text input field with the configured placeholder text

#### Scenario: Dropdown opens on focus
- **WHEN** the text input receives focus and there are available options
- **THEN** a dropdown list of matching options appears below the input

#### Scenario: Options are filtered by typed text
- **WHEN** the user types into the input field
- **THEN** the dropdown shows only options whose label contains the typed text (case-insensitive substring match)

#### Scenario: No matches found without onCreate
- **WHEN** the user types text that matches no options AND no `onCreate` callback is provided
- **THEN** the dropdown SHALL remain open and display a non-selectable "No match found — add it first" message
- **AND** the typed text SHALL be preserved in the input

#### Scenario: No matches found with onCreate
- **WHEN** the user types non-empty text that matches no options AND an `onCreate` callback is provided
- **THEN** the dropdown remains open showing only the "Create [typed text]" item

#### Scenario: Dropdown closes on blur
- **WHEN** the user clicks outside the typeahead component
- **THEN** the dropdown closes

#### Scenario: No-match message is not selectable
- **WHEN** the "No match found" message is displayed in the dropdown
- **THEN** the message SHALL NOT be selectable via click or keyboard navigation
- **AND** the message SHALL NOT be included in the keyboard-navigable item count
- **AND** the message SHALL have `role="status"` (not `role="option"`)
