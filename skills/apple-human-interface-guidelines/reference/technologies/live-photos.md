# Live Photos Design Guidelines

Guidelines for integrating Live Photos — interactive photos with sound and motion captured before and after the shutter press.

## Best Practices

- **Apply adjustments to all frames.** If your app lets people apply effects or adjustments to a Live Photo, apply changes to the entire photo. If you don't support this, offer the option to convert to a still photo.
- **Keep Live Photo content intact.** Don't disassemble a Live Photo to present its frames or audio separately. Maintain consistent visual treatment and interaction model across all apps.
- **Photo sharing:** Let people preview the entire contents of Live Photos before sharing. Always offer the option to share as a traditional still photo.
- **Show download progress.** Display a progress indicator during download and indicate when the photo is playable.
- **Fallback gracefully.** In environments that don't support Live Photos, display as a traditional still photo. Don't attempt to replicate the Live Photos experience.
- **Distinguish from still photos.** Use a hint of movement as the primary indicator. There are no built-in motion effects, so you need to design and implement custom motion effects.
- **When movement isn't possible**, show a system-provided badge (with or without "Live" text) above the photo. Never include a playback button that could be mistaken for video playback.
- **Keep badge placement consistent.** Place the badge in the same location on every photo, typically in a corner.

## Platform Considerations

- **iOS, iPadOS, macOS, tvOS:** No additional considerations.
- **watchOS:** Not supported.
- **visionOS:** People can view but not capture Live Photos.