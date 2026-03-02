# Accessibility Guidelines

Design guidelines for creating accessible Apple platform interfaces across vision, hearing, mobility, speech, and cognitive considerations.

## Core Principles

An accessible interface is:
- **Intuitive** — Familiar, consistent interactions for straightforward tasks
- **Perceivable** — Doesn't rely on any single method to convey information
- **Adaptable** — Supports system accessibility features and personalization

## Vision

### Text Size

- Support text enlargement of at least **200%** (140% for watchOS)
- Adopt Dynamic Type for automatic system-wide text size adjustment

#### Default and Minimum Type Sizes by Platform

| Platform | Default size | Minimum size |
| --- | --- | --- |
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

- Thin font weights need larger sizes for legibility; thicker weights are more readable at smaller sizes

### Color Contrast (WCAG Level AA)

| Text size | Text weight | Minimum contrast ratio |
| --- | --- | --- |
| Up to 17 pts | All | 4.5:1 |
| 18 pts | All | 3:1 |
| All | Bold | 3:1 |

- If your app doesn't meet minimum contrast by default, provide a higher contrast scheme when **Increase Contrast** is enabled
- Check contrast in both light and dark appearances
- Prefer **system-defined colors** — they automatically adapt for Increase Contrast and light/dark modes

### Color Independence

- Never convey information with color alone
- Use distinct shapes, icons, or other visual indicators alongside color
- Consider letting users customize color schemes (e.g., chart colors, game characters)

### VoiceOver

- Describe your app's interface and content for VoiceOver (see VoiceOver guidelines)

## Hearing

- **Captions** — Textual equivalent of audible info synced with media
- **Subtitles** — Onscreen dialogue in preferred language
- **Audio descriptions** — Spoken narration of visual-only information during natural pauses
- **Transcripts** — Complete textual description covering both audible and visual info
- Allow people to customize visual presentation of text-based alternatives
- **Pair audio cues with haptics** for people who can't perceive audio
- **Augment audio cues with visual cues**, especially for off-screen content in games and spatial apps

## Mobility

### Control Sizes

| Platform | Default control size | Minimum control size |
| --- | --- | --- |
| iOS, iPadOS | 44×44 pt | 28×28 pt |
| macOS | 28×28 pt | 20×20 pt |
| tvOS | 66×66 pt | 56×56 pt |
| visionOS | 60×60 pt | 28×28 pt |
| watchOS | 44×44 pt | 28×28 pt |

### Spacing

- ~12 pt padding around elements with a bezel
- ~24 pt padding around elements without a bezel (around visible edges)

### Gestures & Interaction

- Use simplest gesture possible for common interactions; avoid custom multifinger/multihand gestures
- Provide onscreen alternatives (e.g., a button) for every gesture-based action
- Support Voice Control by labeling interface elements appropriately
- Integrate with Siri and Shortcuts for voice-only task completion
- Support assistive technologies: VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control, Switch Control

## Speech

- Support Full Keyboard Access — don't override system-defined keyboard shortcuts
- Support Switch Control for hardware, game controller, and sound-based device control

## Cognitive

- Keep actions simple with familiar system gestures and behaviors
- **Avoid time-boxed UI** — prefer explicit dismiss actions over auto-dismiss timers
- Consider difficulty accommodations in games (adjustable difficulty, reaction time, control assistance)
- Avoid autoplaying audio/video without discoverable start/stop controls
- Respect **Dim Flashing Lights** setting for video playback
- Respect **Reduce Motion** setting:
  - Reduce automatic/repetitive animations
  - Tighten animation springs to reduce bounce
  - Track animations directly with gestures
  - Avoid animating depth changes in z-axis
  - Replace x/y/z transitions with fades
  - Avoid animating into and out of blurs

### Assistive Access (iOS/iPadOS)

When Assistive Access is enabled:
- Identify core functionality; remove noncritical workflows and UI elements
- Break multistep workflows into single-interaction-per-screen flows
- Always ask for confirmation **twice** for destructive/hard-to-recover actions

## visionOS Considerations

Prioritize comfort in immersive experiences:
- Keep UI within the person's field of view; prefer horizontal over vertical layouts
- Reduce speed/intensity of animated objects, especially in peripheral vision
- Be gentle with camera/video motion; avoid uncontrolled world movement
- Don't anchor content to the wearer's head (blocks Pointer Control)
- Minimize large/repetitive gestures