# Launching

Guidelines for creating a streamlined launch experience across Apple platforms.

## Best Practices

- **Launch instantly.** People expect to start interacting within a couple of seconds.
- **Provide a launch screen on platforms that require it** (iOS, iPadOS, tvOS). macOS, visionOS, and watchOS don't require launch screens.
- **Consider displaying a splash screen at the beginning of your onboarding flow** if you need one. If no onboarding, display it as soon as launching completes. A splash screen is distinct from a launch screen.
- **Restore previous state on restart.** Restore granular details: scroll position, window state/location, etc. Don't make people retrace steps.

## Launch Screens

*Applies to iOS, iPadOS, and tvOS only.*

- **Downplay the launch experience.** A launch screen is not an onboarding screen, splash screen, or branding opportunity. Its sole function is to enhance the perception of quick launch.
- **Design nearly identical to your first screen.** Mismatches cause an unpleasant flash. If your app shows a solid color before the first screen, create a launch screen with just that color.
- **Match the device's current orientation and appearance mode.**
- **Avoid text on launch screens.** Launch screen content doesn't change and won't be localized.
- **Don't advertise.** No logos or branding elements unless they're a fixed part of your app's first screen.

## Platform Considerations

### iOS, iPadOS

- **Launch in the appropriate orientation.** If supporting both portrait and landscape, use the device's current orientation. If single-orientation only, launch in that orientation and let people rotate.
- Landscape-only interfaces must respond correctly regardless of left or right rotation.

### tvOS

- Launch screens are static (not layered images).
- **In live-viewing apps, consider auto-starting playback** of new or recently viewed live content after a few seconds of inactivity.

### visionOS

- **Consider launching in the Shared Space even if your app is fully immersive.** This provides context while loading, lets you present a control to open the immersive experience, and lets people choose when to transition to a Full Space (especially if other apps are running).