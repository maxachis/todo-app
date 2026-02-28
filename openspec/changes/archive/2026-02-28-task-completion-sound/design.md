## Context

Task completion currently has visual feedback (checkbox pop animation, opacity fade, toast notification) but no audio feedback. The Web Audio API is available in all modern browsers and can synthesize short tones without loading external audio files. The app already has a localStorage-backed preference pattern (theme store) and a settings dropdown in the navbar.

## Goals / Non-Goals

**Goals:**
- Play a synthesized sound immediately when a task is completed (optimistic, before API response)
- Offer four distinct sound options plus a "None" option to disable
- Persist the user's sound preference in localStorage
- Expose the preference in the existing settings dropdown with an inline selector

**Non-Goals:**
- Volume control (defer to browser/OS volume)
- Custom/uploaded sounds
- Sounds for any action other than task completion
- Backend changes

## Decisions

### 1. Web Audio API over audio files

**Choice**: Synthesize all sounds using the Web Audio API (OscillatorNode + GainNode).

**Alternatives considered**:
- Bundled `.mp3`/`.ogg` files: Adds asset management, licensing concerns, and build complexity for four short tones
- Howler.js or Tone.js: Overkill for four simple sound effects with no advanced audio needs

**Rationale**: Web Audio API is a browser built-in with zero dependencies. Each sound is ~10-20 lines of code. The sounds are short tones (< 500ms) well within what oscillators can produce pleasantly.

### 2. Shared AudioContext with lazy initialization

**Choice**: Create a single `AudioContext` lazily on first use and reuse it across all playback calls.

**Rationale**: Browsers restrict `AudioContext` creation to user gesture contexts. Creating it lazily on the first checkbox click (a user gesture) satisfies this requirement. Reusing it avoids the overhead of creating/closing contexts repeatedly. The context is resumed if suspended (browsers may suspend inactive contexts).

### 3. Sound preference store follows theme store pattern

**Choice**: New `completionSound.ts` store with the same pattern as `theme.ts` — writable store initialized from localStorage, subscriber persists changes.

**Rationale**: Consistent with existing codebase patterns. No new abstractions needed.

### 4. Sound plays in TaskRow.handleCheck, not in the store

**Choice**: Call `playCompletionSound()` directly in `TaskRow.svelte`'s `handleCheck` function, before calling `completeTask()`.

**Alternatives considered**:
- Playing inside the `completeTask` store function: Would also fire for any programmatic completion, and mixes UI concerns into the data layer
- Playing after API success: Adds latency, breaks the optimistic feel

**Rationale**: The sound is UI feedback, like the checkbox animation. It belongs in the component that handles the user interaction. Playing before `completeTask()` ensures it's optimistic and instant.

### 5. Inline select in settings dropdown

**Choice**: Add a `<select>` element inside the settings dropdown, below a visual divider separating it from the link items.

**Alternatives considered**:
- Dedicated settings page: Overbuilt for a single preference (could revisit if more preferences accumulate)
- Custom dropdown component: Unnecessary when a native `<select>` works and matches the lightweight approach

**Rationale**: Minimal change to existing UI. The divider visually separates navigation actions (Import, Export) from preferences (Sound). The `<select>` is compact and familiar.

## Risks / Trade-offs

- **[Browser autoplay policy]** → Mitigated by lazy AudioContext creation on user gesture (checkbox click). All major browsers allow audio initiated by click events.
- **[Sound quality]** → Synthesized tones are simple but effective. If users want richer sounds later, could add audio file support as a separate change.
- **[Mobile Safari AudioContext quirks]** → Mitigated by resuming the AudioContext if it's in a suspended state before playing.
