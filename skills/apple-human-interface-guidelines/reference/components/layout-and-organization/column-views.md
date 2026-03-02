# Column Views

A column view (also called a browser) lets people view and navigate a data hierarchy using a series of vertical columns. Each column represents one level of the hierarchy. Parent items with children are marked with a triangle icon; selecting one shows its children in the next column.

**Platform support:** macOS only (not supported in iOS, iPadOS, tvOS, visionOS, or watchOS). For hierarchical content on iPadOS or visionOS, use a split view instead.

**Implementation:** `NSBrowser` (AppKit)

## Best Practices

- **Use column views for deep hierarchies** where people navigate back and forth frequently between levels, and sorting capabilities (provided by lists/tables) aren't needed. Example: Finder's column view for directory structures.
- **Show the root level in the first column.** People can scroll back to the first column to restart navigation from the top.
- **Show info about the selected item when there are no nested children.** For example, Finder shows a preview plus creation date, modification date, file type, and size.
- **Let people resize columns.** Especially important when data item names may be too long for the default column width.

## Related Components

- Lists and tables — for sortable data
- Outline views — for hierarchical data in a single column
- Split views — for hierarchical navigation on iPadOS/visionOS