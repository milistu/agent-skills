# Disclosure Controls

Disclosure controls reveal and hide information and functionality related to specific controls or views.

## Best Practices

- **Hide details until they're relevant.** Place the most commonly used controls at the top of the disclosure hierarchy (always visible), with more advanced functionality hidden by default.

## Disclosure Triangles

Shows and hides information/functionality associated with a view or list of items (e.g., Finder folder hierarchy in list view, Keynote advanced export options).

- Points **inward from the leading edge** when content is hidden
- Points **down** when content is visible
- Clicking/tapping toggles between states; view expands/collapses accordingly

**Guidelines:**
- Provide a descriptive label indicating what is disclosed or hidden (e.g., "Advanced Options")

**Developer:** `NSButton.BezelStyle.disclosure` (AppKit)

## Disclosure Buttons

Shows and hides functionality associated with a specific control (e.g., macOS Save dialog expanding to show advanced navigation options).

- Points **down** when content is hidden
- Points **up** when content is visible
- Clicking/tapping toggles between states; view expands/collapses accordingly

**Guidelines:**
- Place near the content it shows and hides — establish a clear visual relationship
- **Use no more than one disclosure button in a single view** — multiple buttons add complexity and confusion

**Developer:** `NSButton.BezelStyle.pushDisclosure` (AppKit)

## Platform Considerations

| Platform | Support |
|---|---|
| macOS | Fully supported (no additional considerations) |
| iOS, iPadOS, visionOS | Available via SwiftUI `DisclosureGroup` |
| tvOS, watchOS | Not supported |

## Related Components

- Outline views
- Lists and tables
- Buttons