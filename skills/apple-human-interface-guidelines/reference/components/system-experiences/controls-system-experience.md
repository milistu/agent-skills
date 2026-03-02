# Controls (System Experience)

Guidelines for designing controls — buttons or toggles that provide quick access to app features from Control Center, Lock Screen, or the Action button (iOS/iPadOS).

## Anatomy

Controls contain:
- **Symbol image** — visually represents the control's function (SF Symbol or custom)
- **Title** — describes what the control relates to
- **Value** (optional) — represents the current state

### Display behavior by context

| Context | Displays |
|---|---|
| Control Center | Symbol; at larger sizes, title and value |
| Lock Screen | Symbol only |
| Action button (press & hold) | Symbol in Dynamic Island + value (if present) |

## Best Practices

- **Offer controls for actions that provide the most benefit without launching your app.** Example: launching a Live Activity from a control.
- **Update controls** when someone interacts with them, when an action completes, or remotely via push notification.
- **Choose a descriptive symbol** that conveys the action independently of title/value. For toggles, provide symbols for both on and off states (e.g., `door.garage.open` / `door.garage.closed`).
- **Use symbol animations** to highlight state changes. For toggles, animate between on/off states. For buttons with duration-based actions, animate indefinitely during the action and stop on completion. See `SymbolEffect`.
- **Select a tint color** aligned with your brand. Applied to toggle symbols in the on state and shown in the Dynamic Island when triggered via the Action button.
- **Prompt for configuration** if the control needs additional info (e.g., selecting a specific light). Prompt on first add; allow reconfiguration anytime. See `promptsForUserConfiguration()`.
- **Provide Action button hint text** using verbs to describe what happens on press-and-hold. See `controlWidgetActionHint(_:)`.
- **Include placeholders** for variable titles/values so the controls gallery can show what the control does.
- **Hide sensitive information on locked devices** — redact title and value; optionally redact symbol state (shows off-state symbol).
- **Require authentication for security-affecting actions** (e.g., unlocking a door, starting a car). See `IntentAuthenticationPolicy`.

## Camera Experiences on a Locked Device

iOS 18+: Controls can launch directly to your app's camera experience while the device is locked. Authentication is required for any task beyond capture.

- **Use the same camera UI** in both your app and the locked camera experience for seamless transitions.
- **Provide instructions** for adding the control that launches the camera experience.
- See `LockedCameraCapture` framework.

## Platform Support

iOS and iPadOS only. Not supported on macOS, watchOS, tvOS, or visionOS.