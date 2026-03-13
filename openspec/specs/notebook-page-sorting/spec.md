# Notebook Page Sorting

## Purpose

Sort controls for the notebook sidebar, allowing users to order pages by last updated, creation date, or title, with localStorage persistence.

## Requirements

### Requirement: Sort selector in notebook sidebar
The notebook sidebar SHALL display a sort selector above the page list allowing the user to choose the ordering of pages. The available sort options SHALL be: "Last updated" (default, `-updated_at`), "Date created" (`-created_at`), and "Title" (`title` alphabetical ascending).

#### Scenario: Default sort order
- **WHEN** the user opens the notebook page with no prior sort preference
- **THEN** pages in the sidebar SHALL be ordered by last updated (most recent first)

#### Scenario: Sort by created date
- **WHEN** the user selects "Date created" from the sort selector
- **THEN** pages in the sidebar SHALL be re-ordered by creation date (most recent first)

#### Scenario: Sort by title
- **WHEN** the user selects "Title" from the sort selector
- **THEN** pages in the sidebar SHALL be ordered alphabetically by title (A-Z)

### Requirement: Sort preference persisted in localStorage
The selected sort order SHALL be persisted in localStorage under the key `notebook-sort-order`. On page load, the sort selector SHALL restore the previously selected option. If no preference is stored, the default SHALL be "Last updated".

#### Scenario: Sort preference survives refresh
- **WHEN** the user selects "Date created" and refreshes the page
- **THEN** the sort selector SHALL show "Date created" as selected and pages SHALL be ordered by creation date
