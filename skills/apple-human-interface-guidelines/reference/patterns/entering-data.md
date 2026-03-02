# Entering Data

Guidelines for designing data entry experiences that minimize effort and errors across Apple platforms.

## Best Practices

- **Get information from the system whenever possible.** Don't ask people to enter information you can gather automatically (e.g., from settings, location, or calendar with permission).
- **Be clear about the data you need.** Use placeholder prompts (e.g., "username@company.com"), introductory labels (e.g., "Email"), and prefill fields with reasonable defaults to minimize decision-making.
- **Use secure text-entry fields for sensitive data.** Use `SecureField` (SwiftUI) to obscure input. In tvOS, configure digit entry views with `isSecureDigitEntry`. In visionOS, the system-provided secure text field automatically blurs content during AirPlay streaming.
- **Never prepopulate a password field.** Always require explicit entry or use biometric/keychain authentication.
- **Offer choices instead of requiring text entry.** Use pickers, menus, or other selection components when possible — choosing is faster and less error-prone than typing.
- **Support drag-and-drop and paste.** These interactions ease data entry and integrate with system conventions.
- **Dynamically validate field values.** Verify values as people enter them and provide immediate feedback on errors. Use number formatters for numeric fields to accept only valid values and display them consistently (decimal places, percentage, currency).
- **Require data before proceeding.** Disable Next/Continue buttons until all required fields are completed, making requirements clear.

## Platform-Specific

### macOS

- **Use expansion tooltips** to show full text when fields clip or truncate content. The tooltip appears when the pointer hovers over the field, letting people view complete data in undersized fields. Applies to macOS apps including iOS/iPadOS apps running on Mac.

## Related Components

- Text fields
- Virtual keyboards
- Keyboards
- Pickers
- Menus