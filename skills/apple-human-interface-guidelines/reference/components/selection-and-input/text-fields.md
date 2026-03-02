# Text Fields

Guidelines for designing text fields — rectangular areas for entering or editing small, specific pieces of text.

## Best Practices

- **Use text fields for small amounts of information** (name, email). For larger text input, use a text view instead.
- **Show placeholder text** (e.g., "Email", "Password") to communicate purpose. Since placeholder text disappears on input, include a separate label to remind users of the field's purpose.
- **Use secure text fields** for sensitive data like passwords (`SecureField` in SwiftUI).
- **Size fields to match anticipated input length** — the size helps users gauge how much information to provide.
- **Stack multiple text fields vertically** with even spacing. Use consistent widths to create organized layouts. Group related fields with similar widths.
- **Ensure logical tab order** between fields. The system handles this automatically in most cases.
- **Validate fields contextually:**
  - Email addresses: validate when user leaves the field
  - Usernames/passwords: validate before the user leaves the field
- **Use number formatters** for numeric data — they restrict input to numbers and can format as decimals, percentages, or currency. Don't assume formatting; it varies by locale.
- **Handle text overflow appropriately:**
  - Default: clip text at field bounds
  - Options: wrap at character/word level, or truncate with ellipsis (beginning, middle, or end)
- **Use expansion tooltips** to show full text for clipped/truncated content on pointer hover.
- **Show the appropriate keyboard type** (iOS, iPadOS, tvOS, visionOS) for the content type (numbers, URLs, etc.). See Virtual Keyboards guidelines.
- **Minimize text entry on tvOS and watchOS** — prefer buttons or selection lists over text input.

## Platform-Specific Guidelines

### iOS / iPadOS
- Display a **Clear button** in the trailing end to let users quickly erase input.
- Use **images and buttons** in text fields: leading end for field purpose indication, trailing end for features like bookmarking.

### macOS
- Consider a **combo box** when pairing text input with a list of choices.

### watchOS
- **Present text fields only when necessary** — prefer displaying a list of options over requiring text entry.

### tvOS / visionOS
- No additional platform-specific considerations.