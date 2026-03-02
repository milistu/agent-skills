# Tab Views

A tab view presents multiple mutually exclusive panes of content in the same area, switched via a tabbed control. Primarily a **macOS** component; not supported in iOS, iPadOS, tvOS, or visionOS.

## Best Practices

- **Use for closely related areas of content.** The visual enclosure of tabs signals similarity between panes.
- **Keep panes self-contained.** Controls within a pane should affect content only in that pane — panes are mutually exclusive.
- **Label each tab** with nouns or short noun phrases describing pane contents. Use title-style capitalization.
- **Avoid pop-up buttons to switch tabs.** Tabs require one click; pop-ups require two. Pop-ups also hide choices until clicked. Exception: when there are too many panes for tabs.
- **Avoid more than six tabs.** More than six is overwhelming and causes layout issues. Consider using a pop-up button menu for view options instead.

## Anatomy

- The tabbed control appears on the **top edge** of the content area.
- You can hide the control for programmatic pane switching.
- When the control is hidden, the content area can be borderless, bezeled, or line-bordered. Borderless views can be solid or transparent.
- **Inset the tab view** with a margin of window-body area on all sides. This leaves room for additional controls unrelated to tab content. Extending to window edges is possible but unusual.

## Platform Considerations

| Platform | Guidance |
|---|---|
| **macOS** | Primary platform — use `NSTabView` (AppKit) or `TabView` (SwiftUI) |
| **iOS/iPadOS** | Not supported — use a [segmented control](https://developer.apple.com/design/human-interface-guidelines/segmented-controls) instead |
| **watchOS** | Displayed as page controls. Use `TabView` with `.verticalPage` style (SwiftUI) |
| **tvOS/visionOS** | Not supported |