# Page Controls

A page control displays a row of indicator dots representing pages in a flat list. A solid dot denotes the current page. Not supported in macOS.

## Best Practices

- **Use for ordered, sequential page lists only.** For hierarchical or nonsequential navigation, use a sidebar or split view.
- **Center horizontally at the bottom** of the view or window.
- **Limit to ~10 pages.** More than 10 dots are hard to count at a glance. For more pages, consider a grid layout that allows non-linear navigation.

## Customizing Indicators

By default, all indicators use the system dot image. You can set a custom default image (`preferredIndicatorImage`) or a unique image for a specific page (`setIndicatorImage(_:forPage:)`).

- **Keep custom indicator images simple and clear.** Avoid complex shapes, negative space, text, or inner lines. Use simple SF Symbols or similarly simple icons.
- **Customize the default indicator only when it enhances meaning** (e.g., `bookmark.fill` if every page contains bookmarks).
- **Use no more than two different indicator images.** One default + one special-purpose (e.g., Weather uses `location.fill` for current location). Multiple unique images look messy and force memorization.
- **Avoid coloring indicator images.** Let the system automatically color indicators to maintain proper contrast between current and other pages.

## Platform-Specific Guidance

### iOS / iPadOS

- Indicators shrink at edges when too many to fit, suggesting more pages are available.
- **Interaction:** Tapping leading/trailing side of current indicator reveals next/previous page. Scrubbing (drag left/right) opens pages in sequence. iPadOS also supports pointer targeting of specific indicators.
- **Don't animate page transitions during scrubbing** — only use animated scrolling for taps. Animating during scrubbing causes lag and visual flashes.
- **Background styles:**
  - **Automatic** — Background appears only during interaction. Use when page control isn't the primary nav element.
  - **Prominent** — Background always visible. Use only when page control is the primary nav control.
  - **Minimal** — No background. Shows position only, no visual feedback during scrubbing.
- **Don't support scrubbing with minimal background style** — it provides no visual feedback during scrubbing.

### tvOS

- Use on collections of **full-screen pages** only. Designed for full-screen environments where content-rich pages are peers. Additional controls make it difficult to maintain focus while moving between pages.

### visionOS

- Page controls indicate current page but are **not interactive** — people don't directly interact with them.

### watchOS

- Displayed at **bottom of screen** for horizontal pagination, or **next to Digital Crown** for vertical tab views.
- Vertical page control shows position within current page and within the set of pages, transitioning between scrolling content and scrolling to other pages.
- **Use vertical pagination** to separate views into distinct, purposeful pages navigated via Digital Crown. Preferred over horizontal pagination or deep hierarchy.
- **Limit individual page content to a single screen height** when possible. Use variable-height pages judiciously, placing them after fixed-height pages.

## Related

- [Scroll views](/design/human-interface-guidelines/scroll-views)
- SwiftUI: `PageTabViewStyle`
- UIKit: `UIPageControl`