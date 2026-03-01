## MODIFIED Requirements

### Requirement: Inline creation of new options
The system SHALL support an optional `onCreate` callback on TypeaheadSelect that enables creating new entries directly from the dropdown when no exact match exists.

#### Scenario: Create option appears when no exact match and onCreate provided
- **WHEN** the user types text into a TypeaheadSelect that has an `onCreate` callback AND no existing option label matches the typed text exactly (case-insensitive, untrimmed)
- **THEN** a "Create [typed text]" item appears at the bottom of the dropdown

#### Scenario: Create option does not appear without onCreate
- **WHEN** the user types text into a TypeaheadSelect that does NOT have an `onCreate` callback AND no existing option matches
- **THEN** the dropdown remains open with a "No match found — add it first" message (no "Create" item shown)

#### Scenario: Create option does not appear when exact match exists
- **WHEN** the user types text that exactly matches (case-insensitive, untrimmed) an existing option's label AND `onCreate` is provided
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

#### Scenario: Typing beyond an existing option name keeps dropdown open
- **WHEN** the user types "LinkedIn" (which matches an existing option) and then continues typing " Connection" (making the full input "LinkedIn Connection")
- **THEN** the input SHALL preserve the full typed text "LinkedIn Connection"
- **AND** the dropdown SHALL remain open showing the "Create" option (if `onCreate` is provided)
- **AND** the input text SHALL NOT be erased or overwritten at any intermediate keystroke

#### Scenario: Trailing whitespace does not trigger exact match suppression
- **WHEN** the user types "LinkedIn " (with a trailing space) in a TypeaheadSelect with `onCreate` provided
- **THEN** the "Create" option SHALL appear in the dropdown (since "LinkedIn " is not an exact match for "LinkedIn")
- **AND** the input SHALL preserve "LinkedIn " without being cleared
