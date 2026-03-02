# Multitasking

Guidelines for supporting multitasking across Apple platforms, ensuring apps work well when users switch between apps or view multiple apps simultaneously.

## Best Practices

- **Pause attention-requiring activities when users switch away.** Games and media-viewing apps should pause so users don't miss anything. Let them continue seamlessly when they return.

- **Respond smoothly to audio interruptions:**
  - Pause audio indefinitely for primary interruptions (music, podcasts, audiobooks)
  - Temporarily lower volume or pause for shorter interruptions (e.g., GPS notifications), resuming when the interruption ends

- **Finish user-initiated tasks in the background.** Tasks like downloading assets or processing video should complete even after the user switches away. Complete background work before suspending.

- **Use notifications sparingly.** Notify for important/time-sensitive task completion. Avoid notifications for routine or secondary tasks — let users check when they return.

## Platform Considerations

**Not supported in watchOS.**

### iOS
- Multitasking includes app switching and Picture in Picture (FaceTime, video)
- App switcher displays all currently open apps

### iPadOS
- People can view and interact with windows of several apps simultaneously
- Individual apps can support multiple open windows
- **Full-screen mode:** Apps occupy full screen; switch via app switcher
- **Windowed mode:** Windows are resizable (similar to macOS). System provides window controls for tiling, full screen, minimize, and close. Frontmost window has colored controls and casts drop shadow.
- Picture in Picture works in both full-screen and windowed modes
- Apps don't control multitasking configurations or receive indication of user choices
- Ensure your app adapts gracefully to different screen sizes (see Layout and Windows guidelines)

### macOS
- Multitasking is the default experience — users typically run multiple apps simultaneously
- macOS uses drop shadows for layered windows and visual effects to distinguish window states

### tvOS
- Picture in Picture support for movies/TV shows while browsing other content

### visionOS
- Multiple apps run simultaneously in the Shared Space with windows and volumes
- Only one window is active at a time; looking at a window makes it active while others become more translucent and recede along z-axis
- Closing a window transitions the app to background without quitting
- When an app is the Now Playing app, closing its window pauses audio playback (resumable via Control Center)
- **Don't interfere with system multitasking behavior.** Don't change window edge appearance — visionOS applies a feathered mask to inactive windows
- **Don't pause video playback when users look away** — users expect playback to continue (same as macOS)
- **Be prepared for audio ducking** — unless your app is the Now Playing app, its audio can duck when users look away to another app