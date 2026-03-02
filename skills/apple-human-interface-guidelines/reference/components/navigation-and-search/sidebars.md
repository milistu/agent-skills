# Sidebars

A sidebar appears on the leading side of a view for navigating between sections. It floats above content in the Liquid Glass layer without being anchored to view edges.

## Best Practices

- **Extend content beneath the sidebar.** In iOS, iPadOS, and macOS, sidebars float above content in the Liquid Glass layer. Extend content beneath it by letting it horizontally scroll or applying a background extension view (`backgroundExtensionEffect()`) which mirrors adjacent content to give the impression of stretching it under the sidebar.
- **Let people customize sidebar contents** — allow choosing which areas appear and their order.
- **Group hierarchy with disclosure controls** if your app has a lot of content to keep vertical space manageable.
- **Use familiar SF Symbols** to represent items. Prefer custom symbols over bitmap images.
- **Let people hide the sidebar** using platform-standard interactions (iPadOS: edge swipe; macOS: show/hide button or View menu command). In visionOS, windows typically expand to accommodate the sidebar. **Avoid hiding the sidebar by default** to keep it discoverable.
- **Show no more than two levels of hierarchy.** For deeper hierarchies, use a split view with a content list between sidebar items and detail view.
- **Use succinct, descriptive labels** to title each group when showing two levels. Omit unnecessary words.

## Platform Considerations

### iOS
- **Avoid using a sidebar.** It takes up too much space in landscape and isn't available in portrait. Use a [tab bar](/design/human-interface-guidelines/tab-bars) instead.

### iPadOS
- Use `sidebarAdaptable` style of tab view to present a sidebar that can switch to a tab bar via a button. It responds automatically to rotation and window resizing.
- **Consider using a tab bar first.** Tab bars provide more space for content. The convertible sidebar-style appearance can provide access to less-frequently-used content.
- For non-SwiftUI: use `NavigationSplitView`, `UISplitViewController`, or `UICollectionLayoutListConfiguration.Appearance.sidebar`.

### macOS
- Sidebar row height, text, and glyph size depend on overall size (small, medium, large). Set programmatically or users change it via General settings.
- **Don't use a fixed color for all sidebar icons.** Icons use the current accent color by default; respect the user's choice.
- **Consider auto-hiding/revealing sidebar** when container window resizes (e.g., Mail collapses sidebar when viewer shrinks).
- **Avoid putting critical info/actions at the bottom** — windows often get repositioned hiding the bottom edge.

### visionOS
- **For deep hierarchies, use a sidebar within a tab** in a tab bar for secondary navigation. Ensure sidebar selections don't change the current tab.

## Key Developer APIs

| Framework | API |
|-----------|-----|
| SwiftUI | `sidebarAdaptable`, `NavigationSplitView`, `ListStyle.sidebar`, `backgroundExtensionEffect()` |
| UIKit | `UISplitViewController`, `UICollectionLayoutListConfiguration.Appearance.sidebar` |
| AppKit | `NSSplitViewController` |