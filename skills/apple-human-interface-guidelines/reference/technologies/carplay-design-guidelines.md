# CarPlay Design Guidelines

Design guidelines for CarPlay apps displayed on a car's built-in display. CarPlay apps use system-defined templates (audio, communication, navigation, fueling) — iOS renders the UI, so no layout adjustments are needed for different screen resolutions or input hardware.

## iPhone Interactions

- **Eliminate app interactions on iPhone when CarPlay is active.** All interactions must occur via the car's built-in controls and display. Complete any setup on iPhone before the vehicle is in motion.
- **Never lock people out of CarPlay because the connected iPhone requires input.** The app must function when iPhone is inaccessible (e.g., in a bag or trunk). Let users resolve iPhone issues after the vehicle stops.
- **Ensure your app works without requiring people to unlock iPhone.** Most people use CarPlay with iPhone locked.

## Audio

- **Let people choose when to start playback.** Avoid automatic playback unless the app plays a single source or is resuming previously interrupted audio. Don't start an audio session until ready to play — starting a session silences other audio sources like the car radio.
- **Start playback as soon as audio has sufficiently loaded.** The system shows the selection highlighted with a spinning activity indicator until the app signals readiness.
- **Display the Now Playing screen when audio is ready.** Don't delay playback for descriptive metadata — load it in the background.
- **Resume audio after interruption only when appropriate.** Resume after temporary interruptions (e.g., phone calls) if audio was playing. Don't resume after permanent interruptions (e.g., Siri-initiated playlist).
- **Adjust relative audio levels but don't change overall volume.** Users must control the final output volume.

## Layout

CarPlay supports a wide range of display resolutions. The system automatically scales app icons and interfaces.

### Common Screen Sizes

| Dimensions (pixels) | Aspect ratio |
| --- | --- |
| 800×480 | 5:3 |
| 960×540 | 16:9 |
| 1280×720 | 16:9 |
| 1920×720 | 8:3 |

- Provide useful, high-value information in a **clean layout easy to scan from the driver's seat**.
- Maintain **consistent appearance** throughout the app — similar functions should look similar.
- **Primary content should stand out and feel actionable.** Large items appear more important and are easier to tap. Place the most important content/controls in the **upper half** of the screen.

## Color

- **Use a limited color palette** that coordinates with your app logo.
- **Don't use the same color for interactive and noninteractive elements.**
- **Test color under varied lighting conditions in an actual car** — daylight, nighttime, tinted windows, direct sunlight.
- **Support both light and dark appearances.** CarPlay may auto-adjust based on lighting.
- **Choose colors accessible to everyone.** See [Inclusive color](https://developer.apple.com/design/human-interface-guidelines/color#Inclusive-color).

## Icons and Images

CarPlay supports landscape and portrait displays at @2x and @3x scale factors.

- **Supply @2x and @3x images for all CarPlay artwork.**
- **Mirror your iPhone app icon** — use the same design for CarPlay.
- **Don't use black for icon background.** Lighten it or add a border to prevent blending with the display background.

### CarPlay App Icon Sizes

| @2x (pixels) | @3x (pixels) |
| --- | --- |
| 120×120 | 180×180 |

## Error Handling

- **Report errors in CarPlay, not on the connected iPhone.** Never direct people to pick up their iPhone to read or resolve an error.
- Handle errors gracefully; report only when absolutely necessary.

## Platform Support

iOS only. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS.