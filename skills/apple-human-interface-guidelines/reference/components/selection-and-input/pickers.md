# Pickers

Guidelines for displaying scrollable lists of distinct values that people can choose from.

## Best Practices

- **Use pickers for medium-to-long lists.** For short lists, use a pull-down button instead. For very large sets, use a list or table (which can adjust height and include an index).
- **Use predictable and logically ordered values.** Many values are hidden before interaction — alphabetized or logically ordered lists help people predict and quickly find values.
- **Avoid switching views to show a picker.** Display in context — below or near the field being edited. Typically appears at the bottom of a window or in a popover.
- **Consider less granularity for minutes in date pickers.** Default is 60 values (0–59). You can increase the interval if it divides evenly into 60 (e.g., quarter-hour: 0, 15, 30, 45).

## iOS/iPadOS Date Picker

### Styles

| Style | Description |
|---|---|
| **Compact** | Button showing current value; opens a modal calendar/time editor on tap |
| **Inline** | For time: wheels of values; for dates: inline calendar view |
| **Wheels** | Scrolling wheels; supports keyboard data entry |
| **Automatic** | System-determined based on platform and mode |

### Modes

| Mode | Displays | Notes |
|---|---|---|
| **Date** | Months, days, years | — |
| **Time** | Hours, minutes, optional AM/PM | — |
| **Date and time** | Dates, hours, minutes, optional AM/PM | — |
| **Countdown timer** | Hours and minutes (max 23h 59m) | Not available in inline or compact styles |

- **Use compact date picker when space is constrained.** Shows a button with the current value in the app's accent color. Tapping opens a modal with calendar and time picker. People can make multiple edits before tapping outside to confirm.

## macOS

Two date picker styles:
- **Textual** — Useful in limited space when people make specific date/time selections.
- **Graphical** — Useful for browsing days in a calendar, selecting date ranges, or when a clock face is appropriate.

See `NSDatePicker`.

## tvOS

Pickers available via SwiftUI `Picker`.

## watchOS

- Pickers use the Digital Crown for precise, engaging navigation.
- Supports wheels style for items, dates, and times.
- Configurable with outline, caption, and scrolling indicator.
- For longer lists, use `navigationLink` style — displays picker as a button; tapping shows the list, or users can scrub with Digital Crown without tapping.

See `Picker`, `DatePicker`, and `PickerStyle/navigationLink`.

## Related Components

- Pull-down buttons (short lists alternative)
- Lists and tables (very long lists alternative)

## Developer APIs

- SwiftUI: `Picker`, `DatePicker`
- UIKit: `UIDatePicker`, `UIPickerView`
- AppKit: `NSDatePicker`