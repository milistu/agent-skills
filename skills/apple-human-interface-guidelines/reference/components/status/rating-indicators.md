# Rating Indicators

A rating indicator uses horizontally arranged graphical symbols (default: stars) to communicate a ranking level.

## Key Behaviors
- Does **not** display partial symbols; rounds value to show complete symbols only
- Symbols are always equally spaced and don't expand/shrink to fit the component's width

## Best Practices
- **Make it easy to change rankings** — In a list of ranked items, let people adjust rank inline without navigating to a separate editing screen.
- **If replacing the star with a custom symbol, ensure its purpose is clear** — Stars are universally recognized for ratings; other symbols may not be associated with a rating scale.

## Platform Support
- **macOS**: Supported via `NSLevelIndicator.Style.rating` (AppKit)
- **iOS, iPadOS, tvOS, visionOS, watchOS**: Not supported

## Related
- [Ratings and Reviews](/design/human-interface-guidelines/ratings-and-reviews) pattern