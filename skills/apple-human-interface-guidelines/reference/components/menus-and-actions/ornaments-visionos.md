# Ornaments (visionOS)

An ornament presents controls and information related to a window without crowding or obscuring the window's contents. It floats in a plane parallel to its associated window, slightly in front along the z-axis. Ornaments move with their window and remain unaffected by content scrolling.

Ornaments can appear on any edge of a window and contain UI components like buttons, segmented controls, and other views. The system uses ornaments for toolbars, tab bars, and video playback controls; you can also create custom ornaments.

**Platform:** visionOS only.

## Best Practices

- **Use ornaments for frequently needed controls or information** in a consistent, non-cluttering location. Example: Music uses an ornament for Now Playing controls.
- **Keep ornaments visible** in most cases. Hiding may be appropriate during immersive content (video, photo viewing), but otherwise maintain consistent access.
- **When displaying multiple ornaments, prioritize visual balance.** Constrain the total number to avoid increasing visual weight and complexity. Relocate elements into the main window if removing an ornament.
- **Keep ornament width ≤ window width.** A wider ornament can interfere with tab bars or vertical content on the window's side.
- **Use borderless buttons in ornaments.** The ornament background is glass material by default, so buttons placed directly on it may not need visible borders. The system applies hover effect automatically when people look at a borderless button.
- **Use system-provided toolbars and tab bars** instead of custom ornaments when possible. In visionOS, toolbars and tab bars automatically appear as ornaments.

## Developer Reference

- SwiftUI: `ornament(visibility:attachmentAnchor:contentAlignment:ornament:)`
- Toolbars: SwiftUI `Toolbars` / `TabView`