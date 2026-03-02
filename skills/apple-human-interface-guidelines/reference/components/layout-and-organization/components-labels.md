# Labels

Guidelines for using labels — static, uneditable text elements — across Apple platforms.

## Best Practices

- **Use labels for small amounts of non-editable text.** Use [text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) for editable small text, [text views](https://developer.apple.com/design/human-interface-guidelines/text-views) for large/editable text.
- **Prefer system fonts.** Labels support Dynamic Type by default. Custom fonts/styles must remain legible.
- **Make useful label text selectable.** If a label contains useful info (error messages, locations, IP addresses), let people select and copy it.

## System Label Colors

Use system-provided label colors to communicate relative importance:

| System Color | Usage | iOS/iPadOS/tvOS/visionOS | macOS |
|---|---|---|---|
| Label | Primary information | `UIColor.label` | `NSColor.labelColor` |
| Secondary label | Subheading or supplemental text | `UIColor.secondaryLabel` | `NSColor.secondaryLabelColor` |
| Tertiary label | Unavailable item/behavior description | `UIColor.tertiaryLabel` | `NSColor.tertiaryLabelColor` |
| Quaternary label | Watermark text | `UIColor.quaternaryLabel` | `NSColor.quaternaryLabelColor` |

## Platform Considerations

### macOS
- Use `NSTextField` with `isEditable = false` to display uneditable label text.

### watchOS
- **Date/time text components** display current date, time, or both. Configurable formats, calendars, and time zones.
- **Countdown timer text components** display precise countdown/count-up timers in various formats.
- watchOS automatically adjusts label presentation to fit available space and updates content without further app input.
- Consider using date and timer components in complications.

## Developer Components

| Framework | Component |
|---|---|
| SwiftUI | `Label`, `Text` |
| UIKit | `UILabel` |
| AppKit | `NSTextField` |