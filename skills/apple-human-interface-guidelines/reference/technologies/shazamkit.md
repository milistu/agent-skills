# ShazamKit Design Guidelines

ShazamKit enables audio recognition by matching audio samples against the Shazam catalog or custom audio catalogs. Use cases include syncing graphics with playing music, providing captions/sign language for accessibility, and synchronizing in-app experiences with virtual content.

If your app uses the device microphone for audio recognition, you must request microphone access. Provide a clear explanation of why access is needed (see Privacy guidelines).

## Best Practices

- **Stop recording as soon as possible.** When people allow audio recording for recognition, they don't expect the microphone to stay on. Only record for as long as it takes to get the needed sample.
- **Let people opt in to storing recognized songs to iCloud.** If your app can store recognized songs to iCloud, give people a way to approve this action first. Both the Music Recognition control and Shazam app show your app as the source, but people should have control over which apps store content in their library.

## Platform Considerations

No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.