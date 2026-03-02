# Privacy

Guidelines for handling privacy, requesting permissions, and protecting user data in Apple platform apps.

## Best Practices

- **Request access only to data you actually need.** Make permission requests as specific as possible.
- **Be transparent about data collection and usage.** Respect system features like Hide My Email and Mail Privacy Protection.
- **Process data on-device where possible.** Use Apple Neural Engine and custom CreateML models to avoid round trips to remote servers.
- **Adopt system-defined privacy protections.** E.g., in iOS 15+, use CloudKit encryption for strings, numbers, and dates.

## Requesting Permission

Things requiring permission:
- Personal data (location, health, financial, contact, personally identifying info)
- User-generated content (emails, messages, calendar, contacts, gameplay, Apple Music activity, HomeKit data, audio/video/photo)
- Protected resources (Bluetooth, home automation, Wi-Fi, local networks)
- Device capabilities (camera, microphone)
- In visionOS Full Space: ARKit data (hand tracking, plane estimation, image anchoring, world tracking)
- Device advertising identifier (app tracking)

### Key Guidelines

- **Request permission only when your app clearly needs access.** Wait until people use a feature requiring access.
- **Avoid requesting permission at launch** unless required for core functionality. Navigation apps needing location at launch are acceptable.
- **Write clear purpose strings** (usage description strings):
  - Use brief, complete sentences in sentence case with active voice
  - Be straightforward, specific, and easy to understand
  - End with a period

| | Example purpose string | Notes |
|---|---|---|
| ✅ | The app records during the night to detect snoring sounds. | Active sentence, clearly describes how and why data is collected. |
| ❌ | Microphone access is needed for a better experience. | Passive, vague justification. |
| ❌ | Turn on microphone access. | Imperative, no justification. |

### Pre-alert Screens

Custom screens displayed before system permission alerts:

- **Include only one button** that opens the system alert. Use titles like "Continue" or "Next" — never "Allow".
- **Don't include additional actions** like close, cancel, or dismiss options.

### Tracking Requests

System-provided tracking alert must appear before collecting any tracking data. **Prohibited pre-alert designs** (will cause App Store rejection):

- ❌ Offering incentives for granting permission
- ❌ Displaying a screen that mirrors/imitates the system alert
- ❌ Showing an image of the standard alert (modified or not)
- ❌ Adding visual cues drawing attention to the alert's Allow button
- ❌ Withholding functionality until people allow tracking

See [App Review Guidelines: 5.1.1 (iv)](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage).

## Location Button

Available in iOS, iPadOS, and watchOS via Core Location. Grants temporary one-time location authorization.

- First tap shows a standard alert; subsequent taps grant one-time access without re-prompting.
- If app has no authorization status, tapping equals "Allow Once."
- If user previously chose "While Using the App," tapping doesn't change status.

### Customization Options

- System-provided title (e.g., "Current Location" or "Share My Current Location")
- Filled or outlined location glyph
- Background color and title/glyph color
- Corner radius

**Cannot customize:** other visual attributes. System warns about low-contrast or excess translucency. Text must fit without truncation at all accessibility sizes and translations. If system identifies consistent problems, the button won't grant location access.

## Protecting Data

- **Use passkeys** instead of passwords where possible. If passwords are needed, require two-factor authentication.
- **Use biometric identification** (Face ID, Optic ID, Touch ID) for apps people keep logged in.
- **Store sensitive information in a keychain** — never in plain-text files.
- **Avoid custom authentication schemes.** Prefer passkeys, Sign in with Apple, or Password AutoFill.

## Platform Considerations

### macOS
- Sign apps with a valid Developer ID for distribution outside the store.
- Use app sandboxing (required for Mac App Store).
- Don't assume who is signed in (fast user switching means multiple active users).

### visionOS
- ARKit algorithms run automatically in Shared Space but don't send data to apps.
- ARKit API access requires opening a Full Space; features like Plane Estimation, Scene Reconstruction, Image Anchoring, and Hand Tracking require explicit permission.
- User input (eye tracking) is private by design — system handles hover effects without exposing gaze direction.
- Back camera provides blank input; front camera only provides input for spatial Personas with permission.
- If bringing an iOS/iPadOS app to visionOS with camera features, remove them or replace with content import options.