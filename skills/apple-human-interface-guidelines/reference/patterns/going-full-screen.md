# Going Full Screen

Guidelines for implementing full-screen modes on iPhone, iPad, and Mac. Not applicable to tvOS, watchOS (apps already fill screen), or visionOS (use immersive experiences instead).

## Best Practices

- **Support full-screen mode when appropriate** — games, media viewing (videos, photo slideshows), or in-depth tasks benefiting from distraction-free environments.
- **Adjust layout but don't programmatically resize the window** — Keep essential content prominent while using extra space. Adjustments should be subtle to maintain consistency and avoid jarring transitions between modes.
- **Keep essential features accessible** — People should complete their task without exiting full-screen mode. E.g., playback controls should be persistently available or easy to reveal.
- **Preserve Dock access (except in games)** — On iPadOS/macOS, let people reveal the Dock. For games, you can defer the initial swipe gesture on iPadOS (`preferredScreenEdgesDeferringSystemGestures`) or hide the Dock on macOS (`NSApplication.PresentationOptions.hideDock`).
- **Resume where they left off** — When people return after switching away, restore their state. Pause games/slideshows automatically when they leave.
- **Let people choose when to exit** — Don't end full-screen mode automatically when users switch to a different experience or finish an activity.
- **Temporarily hide toolbars and navigation controls to prioritize content** — Hide non-essential chrome when content is primary (e.g., full-screen photos, reading). Let people restore hidden elements with familiar gestures (tap, swipe down, cursor to top of screen). Keep controls visible when essential for navigation.

## Platform-Specific Guidance

### iOS / iPadOS

- **Defer system gestures to prevent accidental exits** — By default, the Home Screen indicator auto-hides and reappears on bottom-edge interaction. Retain this default behavior when possible. If it causes unexpected exits, enable two-swipe exit instead of one via `preferredScreenEdgesDeferringSystemGestures`.

### macOS

- **Use the system-provided full-screen experience** — Ensures proper behavior in all contexts, including automatic accommodation of the camera housing area. Use `toggleFullScreen(_:)`.
- **Don't change display mode when players go full screen in games** — People expect control of their display mode; changing it doesn't improve performance.
- **Let people choose when to enter full-screen mode** — Support the Enter Full Screen button, View menu item, or Control-Command-F shortcut. Avoid custom window mode menus. Games may additionally provide a custom toggle.

## Key Developer APIs

| API | Framework | Purpose |
|---|---|---|
| `preferredScreenEdgesDeferringSystemGestures` | SwiftUI / UIKit | Defer system edge gestures in full-screen apps/games |
| `NSApplication.PresentationOptions.hideDock` | AppKit | Hide Dock in full-screen macOS games |
| `toggleFullScreen(_:)` | AppKit | System full-screen support on macOS |
| `fullScreenCover(item:onDismiss:content:)` | SwiftUI | Present full-screen modal covers |
| `NSWindow.CollectionBehavior` | AppKit | Configure window full-screen behavior |