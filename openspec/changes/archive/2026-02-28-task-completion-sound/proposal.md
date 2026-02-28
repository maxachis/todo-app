## Why

Completing a task is the most rewarding moment in a task manager, but it currently only has visual feedback (checkbox animation, opacity fade, toast). A short, pleasant audio cue on completion adds a satisfying sensory reward that reinforces the habit loop and makes checking things off feel genuinely good.

## What Changes

- **Synthesized completion sounds**: Four distinct sounds generated via the Web Audio API (no audio file assets) — Ding, Pop, Chime, and Celeste
- **Sound preference store**: New localStorage-backed Svelte store for the user's chosen sound (or "None" to disable)
- **Settings UI expansion**: The existing settings cog dropdown gains an inline sound selector, separated from the link items by a divider
- **Optimistic playback**: Sound fires immediately on checkbox click / keyboard shortcut, before the API call completes
- **Silent on undo**: Uncompleting a task (including via the toast Undo button) does not play a sound

## Non-goals

- Background/ambient sounds or other UI sound effects beyond task completion
- User-uploadable custom sounds
- Volume control (browser volume is sufficient)
- Sound on subtask auto-completion (backend handles recursive completion; frontend triggers once)

## Capabilities

### New Capabilities

- `completion-sound`: Audio feedback on task completion — sound synthesis, preference storage, and settings UI

### Modified Capabilities

- `settings-menu`: Adding the completion sound selector as an inline control in the settings dropdown

## Impact

- **New files**: `frontend/src/lib/stores/completionSound.ts`, `frontend/src/lib/audio/completionSounds.ts`
- **Modified files**: `frontend/src/lib/components/tasks/TaskRow.svelte` (play sound in handleCheck), `frontend/src/routes/+layout.svelte` (sound selector in settings dropdown)
- **Dependencies**: None — Web Audio API is a browser built-in
- **APIs**: No backend changes
