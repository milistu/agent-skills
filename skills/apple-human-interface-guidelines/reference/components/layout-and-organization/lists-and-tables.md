# Lists and Tables

Guidelines for designing lists and tables that present data in rows and columns across Apple platforms.

## Best Practices

- **Prefer text in lists/tables.** The row-based format is well suited for scannable text. For items varying widely in size or large image collections, use a [collection](https://developer.apple.com/design/human-interface-guidelines/collections) instead.
- **Let people edit tables when it makes sense.** Support reordering even if add/remove isn't available. In iOS/iPadOS, users must enter edit mode before selecting table items.
- **Provide appropriate feedback on selection:**
  - Navigation hierarchy: persistently highlight the selected row to clarify the path.
  - Options list: briefly highlight, then show an indicator (e.g., checkmark) for the selected state.

## Content

- **Keep item text succinct** to minimize truncation and wrapping. Consider showing only titles and revealing full content in a detail view.
- **Preserve readability of clipped text.** Mid-text ellipsis can help distinguish items by preserving both beginning and end.
- **Use descriptive column headings** with nouns or short noun phrases in title-style capitalization, no ending punctuation. For single-column tables without headings, use a label or header for context.

## Style

- **Choose a style that fits your data and platform:**
  - iOS/iPadOS grouped style: uses headers, footers, and spacing to separate groups.
  - watchOS elliptical style: items appear to roll off a rounded surface while scrolling.
  - macOS bordered style: alternating row backgrounds for large tables.
  - See [`ListStyle`](https://developer.apple.com/documentation/SwiftUI/ListStyle).
- **Choose appropriate row styles.** Use built-in row configurations (e.g., [`UIListContentConfiguration`](https://developer.apple.com/documentation/UIKit/UIListContentConfiguration-swift.struct)) to lay out content in rows, headers, and footers.

## Platform-Specific Guidelines

### iOS, iPadOS, visionOS

- **Info button (detail disclosure button):** Only use to reveal more information about a row's content — it does **not** support navigation.
- **Disclosure indicator (chevron):** Use to drill into subviews in a hierarchical list. See [`UITableViewCell.AccessoryType.disclosureIndicator`](https://developer.apple.com/documentation/UIKit/UITableViewCell/AccessoryType-swift.enum/disclosureIndicator).
- **Avoid combining an index with trailing controls** (like disclosure indicators). Both appear on the trailing side, making interaction difficult.

### macOS

- **Column heading sort:** Let people click column headings to sort; clicking an already-sorted column reverses the order.
- **Resizable columns:** Let people resize columns to reveal clipped data.
- **Alternating row colors:** Consider for multicolumn tables to help track values across columns.
- **Use outline views for hierarchical data** — they include disclosure triangles for nested levels.

### tvOS

- **Account for focus effects.** Rows slightly increase in size and corners become rounded when focused. Ensure nearby images still look good and don't add custom corner masks.

### watchOS

- **Limit row count when possible.** Short lists are easier to scan, but show all items if users expect them (e.g., podcast subscriptions). List most relevant items first with an option to view more.
- **Constrain detail view length for vertical page-based navigation.** This lets people swipe vertically among detail items without returning to the list. Scrollable detail views prevent this navigation pattern.

## Key APIs

| Framework | API |
|-----------|-----|
| SwiftUI | [`List`](https://developer.apple.com/documentation/SwiftUI/List), [Tables](https://developer.apple.com/documentation/SwiftUI/Tables), [`ListStyle`](https://developer.apple.com/documentation/SwiftUI/ListStyle) |
| UIKit | [`UITableView`](https://developer.apple.com/documentation/UIKit/UITableView), [`UIListContentConfiguration`](https://developer.apple.com/documentation/UIKit/UIListContentConfiguration-swift.struct) |
| AppKit | [`NSTableView`](https://developer.apple.com/documentation/AppKit/NSTableView) |