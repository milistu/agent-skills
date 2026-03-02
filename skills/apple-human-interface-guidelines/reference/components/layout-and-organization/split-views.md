# Split Views

Guidelines for managing multiple adjacent panes of content, typically used to show multiple levels of app hierarchy and support navigation between them.

## Best Practices

- **Persistently highlight the current selection** in each pane that leads to the detail view to clarify relationships between panes and help people stay oriented.
- **Consider letting people drag and drop content between panes** to conveniently move content from one part of the app to another.

## Platform-Specific Guidelines

### iOS

- **Prefer split views in regular — not compact — environments.** In compact environments (e.g., iPhone portrait), multiple panes cause wrapping/truncation, reducing legibility and usability.

### iPadOS

- Supports two or three vertical panes.
- **Account for narrow, compact, and intermediate window widths.** iPad windows are fluidly resizable — ensure logical navigation between panes at all widths.
- Developer APIs: `NavigationSplitView` (SwiftUI), `UISplitViewController` (UIKit).

### macOS

- Panes can be arranged **vertically, horizontally, or both**.
- Dividers between panes can support dragging to resize.
- **Set reasonable defaults for minimum and maximum pane sizes.** Keep dividers visible — panes that are too small make dividers seem to disappear.
- **Consider letting people hide panes** when it makes sense (e.g., reducing distractions during editing).
- **Provide multiple ways to reveal hidden panes** — toolbar button, menu command, keyboard shortcut.
- **Prefer the thin divider style** (1 point width) for maximum content space. Use thicker dividers only when thin ones are hard to distinguish (e.g., adjacent table rows with strong linear elements).
- Developer APIs: `VSplitView`, `HSplitView` (SwiftUI), `NSSplitView.DividerStyle` (AppKit).

### tvOS

- Split views work well for filtering content — category in primary pane, results in secondary pane.
- **Keep panes looking balanced.** Default: 1/3 primary, 2/3 secondary. Half-and-half is also an option.
- **Display a single title above the split view** — don't title individual panes separately.
- **Align the title based on secondary pane content:** center when it contains a collection; place above the primary view when it contains a single main content view.

### visionOS

- **Prefer a split view over a new window** for supplementary information. Avoids context-switching and the complexity of managing multiple windows. Use a sheet for small amounts of information or simple tasks.

### watchOS

- Split view displays either list or detail as a full-screen view.
- **Automatically display the most relevant detail view** on launch (based on location, time, or recent actions).
- **Place multiple detail pages in a vertical tab view** so people can scroll between tabs with the Digital Crown. watchOS displays a page indicator next to the Digital Crown.

## Related Components

- Sidebars
- Tab bars
- Layout

## Developer APIs

| Framework | API |
|-----------|-----|
| SwiftUI | `NavigationSplitView`, `VSplitView`, `HSplitView` |
| UIKit | `UISplitViewController` |
| AppKit | `NSSplitViewController`, `NSSplitView.DividerStyle` |