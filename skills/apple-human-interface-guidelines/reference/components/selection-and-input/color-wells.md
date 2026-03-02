# Color Wells

A color well displays a color picker when people tap or click it. It can use the system-provided picker or a custom interface.

## Best Practices

- **Prefer the system-provided color picker** for a consistent, familiar experience. It lets people save colors accessible from any app and provides consistency across iOS, iPadOS, and macOS.

## Platform Support

- **Supported:** iOS, iPadOS, macOS, visionOS
- **Not supported:** tvOS, watchOS

## macOS-Specific Behavior

- Clicking a color well gives it a highlight (visual confirmation it's active), then opens a color picker.
- After selection, the color well updates to show the new color.
- Color wells support **drag and drop**: users can drag colors between color wells and from the color picker to a color well.

## Related APIs

- `UIColorWell` (UIKit)
- `UIColorPickerViewController` (UIKit)
- `NSColorWell` (AppKit)