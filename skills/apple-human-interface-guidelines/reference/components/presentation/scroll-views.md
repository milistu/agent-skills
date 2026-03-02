# Scroll Views

Guidelines for designing scroll views across Apple platforms. A scroll view lets people view content larger than the view's boundaries by moving content vertically or horizontally.

## Best Practices

- **Support default scrolling gestures and keyboard shortcuts.** People expect systemwide scrolling behavior everywhere. Custom scroll indicators should use elastic behavior.
- **Make it apparent when content is scrollable.** Display partial content at the view's edge to hint that more content exists in that direction.
- **Avoid nesting scroll views with the same orientation.** Creates unpredictable, hard-to-control interfaces. Horizontal inside vertical (or vice versa) is fine.
- **Consider page-by-page scrolling** for appropriate content. Define page size (typically view height/width) and a unit of overlap (line of text, row of glyphs, part of a picture) subtracted from page size to maintain context. See `PagingScrollTargetBehavior`.
- **Use automatic scrolling sparingly** to help people find their place:
  - When an operation selects content or moves insertion point to a hidden area
  - When people start entering info in a non-visible location
  - When the pointer moves past the view edge during selection
  - When people select something, scroll away, then act on the selection
  - Only scroll as much as necessary to retain context.
- **Set appropriate zoom min/max scale values** — e.g., don't allow zooming until one character fills the screen.

## Scroll Edge Effects

In iOS, iPadOS, and macOS, a scroll edge effect is a variable blur providing transition between content and Liquid Glass controls (e.g., toolbars). The system usually applies it automatically when a pinned element overlaps scrolling content. For custom controls/layouts, add manually via `ScrollEdgeEffectStyle` (SwiftUI) or `UIScrollEdgeEffect` (UIKit).

### Two Styles

| Style | Use Case |
|-------|----------|
| **Soft** (`.soft`) | Default for most cases, especially iOS/iPadOS. Subtle transition for toolbars and interactive elements like buttons. |
| **Hard** (`.hard`) | Primarily macOS. Stronger, more opaque boundary for interactive text, backless controls, or pinned table headers needing extra clarity. |

### Edge Effect Rules

- **Only use when a scroll view is adjacent to floating interface elements** — not decorative.
- **Apply one scroll edge effect per view.** In split view layouts (iPad/Mac), each pane can have its own; keep heights consistent for alignment.

## Platform Considerations

### iOS, iPadOS

- Show a **page control** when scroll view is in page-by-page mode. Don't show scroll indicator on the same axis as the page control to avoid redundancy.

### macOS

- Scroll indicator is called a **scroll bar**.
- Use **small or mini scroll bars** in panels when space is tight. Keep consistent sizing for all controls in the panel.

### tvOS

- Views scroll but aren't treated as distinct objects with scroll indicators. The system automatically scrolls to keep focused items visible.

### visionOS

- Scroll indicator is small and fixed-size; always appears in a predictable location:
  - **Vertical scrolling:** vertically centered at trailing edge
  - **Horizontal scrolling:** horizontally centered at bottom edge
- Looking at the scroll indicator and dragging enables a **jog bar** experience — controls scrolling speed rather than position, with tick marks providing visual feedback.
- **Account for indicator size** — it's slightly thicker than iOS. Increase margins if using tight spacing to prevent overlap.

### watchOS

- **Prefer vertically scrolling content** — Digital Crown scrolls vertically.
- **Use tab views for page-by-page scrolling** — displayed as pages; vertical stack allows Digital Crown navigation through full-screen pages with page indicator.
- **Consider limiting individual page content to single screen height** for glanceability. Variable-height pages are supported (page indicator expands to scroll indicator) but should be placed after fixed-height pages.