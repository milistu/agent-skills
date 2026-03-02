# Remotes (tvOS)

Guidelines for designing Siri Remote interactions in Apple TV apps. The Siri Remote combines a clickpad and touch surface supporting swipe and press gestures.

## Best Practices

- **Use standard gestures for standard actions.** Redefining standard remote behaviors causes confusion. Only define custom gestures when it makes sense (e.g., gameplay).
- **Be consistent with the focus experience.** Always move focus in the same direction as the gesture. See Focus and Selection guidelines.
- **Provide clear feedback** for gestures — e.g., resting a thumb shows where to swipe down to reveal an info area.
- **Differentiate press vs. tap.** Pressing is intentional (choosing buttons, confirming selections, gameplay actions). Taps work for navigation but can be inadvertent (picking up remote, handing it off). Avoid responding to taps during live video playback.
- **Consider positional taps** (up/down/left/right on touch surface) for navigation or gameplay only when intuitive and discoverable.
- **Back button behavior:** Open the parent of the current screen. At the app's top level, parent = Home Screen. Exception: during active gameplay, Back should open an in-game pause menu (not navigate back); pressing Back again closes the pause menu and resumes. Press-and-hold Back always goes to Home Screen.
- **Play/Pause button:** Always play, pause, or resume media playback when pressed during media playback.

## Gestures

| Gesture | Behavior |
|---------|----------|
| **Swipe** | Scrolls through items with momentum (fast then slowing). Swiping on the edge speeds through items quickly. |
| **Press** | Activates a control or selects an item. Press before swiping activates scrubbing mode. |

## Button Behavior Reference

| Button/Area | App Behavior | Game Behavior |
|---|---|---|
| Touch surface (swipe) | Navigates. Changes focus. | Directional pad behavior. |
| Touch surface (press) | Activates control/item. Navigates deeper. | Primary button behavior. |
| Back | Returns to previous screen. Exits to Home Screen. | Pauses/resumes gameplay. Returns to previous screen, main menu, or Home Screen. |
| Play/Pause | Activates/pauses/resumes media playback. | Secondary button behavior. Skips intro video. |

## Compatible Remotes (Live TV)

Some remotes include buttons for live TV / channel-based content (EPG guide, page up/down, channel change).

- **EPG browsing buttons:** "Guide"/"browse" button should open your EPG. "Page up"/"page down" navigates the EPG. Don't repurpose these buttons while EPG is open. Tapping upper/lower Touch surface also browses EPG.
- **During content playback:** "Page up"/"page down" should change the channel (different behavior than when browsing EPG).
- If your app doesn't support EPG, the system routes these presses to the default guide app.

## Platform Support

tvOS only. Not supported on iOS, iPadOS, macOS, visionOS, or watchOS.