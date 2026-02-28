## MODIFIED Requirements

### Requirement: Bound-value mode (form field selection)
The system SHALL support a bound-value mode where selecting an option updates a bound value and displays the selected label, used for form fields. When the user blurs with unmatched text, the component SHALL auto-create (if `onCreate` is available) or revert with feedback (if not).

#### Scenario: Selected option label displays in input
- **WHEN** the component is in bound-value mode and an option is selected
- **THEN** the input displays the selected option's label and the bound `value` is set to the option's id

#### Scenario: Typing replaces selected label to filter
- **WHEN** the component is in bound-value mode with a selected value and the user starts typing
- **THEN** the input text replaces the selected label and the dropdown opens with filtered options

#### Scenario: Escape reverts to selected label
- **WHEN** the component is in bound-value mode with a selected value and the dropdown is open and the user presses Escape
- **THEN** the input reverts to displaying the previously selected option's label

#### Scenario: Escape clears input when no prior selection
- **WHEN** the component is in bound-value mode with no prior selected value and the dropdown is open and the user presses Escape
- **THEN** the input SHALL clear to empty

#### Scenario: Initial value displays label on mount
- **WHEN** the component is in bound-value mode and a `value` prop is provided on mount
- **THEN** the input displays the label of the option matching that value

#### Scenario: External value reset clears display text
- **WHEN** the component is in bound-value mode with a selected value and the bound `value` prop is set to `null` externally (e.g., by a parent form resetting after submission)
- **THEN** the input SHALL clear its display text to an empty string

#### Scenario: Blur with unmatched text auto-creates when onCreate available
- **WHEN** the component is in bound-value mode with `onCreate` provided AND the user has typed text that does not exactly match any option AND the input loses focus (click outside, Tab)
- **THEN** the component SHALL call `onCreate` with the trimmed input text, select the returned option as the current value, and close the dropdown

#### Scenario: Blur with unmatched text reverts when no onCreate
- **WHEN** the component is in bound-value mode without `onCreate` AND the user has typed text that does not match any option AND the input loses focus
- **THEN** the component SHALL revert `displayText` to the previously selected label (or empty if no prior selection) AND display a toast notification indicating no match was found for the typed text

#### Scenario: Blur with empty input does not trigger auto-create
- **WHEN** the component is in bound-value mode with `onCreate` provided AND the input is empty or whitespace-only AND the input loses focus
- **THEN** the component SHALL NOT call `onCreate` and SHALL revert to the previously selected label (or empty)

#### Scenario: Blur with matched text selects the matching option
- **WHEN** the component is in bound-value mode AND the user has typed text that exactly matches (case-insensitive) an existing option's label AND the input loses focus
- **THEN** the component SHALL select the matching option (setting `value` to its id and `displayText` to its label)

#### Scenario: Tab key triggers same blur behavior as click-outside
- **WHEN** the component is in bound-value mode with the dropdown open AND the user presses Tab
- **THEN** the same blur-with-unmatched-text behavior applies (auto-create or revert-with-toast) before focus moves to the next element
