## MODIFIED Requirements

### Requirement: Dark color palette via CSS variable overrides
The system SHALL define a dark theme by overriding all CSS custom properties under `:root[data-theme="dark"]`. The dark palette SHALL use warm dark tones (not pure black) to maintain visual consistency with the light theme's earthy character. All interactive input elements (text inputs, textareas) SHALL explicitly use `--bg-input` for background and `--text-primary` for text color via their component-scoped CSS, ensuring readability across all theme modes.

#### Scenario: Dark variables override light defaults
- **WHEN** the `<html>` element has `data-theme="dark"`
- **THEN** all CSS custom properties (backgrounds, text, borders, accents, shadows, status colors, pinned colors, tag colors) reflect dark-appropriate values

#### Scenario: Light theme remains the default
- **WHEN** no `data-theme` attribute is set on `<html>`
- **THEN** the existing light color palette applies unchanged

#### Scenario: All components respond to theme change
- **WHEN** the theme switches from light to dark or vice versa
- **THEN** all UI surfaces, text, borders, and interactive elements update without page reload

#### Scenario: Inline-edit inputs are readable in dark mode
- **WHEN** the user activates an inline-edit input (task title, section name, list name, project name, or markdown editor) in dark mode
- **THEN** the input SHALL display text in `--text-primary` color on a `--bg-input` background

#### Scenario: Inline-edit inputs are readable in light mode
- **WHEN** the user activates an inline-edit input in light mode
- **THEN** the input SHALL display text in `--text-primary` color on a `--bg-input` background, consistent with the light theme palette
