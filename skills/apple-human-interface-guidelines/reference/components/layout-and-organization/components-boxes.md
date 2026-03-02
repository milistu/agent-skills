# Boxes

A box creates a visually distinct group of logically related information and components using a visible border or background color. Can include a title. Implemented as `GroupBox` (SwiftUI) or `NSBox` (AppKit).

## Best Practices

- **Keep boxes relatively small** compared to their containing view. As a box approaches the size of the containing window/screen, it loses its effectiveness at communicating grouping and can crowd other content.
- **Use padding and alignment for sub-grouping** rather than nesting boxes. Nested boxes make the interface feel busy and constrained.

## Content & Titles

- Provide a succinct introductory title only if it helps clarify the box's contents.
- Titles help VoiceOver users predict content within the box.
- Write a brief phrase describing the contents using **sentence-style capitalization**.
- **No ending punctuation** unless used in a settings pane, where you append a colon to the title.

## Platform Considerations

| Platform | Notes |
|----------|-------|
| iOS, iPadOS | Uses secondary and tertiary background colors by default |
| macOS | Displays the box's title above it by default |
| visionOS | No additional considerations |
| tvOS, watchOS | Not supported |