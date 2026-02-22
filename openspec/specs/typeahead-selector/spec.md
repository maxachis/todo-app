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

### Requirement: Keyboard navigation in typeahead dropdown
The system SHALL support keyboard-driven navigation and selection within the typeahead dropdown.

#### Scenario: ArrowDown moves highlight to next option
- **WHEN** the dropdown is open and the user presses ArrowDown
- **THEN** the highlight moves to the next option in the list (wrapping to the first option from the end)

#### Scenario: ArrowUp moves highlight to previous option
- **WHEN** the dropdown is open and the user presses ArrowUp
- **THEN** the highlight moves to the previous option in the list (wrapping to the last option from the beginning)

#### Scenario: Enter selects the highlighted option
- **WHEN** the dropdown is open and an option is highlighted and the user presses Enter
- **THEN** the highlighted option is selected, the dropdown closes, and the `onSelect` callback fires with the option's id

#### Scenario: Enter selects first option when none highlighted
- **WHEN** the dropdown is open with filtered results, no option is highlighted, and the user presses Enter
- **THEN** the first visible option is selected

#### Scenario: Escape closes the dropdown
- **WHEN** the dropdown is open and the user presses Escape
- **THEN** the dropdown closes without selecting an option

#### Scenario: Enter does not submit parent form
- **WHEN** the typeahead is inside a `<form>` and the dropdown is open and the user presses Enter
- **THEN** the form submission is prevented (only the typeahead selection occurs)

### Requirement: Action mode (fire-and-forget selection)
The system SHALL support an action mode where selecting an option fires a callback and clears the input, used for adding links.

#### Scenario: Input clears after selection in action mode
- **WHEN** the component is in action mode (no `value` prop bound) and the user selects an option
- **THEN** the `onSelect` callback fires with the selected option's id and the input text clears

#### Scenario: Escape clears input in action mode
- **WHEN** the component is in action mode and the user presses Escape
- **THEN** the input text clears and the dropdown closes

### Requirement: Bound-value mode (form field selection)
The system SHALL support a bound-value mode where selecting an option updates a bound value and displays the selected label, used for form fields.

#### Scenario: Selected option label displays in input
- **WHEN** the component is in bound-value mode and an option is selected
- **THEN** the input displays the selected option's label and the bound `value` is set to the option's id

#### Scenario: Typing replaces selected label to filter
- **WHEN** the component is in bound-value mode with a selected value and the user starts typing
- **THEN** the input text replaces the selected label and the dropdown opens with filtered options

#### Scenario: Escape reverts to selected label
- **WHEN** the component is in bound-value mode with a selected value and the dropdown is open and the user presses Escape
- **THEN** the input reverts to displaying the previously selected option's label

#### Scenario: Initial value displays label on mount
- **WHEN** the component is in bound-value mode and a `value` prop is provided on mount
- **THEN** the input displays the label of the option matching that value

### Requirement: Typeahead accessibility
The system SHALL include ARIA attributes for screen reader compatibility on the typeahead component.

#### Scenario: Combobox role is present
- **WHEN** the TypeaheadSelect component renders
- **THEN** the input has `role="combobox"`, `aria-autocomplete="list"`, and `aria-expanded` reflecting the dropdown open state

#### Scenario: Listbox role on dropdown
- **WHEN** the dropdown is open
- **THEN** the dropdown container has `role="listbox"` and each option has `role="option"`

#### Scenario: Active descendant tracks highlight
- **WHEN** an option is highlighted via keyboard
- **THEN** the input's `aria-activedescendant` references the highlighted option's id
