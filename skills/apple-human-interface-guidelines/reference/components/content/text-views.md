# Text Views

A text view displays multiline, styled text content, optionally editable. Text views can be any height and allow scrolling when content extends outside the view. Content is aligned to the leading edge by default and uses system label color.

In iOS, iPadOS, and visionOS, an editable text view shows a keyboard when selected.

## Best Practices

- **Use text views for long, editable, or specially formatted text.** For small amounts of text, use a label or (if editable) a text field instead.
- **Keep text legible.** Adopt Dynamic Type so text adapts to user text-size preferences. Test with accessibility options (e.g., bold text).
- **Make useful text selectable.** If a text view contains practical info (error messages, serial numbers, IP addresses), let people select and copy it.

## Platform Considerations

### iOS, iPadOS
- **Show the appropriate keyboard type.** Match the keyboard to the content type expected in the text view. See Virtual Keyboards guidance.

### tvOS
- Text views are display-only. Use text fields for editable text, as text input in tvOS is minimal by design.

### macOS, visionOS, watchOS
No additional considerations.

## Related Components
- Labels — for short, non-editable text
- Text Fields — for single-line editable text
- Combo Boxes — for text input with predefined options