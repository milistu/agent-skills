# Digital Crown

Guidelines for Digital Crown interactions on Apple Vision Pro and Apple Watch.

## Apple Vision Pro

On Apple Vision Pro, people use the Digital Crown to:
- Adjust volume
- Adjust the amount of immersion in a portal, Environment, or Full Space app/game
- Recenter content in front of them
- Open Accessibility settings
- Exit an app and return to the Home View

**Note:** visionOS apps don't receive direct information from the Digital Crown — all interactions are system-level.

## Apple Watch

Starting with watchOS 10, the Digital Crown is the **primary input for navigation**:
- On watch face → turn to view widgets in Smart Stack
- On Home Screen → turn to move vertically through apps
- Within apps → turn to switch between vertically paginated tabs, scroll lists, and variable height pages

> Apps don't respond to Digital Crown **presses** — watchOS reserves these for system functionality (e.g., revealing the Home Screen).

### Haptic Feedback

Most Apple Watch models provide haptic feedback via linear haptic *detents* (taps) as the Crown is turned a specific distance. Some system controls (e.g., table views) provide detents as new items scroll onto screen.

### Design Guidelines

- **Anchor navigation to the Digital Crown.** List, tab, and scroll views should be vertically oriented so people can use the Crown to move between key interface elements. Always back Crown interactions with corresponding touch screen interactions.

- **Use the Crown to inspect data when navigation isn't needed.** Example: World Clock uses the Crown to advance time of day at a selected location.

- **Provide visual feedback** for all Digital Crown interactions. Without it, people assume turning the Crown has no effect. Pickers should change the displayed value; if tracking turns directly, update UI programmatically.

- **Match interface update speed to Crown turn speed.** People expect precise control — avoid updating content at a rate that makes value selection difficult.

- **Use default haptic feedback when appropriate.** Disable detents if they don't match your app's animation. For tables with significantly different row heights, consider linear detents instead of row-based detents for a more consistent experience.

## Platform Support

Not supported in iOS, iPadOS, macOS, or tvOS.