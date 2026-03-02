# Action Sheets

A modal view that presents choices related to an action people initiate. Supported on iOS, iPadOS, watchOS, and tvOS. **Not supported in visionOS.**

## Best Practices

- **Use an action sheet — not an alert — to offer choices related to an intentional action.** Alerts are for unexpected problems or situation changes; action sheets provide choices for deliberate actions (e.g., Mail's "Delete Draft" / "Save Draft" when canceling a message).
- **Use action sheets sparingly.** They interrupt the current task.
- **Keep titles short enough for a single line.** Long titles get truncated or require scrolling.
- **Provide a message only if necessary.** The title combined with context usually suffices.
- **Provide a Cancel button for actions that might destroy data.** Place it at the bottom (or upper-left in watchOS). SwiftUI confirmation dialogs include Cancel by default.
- **Make destructive choices visually prominent.** Use the destructive button style and place destructive buttons at the **top** of the action sheet.

## Platform Considerations

### iOS, iPadOS

- **Use an action sheet — not a menu — to provide choices related to an action.** People expect action sheets for actions needing clarification; menus appear when deliberately revealed.
- **Avoid letting an action sheet scroll.** Too many buttons make choosing harder, and scrolling risks accidental taps.

### watchOS

Action sheets include a title, optional message, Cancel button, and one or more additional buttons.

**Button styles:**

| Style | Meaning |
|---|---|
| Default | No special meaning |
| Destructive | Destroys user data or performs a destructive action |
| Cancel | Dismisses the view without action |

- **Limit to 4 buttons max (including Cancel).** Since Cancel is required, provide no more than 3 additional choices.

## Developer Reference

- **SwiftUI:** Use `confirmationDialog(_:isPresented:titleVisibility:actions:)` or a presentation modifier for confirmation dialogs.
- **UIKit:** Use `UIAlertController.Style.actionSheet`.
- Destructive button style: `ButtonRole.destructive` (SwiftUI) or `UIAlertAction.Style.destructive` (UIKit).

## Related

- Modality
- Sheets
- Alerts