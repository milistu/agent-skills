# Tab Bars

Guidelines for designing tab bars that let people navigate between top-level sections of an app.

## Best Practices

- **Use for navigation, not actions.** Tab bars are for switching between app sections. Use a toolbar for controls that act on the current view.
- **Keep the tab bar visible** when navigating between sections. Only hide it when a modal view covers it temporarily.
- **Use the appropriate number of tabs.** Fewer tabs are easier to navigate. For complex apps, consider a sidebar or a tab bar that adapts to a sidebar.
- **Avoid overflow tabs.** When horizontal space is limited, trailing tabs collapse into a "More" tab (iOS/iPadOS), making hidden content harder to discover.
- **Never disable or hide tab bar buttons.** If a section is empty, explain why content is unavailable instead.
- **Include tab labels** beneath or beside icons. Use single words whenever possible.
- **Use SF Symbols** (filled variants preferred) for scalable, platform-consistent icons. Icons appear above labels in compact views and side-by-side in regular views.
- **Use badges sparingly** — red oval with white text (number or exclamation point) — only for critical new/updated information.
- **Avoid similar colors** for tab labels and content layer backgrounds. Prefer monochromatic tab bars or choose an accent color with sufficient differentiation against colorful content.

## Platform-Specific Guidelines

### iOS

- Tab bar floats at the bottom on a Liquid Glass background.
- For tab bars with an attached accessory (e.g., MiniPlayer in Music), you can minimize the tab bar when scrolling down. User exits minimized state by tapping a tab or scrolling to top.
  - SwiftUI: `TabBarMinimizeBehavior`
  - UIKit: `UITabBarController.MinimizeBehavior`
- A tab bar can include a distinct search item at the trailing end.

### iPadOS

- Tab bar appears near the top of the screen.
- Can be fixed or convertible to a sidebar via a button.
  - SwiftUI: `tabBarOnly` / `sidebarAdaptable` (`TabViewStyle`)
- To present a sidebar without tab bar conversion, use `NavigationSplitView` instead of a tab view.
- **Prefer a tab bar for navigation.** Offer sidebar conversion for more complex apps needing wider navigation options.
- **Let people customize the tab bar** — select frequently used items, remove less-used ones. Default to 5 or fewer tabs for compact/regular continuity.
  - SwiftUI: `TabViewCustomization`
  - UIKit: `UITab.Placement`

### tvOS

- Highly customizable: tint/color/image for background, custom fonts, tints for selected/unselected items, button icons.
- Default: translucent bar, selected tab is opaque with drop shadow on focus.
- Height: 68 pt, top edge 46 pt from screen top (fixed).
- Overflow items get a fade effect; scrolling applies fade on both sides.
- **Scrolling behavior:** Tab bar scrolls offscreen by default with single main views. Stays pinned with split views. Menu button always returns focus to tab bar.
- **Live-viewing app tab order:** Live content → Cloud DVR/recorded → Other content.

### visionOS

- Tab bar is always vertical, fixed to the window's leading side.
- Automatically expands when the user looks at it; tap to open a tab.
- Expanded tab bar can temporarily obscure content behind it.
- **Supply both a symbol and text label** for each tab. Keep labels short for at-a-glance reading.
- **Consider a sidebar within a tab** for deep hierarchies. Prevent sidebar selections from changing the current tab.

### macOS

No additional considerations.

### watchOS

Not supported.

## Developer References

| Framework | API |
|-----------|-----|
| SwiftUI | `TabView`, `TabViewBottomAccessoryPlacement`, `TabViewCustomization`, `TabBarMinimizeBehavior` |
| UIKit | `UITabBar`, `UITabBarController.MinimizeBehavior`, `UITab.Placement` |