## Context

The app uses a comprehensive CSS custom property system defined in `:root` within `+layout.svelte` (lines 85–138). All 40+ variables cover backgrounds, text, accents, borders, shadows, status colors, pinned-task colors, and tag colors. Components consume these variables in scoped `<style>` blocks. There is no external CSS framework.

The top navigation bar is a dark strip (`--bg-nav: #2c2825`) with light text. The rest of the UI is a warm beige/white palette. Theme switching needs to invert the main surfaces while keeping the nav bar usable and the accent color legible.

## Goals / Non-Goals

**Goals:**
- Users can switch between light, dark, and system-follow themes
- Theme preference persists across sessions via `localStorage`
- The system respects `prefers-color-scheme` when set to "system"
- No flash of wrong theme on page load (FOUC prevention)
- Zero new runtime dependencies

**Non-Goals:**
- Custom color palette editor
- Per-page or per-component theme overrides
- Server-side theme detection (no backend changes)
- Animated theme transitions between light and dark

## Decisions

### 1. CSS class toggle on `<html>` element

**Choice:** Apply a `data-theme="dark"` attribute on `<html>` and override CSS variables via `:root[data-theme="dark"]`.

**Alternatives considered:**
- `prefers-color-scheme` media query only — no manual toggle possible, ruled out.
- Class on `<body>` — `<html>` is conventional and allows the inline script to set it before body renders.

**Rationale:** Attribute on `<html>` is set by an inline `<script>` in `app.html` before the body paints, preventing FOUC. The Svelte store then syncs with this attribute at runtime.

### 2. Inline script in `app.html` for FOUC prevention

**Choice:** Add a `<script>` block in `<head>` of `frontend/src/app.html` that reads `localStorage` and sets `data-theme` before any CSS renders.

```
const saved = localStorage.getItem('theme');
const prefersDark = matchMedia('(prefers-color-scheme: dark)').matches;
const theme = saved === 'dark' || (saved !== 'light' && prefersDark) ? 'dark' : 'light';
document.documentElement.dataset.theme = theme;
```

**Rationale:** Svelte stores initialize after hydration; without this, users would see a light flash then dark switch. The inline script runs synchronously during parse.

### 3. Svelte store for runtime theme management

**Choice:** Create `frontend/src/lib/stores/theme.ts` with a writable store holding `'light' | 'dark' | 'system'`. The store:
- Reads initial value from `localStorage` (defaulting to `'system'`)
- On change, writes to `localStorage` and updates `document.documentElement.dataset.theme`
- When set to `'system'`, listens to `matchMedia('(prefers-color-scheme: dark)')` change events

**Alternatives considered:**
- Component-local state — wouldn't allow other components to react to theme changes.
- Context API — overkill for a single global value.

### 4. Toggle UI placement

**Choice:** Add a three-state toggle (light / system / dark) in the top navigation bar, between the nav links and the search bar.

**Rationale:** The nav bar is always visible, accessible from every page, and already has controls. A three-state toggle is clearer than a two-state button with hidden "system" behavior.

### 5. Dark palette strategy

**Choice:** Override all existing CSS variables under `:root[data-theme="dark"]` in `+layout.svelte`, keeping the same variable names. No new variables needed.

Key dark values:
- `--bg-page`: `#1a1816` (warm dark, not pure black)
- `--bg-surface`: `#262220` (slightly lighter warm dark)
- `--bg-nav`: `#1a1816` (blends with page in dark mode)
- `--text-primary`: `#ede9e1` (current `--text-on-dark` value)
- `--accent`: `#d4753e` (slightly brighter warm orange for dark backgrounds)
- Shadows reduced to near-zero opacity (dark on dark is invisible)

**Rationale:** Warm dark tones maintain the app's earthy personality. Pure black (#000) causes excessive contrast and looks clinical.

## Risks / Trade-offs

- **Hardcoded colors in components** → Audit needed; any component using hex/rgb literals outside CSS variables will not respond to theme changes. Mitigation: search for hardcoded color values and migrate them before declaring the feature complete.
- **Third-party component styling** → `svelte-dnd-action` may inject inline styles during drag. Mitigation: verify drag ghost elements are legible in dark mode; override via CSS if needed.
- **FOUC on very slow connections** → The inline script approach is reliable but adds ~200 bytes to `app.html`. Acceptable trade-off.
- **Emoji picker contrast** → The custom emoji picker has its own background/text styling. Mitigation: ensure it uses CSS variables throughout.

## Open Questions

- None — all decisions are straightforward given the existing CSS variable architecture.
