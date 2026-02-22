## ADDED Requirements

### Requirement: Backup both application datasets
The system SHALL produce raw database file backups and JSON exports via `dumpdata` for both the ToDo app and the network app before any import occurs.

#### Scenario: Create backups
- **WHEN** data integration begins
- **THEN** raw DB copies and JSON exports exist for both apps

### Requirement: Import network data into unified database
The system SHALL import network app data into the unified database without modifying or deduplicating records.

#### Scenario: Import network data
- **WHEN** the network data import runs
- **THEN** all network entities and relationships are present in the unified database with original identifiers
