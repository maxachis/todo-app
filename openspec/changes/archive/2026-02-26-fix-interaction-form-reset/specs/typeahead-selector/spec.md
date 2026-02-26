## MODIFIED Requirements

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

#### Scenario: External value reset clears display text
- **WHEN** the component is in bound-value mode with a selected value and the bound `value` prop is set to `null` externally (e.g., by a parent form resetting after submission)
- **THEN** the input SHALL clear its display text to an empty string
