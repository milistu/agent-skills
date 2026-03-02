# Combo Boxes

A combo box combines a text field with a pull-down button in a single control. People can enter a custom value or choose from predefined values. Custom values are not added to the list.

**Platform support:** macOS only (not supported in iOS, iPadOS, tvOS, visionOS, or watchOS).

## Best Practices

- **Populate the field with a meaningful default value from the list.** The default value should refer to the hidden choices but doesn't need to be the first item.
- **Use an introductory label** with title-style capitalization ending with a colon to indicate what types of items to expect.
- **Provide relevant choices.** Offer the most likely choices in the list while allowing custom entry.
- **Ensure list items aren't wider than the text field.** Truncated items are hard to read.

## Related Components

- Text fields
- Pull-down buttons

## Developer Reference

- `NSComboBox` (AppKit)