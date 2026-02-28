## 1. Sound Preference Store

- [x] 1.1 Create `frontend/src/lib/stores/completionSound.ts` with a writable store backed by localStorage (key: `completion-sound`). Type: `'none' | 'ding' | 'pop' | 'chime' | 'celeste'`. Default: `'ding'`. Follow the theme store pattern for initialization and persistence.

## 2. Sound Synthesis Module

- [x] 2.1 Create `frontend/src/lib/audio/completionSounds.ts` with a lazy-initialized shared AudioContext and four synthesis functions: `ding()` (sine ~800Hz, quick decay), `pop()` (sine ~400Hz, very fast decay), `chime()` (two ascending sine tones C5→E5), `celeste()` (sine + soft overtone, longer tail). Each function creates oscillator + gain nodes, plays for < 500ms, and cleans up.
- [x] 2.2 Export a `playCompletionSound(sound: CompletionSound)` function that looks up the sound name, resumes the AudioContext if suspended, and calls the corresponding synthesis function. No-op for `'none'`.

## 3. Task Completion Integration

- [x] 3.1 Modify `frontend/src/lib/components/tasks/TaskRow.svelte`: import `playCompletionSound` and the completion sound store. In `handleCheck`, when the task is not yet completed (before calling `completeTask`), call `playCompletionSound()` with the current store value. No sound on uncomplete path.

## 4. Settings UI

- [x] 4.1 Modify `frontend/src/routes/+layout.svelte`: import the completion sound store. Add a `<hr>` divider after the Export Database link, followed by a "Completion Sound" label and a `<select>` bound to the store value. Options: None, Ding, Pop, Chime, Celeste.
- [x] 4.2 Add an `on:change` handler on the select that plays the newly selected sound as a preview (unless "None" is selected).
- [x] 4.3 Style the divider, label, and select to match the dropdown's existing appearance (padding, font, colors, dark mode).

## 5. Verification

- [x] 5.1 Manual test: complete a task via checkbox — sound plays. Uncomplete — silent. Change sound in settings — preview plays. Reload — preference persists.
- [x] 5.2 Run `cd frontend && npm run check` to verify no type errors.
