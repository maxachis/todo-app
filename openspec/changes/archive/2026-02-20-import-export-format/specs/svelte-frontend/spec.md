## MODIFIED Requirements

### Requirement: Import page
The system SHALL provide a dedicated page at `/import` for importing tasks from TickTick CSV files, the app's native JSON export, and the app's native CSV export.

#### Scenario: Upload CSV file
- **WHEN** the user selects a `.csv` file and submits the import form
- **THEN** the file is uploaded to the API and a summary shows counts of created/skipped entities

#### Scenario: Upload JSON file
- **WHEN** the user selects a `.json` file and submits the import form
- **THEN** the file is uploaded to the API and a summary shows counts of created/skipped entities

#### Scenario: Import error display
- **WHEN** the import fails (invalid file, parse error, unrecognized format)
- **THEN** the error message is displayed to the user

#### Scenario: File picker accepts JSON and CSV
- **WHEN** the user clicks the file input on the import page
- **THEN** the file picker filters for `.csv` and `.json` files
