# Outline Views

Guidelines for designing outline views that present hierarchical data in a scrolling list organized into columns and rows. **macOS only** — not supported on iOS, iPadOS, tvOS, visionOS, or watchOS.

An outline view includes at least one column with primary hierarchical data (parent containers and children). Additional columns display supplementary attributes (e.g., sizes, dates). Parent containers use disclosure triangles to expand/collapse children.

Outline views often appear in the leading side of a split view, with related content on the opposite side.

## Best Practices

- **Use a table instead if data is not hierarchical.** See Lists and Tables.
- **Expose data hierarchy in the first column only.** Other columns display attributes of the primary hierarchical data.
- **Use descriptive column headings** — nouns or short noun phrases with title-style capitalization, no punctuation (no trailing colon). Always provide headings in multi-column views. For single-column, use a label or other context if omitting headings.
- **Consider clickable column headings for sorting.** Clicking the primary column heading sorts at each hierarchy level. Clicking an already-sorted column reverses sort direction. Implement secondary sorting behind the scenes if needed.
- **Let people resize columns** to reveal data wider than the column.
- **Support expand/collapse shortcuts.** E.g., clicking a disclosure triangle expands one folder; Option-clicking expands all subfolders.
- **Retain expansion state.** Store which levels are expanded so users don't need to navigate back to the same place.
- **Consider alternating row colors** in multi-column views to help track values across columns.
- **Support inline editing when appropriate.** Single-click to edit cell contents; double-click can perform a different action (e.g., opening a file). Allow reordering, adding, and removing rows if useful.
- **Use centered ellipsis for truncation** instead of clipping — preserves beginning and end of text for recognizability.
- **Consider a search field** in the toolbar for lengthy outline views.

## Related Components

- Column Views
- Lists and Tables
- Split Views

## Developer References

- `OutlineGroup` (SwiftUI)
- `NSOutlineView` (AppKit)