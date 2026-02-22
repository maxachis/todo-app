## ADDED Requirements

### Requirement: Inline creation of new options
The system SHALL support an optional `onCreate` callback on TypeaheadSelect that enables creating new entries directly from the dropdown when no exact match exists.

#### Scenario: Create option appears when no exact match and onCreate provided
- **WHEN** the user types text into a TypeaheadSelect that has an `onCreate` callback AND no existing option label matches the typed text exactly (case-insensitive)
- **THEN** a "Create [typed text]" item appears at the bottom of the dropdown

#### Scenario: Create option does not appear without onCreate
- **WHEN** the user types text into a TypeaheadSelect that does NOT have an `onCreate` callback AND no existing option matches
- **THEN** the dropdown is hidden (existing behavior unchanged)

#### Scenario: Create option does not appear when exact match exists
- **WHEN** the user types text that exactly matches (case-insensitive) an existing option's label AND `onCreate` is provided
- **THEN** the "Create" item does NOT appear in the dropdown (only the matching option is shown)

#### Scenario: Create option does not appear when input is empty
- **WHEN** the input is empty or whitespace-only AND `onCreate` is provided
- **THEN** the "Create" item does NOT appear in the dropdown

#### Scenario: Selecting the create option calls onCreate and selects the new entry
- **WHEN** the user selects the "Create [typed text]" item (via click or Enter)
- **THEN** the `onCreate` callback is called with the trimmed input text, the returned `{ id, label }` is selected as the current value, and the dropdown closes

#### Scenario: Create option is keyboard-navigable
- **WHEN** the dropdown is open with both filtered options and a "Create" item
- **THEN** ArrowDown/ArrowUp navigation cycles through all items including the "Create" item, and Enter selects the highlighted item

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
- **THEN** the dropdown is hidden (no empty-state message displayed)

#### Scenario: No matches found with onCreate
- **WHEN** the user types non-empty text that matches no options AND an `onCreate` callback is provided
- **THEN** the dropdown remains open showing only the "Create [typed text]" item

#### Scenario: Dropdown closes on blur
- **WHEN** the user clicks outside the typeahead component
- **THEN** the dropdown closes
