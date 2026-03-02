# Playing Haptics

Guidelines for using haptic feedback across Apple platforms to engage people's sense of touch.

## Best Practices

- **Use system-provided haptic patterns according to their documented meanings.** People recognize standard haptics from consistent system use. If a pattern's documented use case doesn't fit, use a generic pattern or create a custom one.
- **Use haptics consistently.** Build clear cause-and-effect relationships between haptics and actions. Don't reuse the same pattern for both positive and negative outcomes.
- **Complement other feedback.** Match haptic intensity/sharpness with accompanying animations. Synchronize sound with haptics.
- **Avoid overusing haptics.** Occasional haptics feel right; frequent ones become tiresome. The best haptic experience is one people miss when turned off.
- **Prefer short haptics for discrete events in most apps.** Long-running haptics suit gameplay but dilute meaning in apps. On Apple Pencil Pro, continuous haptics make holding the pencil less pleasant.
- **Make haptics optional.** Let people turn off or mute haptics; ensure the app works without them.
- **Avoid disrupting other device features.** Haptic vibrations can impact the camera, gyroscope, or microphone.

## Custom Haptics

Games commonly use custom haptics; nongame apps can too for richer experiences.

### Building Blocks

| Type | Feel | Example |
|------|------|---------|
| **Transient** | Brief, compact taps or impulses | Tapping the Flashlight button on Home Screen |
| **Continuous** | Sustained vibrations | Lasers effect in Messages |

### Parameters

- **Sharpness** — Abstracts the waveform character: soft/rounded/organic vs. crisp/precise/mechanical
- **Intensity** — Strength of the haptic

Combine transient and continuous events with varying sharpness/intensity and optional audio for a wide range of experiences. See [Core Haptics](https://developer.apple.com/documentation/CoreHaptics).

## iOS Haptic Patterns

On supported iPhone models, use standard UI components (toggles, sliders, pickers) for automatic system haptics, or use `UIFeedbackGenerator` for predefined patterns:

### Notification Haptics

Feedback about task/action outcomes.

| Pattern | Use |
|---------|-----|
| **Success** | Task or action completed |
| **Warning** | Task or action produced a warning |
| **Error** | An error occurred |

### Impact Haptics

Physical metaphor complementing visual experiences.

| Pattern | Use |
|---------|-----|
| **Light** | Collision between small/lightweight UI objects |
| **Medium** | Collision between medium-sized/weight UI objects |
| **Heavy** | Collision between large/heavyweight UI objects |
| **Rigid** | Collision between hard/inflexible UI objects |
| **Soft** | Collision between soft/flexible UI objects |

### Selection Haptics

| Pattern | Use |
|---------|-----|
| **Selection** | UI element's values are changing |

## macOS Haptic Patterns

Available with Magic Trackpad via `NSHapticFeedbackPerformer`:

| Pattern | Use |
|---------|-----|
| **Alignment** | Dragged item aligns with another object, reaches min/max, or snaps to position |
| **Level change** | Movement between discrete levels of pressure (e.g., fast-forward speed changes) |
| **Generic** | General feedback when other patterns don't apply |

## watchOS Haptic Patterns

Apple Watch Series 4+ provides Digital Crown haptic detents. Use `WKHapticType` for these patterns:

| Pattern | Use |
|---------|-----|
| **Notification** | Something significant happened requiring attention |
| **Up** | Important value increased above a significant threshold |
| **Down** | Important value decreased below a significant threshold |
| **Success** | Action completed successfully |
| **Failure** | Action failed |
| **Retry** | Action failed but can be retried |
| **Start** | Activity started (e.g., timer). Usually paired with Stop |
| **Stop** | Activity stopped (previously started by user) |
| **Click** | Dial clicking sensation for progress at predefined increments. Avoid overuse — overlapping clicks are confusing |

## External Device Haptics

- **Game controllers** (iPadOS, macOS, tvOS, visionOS): See [Playing Haptics on Game Controllers](https://developer.apple.com/documentation/CoreHaptics/playing-haptics-on-game-controllers)
- **Apple Pencil Pro** and some trackpads on certain iPad models