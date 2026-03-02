# Collaboration and Sharing

Guidelines for designing collaboration and sharing experiences across Apple platforms using system interfaces, Messages integration, and sharing sheets.

## Best Practices

- **Place the Share button in a convenient location (like a toolbar)** to make it easy to start sharing or collaborating. In iOS 16+, the share sheet includes file-sharing methods and permission settings. Use `ShareLink` in SwiftUI to present the system share sheet.

- **Customize the share sheet to offer supported file sharing types if needed.** CloudKit: pass both the file and collaboration object to get "send copy" support. iCloud Drive: "send copy" is supported by default. Custom collaboration: include a file or plain text representation in your collaboration object.

- **Write succinct permission summary phrases.** Examples: "Only invited people can edit" or "Everyone can make changes." The system displays these in a button that reveals sharing options.

- **Provide simple sharing options that streamline collaboration setup.** Customize the permission view to let people specify who can access content, edit vs. read-only access, and whether collaborators can add participants. Keep choices minimal and grouped logically.

- **Prominently display the Collaboration button when collaboration starts.** Place it next to the Share button since people typically interact with the share sheet first. The button reminds people content is shared and shows who's sharing.

- **Provide custom actions in the collaboration popover only if essential.** The popover has three sections:
  1. **Top:** Collaborator list with Messages/FaceTime communication buttons
  2. **Middle:** Your custom items (keep minimal)
  3. **Bottom:** Manage shared file button

- **Customize the management button title if needed.** Default title is "Manage Shared File." CloudKit provides a management view automatically; otherwise create your own.

- **Consider posting collaboration event notifications in Messages.** Use `SWHighlightEvent` for content changes, membership changes, or participant mentions. Include universal links to open relevant views.

## Platform Considerations

| Platform | Notes |
|----------|-------|
| iOS, iPadOS, macOS | No additional considerations |
| tvOS | Not available |
| visionOS | System supports screen sharing in Shared Space by streaming windows. Transitioning to Full Space pauses the stream until returning to Shared Space. |
| watchOS | Use `ShareLink` in SwiftUI to present the system share sheet |

## Related

- [Activity views](/design/human-interface-guidelines/activity-views) — the component used for sharing
- [SharePlay](/design/human-interface-guidelines/shareplay) — for immersive sharing experiences in visionOS
- `SharedWithYou` framework, `ShareLink` (SwiftUI)