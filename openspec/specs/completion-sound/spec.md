### Requirement: Sound plays on task completion
The system SHALL play the user's selected completion sound immediately when a task is marked as completed, before the API call is made. The sound SHALL play for both checkbox clicks and keyboard shortcut (X key) completion.

#### Scenario: Completing a task via checkbox plays sound
- **WHEN** the user clicks the checkbox on an incomplete task
- **THEN** the selected completion sound plays immediately

#### Scenario: Completing a task via keyboard plays sound
- **WHEN** the user presses X to complete the selected task
- **THEN** the selected completion sound plays immediately

#### Scenario: Sound plays before API response
- **WHEN** the user completes a task
- **THEN** the sound plays before the completion API call resolves

### Requirement: No sound on uncomplete
The system SHALL NOT play any sound when a task is uncompleted, whether via direct checkbox toggle or the Undo action in the toast notification.

#### Scenario: Uncompleting a task is silent
- **WHEN** the user clicks the checkbox on a completed task to uncomplete it
- **THEN** no sound plays

#### Scenario: Undo completion is silent
- **WHEN** the user clicks "Undo" on the completion toast
- **THEN** no sound plays

### Requirement: Single sound per completion action
The system SHALL play exactly one sound per user-initiated completion action, regardless of how many subtasks are recursively completed by the backend.

#### Scenario: Completing a parent with subtasks plays one sound
- **WHEN** the user completes a task that has incomplete subtasks
- **THEN** exactly one sound plays (not one per subtask)

### Requirement: Sound preference persistence
The system SHALL persist the user's completion sound preference in localStorage under the key `completion-sound`. The preference SHALL survive page reloads and browser restarts.

#### Scenario: Sound preference persists across reload
- **WHEN** the user selects "Chime" as their completion sound and reloads the page
- **THEN** "Chime" remains the selected sound and plays on next completion

#### Scenario: Default sound on first visit
- **WHEN** no completion sound preference exists in localStorage
- **THEN** the system defaults to "Ding"

### Requirement: Sound options
The system SHALL offer exactly five sound options: "Ding", "Pop", "Chime", "Celeste", and "None". Selecting "None" SHALL disable completion sounds entirely.

#### Scenario: Selecting None disables sound
- **WHEN** the user selects "None" as their completion sound
- **THEN** no sound plays when completing tasks

#### Scenario: Each sound option is distinct
- **WHEN** the user selects each sound option in turn and completes a task
- **THEN** each option produces an audibly distinct sound (or silence for None)

### Requirement: Web Audio API synthesis
All sounds SHALL be synthesized using the Web Audio API (OscillatorNode, GainNode) with no external audio files. A shared AudioContext SHALL be created lazily on the first completion and reused for subsequent playback.

#### Scenario: Sound plays without network requests
- **WHEN** the user completes a task with sound enabled
- **THEN** the sound plays using only the Web Audio API with no network requests for audio data

#### Scenario: AudioContext created on first completion
- **WHEN** the user completes a task for the first time in a session
- **THEN** an AudioContext is created and the sound plays successfully

#### Scenario: Suspended AudioContext is resumed
- **WHEN** the browser has suspended the AudioContext due to inactivity
- **THEN** the system resumes it before playing the sound
