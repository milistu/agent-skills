# Virtual Keyboards

Guidelines for using system and custom virtual keyboards across Apple platforms.

## Best Practices

- **Choose a keyboard type matching the content being edited.** Specify semantic meaning for text input areas so the system auto-provides the appropriate keyboard. Use `keyboardType(_:)` (SwiftUI), `textContentType(_:)` (SwiftUI), `UIKeyboardType` (UIKit), `UITextContentType` (UIKit).

### Available Keyboard Types
| Type | Description |
|---|---|
| ASCII capable | Full letter keys + Shift, Delete, Numbers, Space, Return |
| ASCII capable number pad | 10 number keys with phone-style letters + Delete |
| Decimal pad | 10 number keys with phone-style letters + Delete + period |
| Default | Full letter keys + standard controls + Emoji/Dictation |
| Email address | Full letter keys + @ symbol + period + Return |
| Name phone pad | Full letter keys + standard controls + Emoji/Dictation |
| Number pad | 10 number keys with phone-style letters + Delete |
| Numbers and punctuation | Numbers + 15 punctuation keys + Letters/Space/Return |
| Phone pad | 10 number keys + Delete + plus/star/hash |
| Twitter | Full letter keys + @ symbol + hash |
| URL | Full letter keys + period + slash + .com + Return |
| Web search | Full letter keys + period + Go button |

- **Customize the Return key type when it clarifies the experience.** Use `submitLabel(_:)` (SwiftUI) or `UIReturnKeyType` (UIKit) to change the Return key label (e.g., "Search", "Go").

## Custom Input Views

Replace the system keyboard with a custom view for app-specific data entry tasks (e.g., Numbers' spreadsheet input). Use `ToolbarItemPlacement` (SwiftUI) or `inputViewController` (UIKit).

- **Ensure the custom input view makes sense in your app's context.** People should understand why they can't access the system keyboard.
- **Play the standard keyboard click sound** when people tap keys. Use `playInputClick()` (UIKit). Users control this in Settings > Sounds.

## Custom Keyboards (App Extensions)

Custom keyboard app extensions replace the system keyboard systemwide (iOS, iPadOS, tvOS). They work in all apps except secure text fields and phone number fields.

- **Provide an obvious way to switch keyboards.** Users expect Globe key-like behavior for switching.
- **Don't duplicate system keyboard features.** The Emoji/Globe key and Dictation key appear automatically beneath custom keyboards on some devices.
- **Consider providing a tutorial in your app** explaining how to choose, activate, and use your keyboard.

## Platform Considerations

### iOS / iPadOS

- **Use the keyboard layout guide** to keep important UI visible when the keyboard appears. See [Adjusting your layout with keyboard layout guide](https://developer.apple.com/documentation/UIKit/adjusting-your-layout-with-keyboard-layout-guide). Without it, the keyboard can obscure text fields and buttons.
- **Place custom controls above the keyboard thoughtfully.** Use an input accessory view for task-relevant controls. Apply Liquid Glass if other views use it, or use a standard toolbar (which adopts Liquid Glass automatically). Use keyboard layout guide + standard padding for positioning. See `ToolbarItemPlacement` (SwiftUI), `inputAccessoryView` (UIKit), `UIKeyboardLayoutGuide` (UIKit).

### macOS
Not supported.

### tvOS
Displays a linear virtual keyboard when people select a text field via Siri Remote. Grid keyboard appears for other input devices.

### visionOS
The virtual keyboard supports both direct and indirect gestures and appears in a separate movable window. **You don't need to account for keyboard location in your layouts.**

### watchOS
Keyboard appears if the device screen is large enough; otherwise dictation or Scribble is used. You can't change keyboard type, but **set `textContentType(_:)` to help the system offer suggestions**. Users can also enter text via paired iPhone.