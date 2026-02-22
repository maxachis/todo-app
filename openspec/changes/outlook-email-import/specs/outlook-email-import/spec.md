## ADDED Requirements

### Requirement: OAuth Device Code authentication command
The system SHALL provide a Django management command `outlook_auth` that performs the Microsoft OAuth 2.0 Device Code flow, obtains access and refresh tokens, and persists them to a token cache file.

#### Scenario: First-time authentication
- **WHEN** the user runs `manage.py outlook_auth` with valid `OUTLOOK_CLIENT_ID` configured
- **THEN** the command prints a URL and a device code, waits for the user to authorize in a browser, and saves tokens to the token cache file

#### Scenario: Token cache already exists
- **WHEN** the user runs `manage.py outlook_auth` and a valid token cache file already exists with a non-expired refresh token
- **THEN** the command reports that authentication is already active and offers to re-authenticate

#### Scenario: Missing client ID configuration
- **WHEN** the user runs `manage.py outlook_auth` and `OUTLOOK_CLIENT_ID` is not configured
- **THEN** the command exits with an error message identifying the missing setting

### Requirement: Graph API email polling management command
The system SHALL provide a Django management command `poll_outlook` that queries the Microsoft Graph API for emails tagged with a configured category, creates tasks from them, and replaces the category with a "processed" category — without changing read/unread status or moving the emails.

#### Scenario: Successful poll creates tasks from category-tagged emails
- **WHEN** the `poll_outlook` command runs and 3 emails have the "ToDo" category
- **THEN** 3 new tasks are created in the "Email Inbox" list and the "ToDo" category on each email is replaced with "ToDo-Imported"

#### Scenario: Poll with no matching emails
- **WHEN** the `poll_outlook` command runs and no emails have the "ToDo" category
- **THEN** no tasks are created and the command exits successfully

#### Scenario: Poll does not change email read/unread status
- **WHEN** the `poll_outlook` command processes an unread email
- **THEN** the email remains unread after processing

#### Scenario: Poll does not move emails
- **WHEN** the `poll_outlook` command processes an email in any folder
- **THEN** the email remains in its original folder after processing

#### Scenario: Poll is idempotent via Message-ID deduplication
- **WHEN** the `poll_outlook` command runs and an email's `internetMessageId` already exists as a task's `external_id`
- **THEN** that email is skipped (no duplicate task created) and its category is still replaced with "ToDo-Imported"

#### Scenario: Poll handles expired access token via automatic refresh
- **WHEN** the `poll_outlook` command runs and the access token has expired but the refresh token is valid
- **THEN** the token is automatically refreshed and the poll proceeds normally

#### Scenario: Poll fails on expired refresh token
- **WHEN** the `poll_outlook` command runs and both access and refresh tokens have expired
- **THEN** the command writes an error to the status file indicating re-authentication is needed, and exits with a non-zero exit code

#### Scenario: Command exits with clear error on API failure
- **WHEN** the `poll_outlook` command runs and the Graph API returns an error (network failure, permission denied, etc.)
- **THEN** the command logs the error and writes it to the poll status file, then exits with a non-zero exit code

### Requirement: Email-to-task field mapping
The system SHALL map email fields to task fields when creating a task from an email.

#### Scenario: Email subject becomes task title
- **WHEN** a task is created from an email with subject "Review Q3 budget proposal"
- **THEN** the task's `title` is "Review Q3 budget proposal"

#### Scenario: Email HTML body is converted to plain text for task notes
- **WHEN** a task is created from an email with an HTML body containing paragraphs, links, and formatting
- **THEN** the task's `notes` field contains a readable plain-text conversion with basic structure preserved (paragraph breaks, link URLs)

#### Scenario: Email body is truncated at length limit
- **WHEN** a task is created from an email whose converted plain-text body exceeds 10,000 characters
- **THEN** the task's `notes` field contains the first 10,000 characters followed by a truncation indicator

#### Scenario: Email Message-ID stored as external_id
- **WHEN** a task is created from an email
- **THEN** the email's `internetMessageId` value is stored in the task's `external_id` field

#### Scenario: Email sender stored in task notes
- **WHEN** a task is created from an email with sender "Jane Doe <jane@example.com>"
- **THEN** the task's `notes` field begins with "From: Jane Doe <jane@example.com>" followed by the email body

### Requirement: Dedicated Email Inbox list
The system SHALL auto-create a dedicated list for imported email-tasks if it does not already exist.

#### Scenario: Email Inbox list is created on first poll
- **WHEN** the `poll_outlook` command runs for the first time and no list with the configured inbox name exists
- **THEN** a new list is created with the configured name (default: "Email Inbox") and a default section

#### Scenario: Email Inbox list is reused on subsequent polls
- **WHEN** the `poll_outlook` command runs and a list with the configured inbox name already exists
- **THEN** new email-tasks are created in the existing list's default section

### Requirement: Graph API configuration via Django settings
The system SHALL read Microsoft Graph API configuration from Django settings, with values sourced from environment variables.

#### Scenario: All required settings configured
- **WHEN** the environment variables `OUTLOOK_CLIENT_ID` is set
- **THEN** the management commands use this value for OAuth authentication

#### Scenario: Missing required settings
- **WHEN** the `poll_outlook` command runs and `OUTLOOK_CLIENT_ID` is not configured
- **THEN** the command exits with an error message identifying the missing setting

#### Scenario: Default values for optional settings
- **WHEN** `OUTLOOK_TENANT_ID` is not set
- **THEN** the system defaults to `consumers` (personal Microsoft accounts)
- **WHEN** `OUTLOOK_SOURCE_CATEGORY` is not set
- **THEN** the system defaults to `ToDo`
- **WHEN** `OUTLOOK_PROCESSED_CATEGORY` is not set
- **THEN** the system defaults to `ToDo-Imported`
- **WHEN** `OUTLOOK_INBOX_LIST_NAME` is not set
- **THEN** the system defaults to `Email Inbox`
- **WHEN** `OUTLOOK_TOKEN_CACHE_FILE` is not set
- **THEN** the system defaults to `outlook_token_cache.json` in the project base directory

### Requirement: Poll status reporting
The system SHALL write poll results to a status file that can be read by the API to surface errors to the user.

#### Scenario: Successful poll writes status
- **WHEN** the `poll_outlook` command completes successfully
- **THEN** a JSON status file is written containing `timestamp`, `status: "success"`, `tasks_created` count, and `tasks_skipped` count

#### Scenario: Failed poll writes error status
- **WHEN** the `poll_outlook` command encounters an error
- **THEN** a JSON status file is written containing `timestamp`, `status: "error"`, and `error` message

#### Scenario: API endpoint returns poll status
- **WHEN** a GET request is made to `/api/import/outlook/status/`
- **THEN** the response contains the contents of the most recent poll status file

#### Scenario: Frontend shows toast on poll error
- **WHEN** the frontend loads and the poll status endpoint returns `status: "error"`
- **THEN** an error toast is displayed with the error message from the last poll

#### Scenario: Frontend shows no toast on successful poll
- **WHEN** the frontend loads and the poll status endpoint returns `status: "success"`
- **THEN** no error toast is displayed
