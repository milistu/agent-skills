# Alerts

Guidelines for designing alerts across Apple platforms. An alert gives people critical information they need right away via a modal view.

## Best Practices

- **Use alerts sparingly.** They interrupt the current task. Each alert should offer only essential information and useful actions.
- **Avoid purely informational alerts.** If not actionable, find an alternative way to communicate within the relevant context (e.g., an inline indicator).
- **Don't alert for common, undoable destructive actions.** No alert needed when deleting an email (undoable, intentional). Do alert for uncommon, irreversible destructive actions.
- **Don't show alerts at app startup.** Use cached/placeholder data with a nonintrusive label instead.

## Content

Alerts display a title, optional informative text, and up to three buttons.

### Platform-Specific Extras
- **iOS, iPadOS, macOS, visionOS:** Can include a text field
- **macOS, visionOS:** Can include an icon and accessory view
- **macOS:** Can add a suppression checkbox and Help button

### Writing Guidelines

- **Be direct with a neutral, approachable tone.** Avoid being oblique, accusatory, or masking severity.
- **Title:** Clearly and succinctly describe the situation — what happened, context, and why. Avoid generic titles like "Error" or error codes. Keep to two lines max.
  - Complete sentence → sentence-style capitalization + ending punctuation
  - Sentence fragment → title-style capitalization, no ending punctuation
- **Informative text:** Include only if it adds value. Keep short, use complete sentences and sentence-style capitalization.
- **Don't explain buttons** in the alert body. If necessary, use the term "choose" and refer to buttons by exact title without quotes.
- **Text fields:** Include only if input is needed to resolve the situation (e.g., password entry).

## Buttons

- **Succinct, logical titles.** Aim for one or two words describing the result. Use verbs/verb phrases related to the alert text (e.g., "View All," "Reply," "Ignore").
- **Use "OK" only for purely informational alerts.** Avoid "Yes" and "No." Always use "Cancel" for cancellation.
- **Prefer specific titles over "OK"** for confirmation alerts — e.g., "Erase," "Convert," "Clear," "Delete."
- **Use title-style capitalization** and no ending punctuation for button titles.

### Button Placement
- Most likely action → **trailing side** of a row or **top** of a stack
- Default button → trailing side of row / top of stack
- Cancel button → **leading side** of a row or **bottom** of a stack

### Destructive Button Style
- Apply destructive style **only** when the button performs a destructive action the user **didn't deliberately choose**.
- If the user deliberately initiated the destructive action (e.g., Empty Trash), don't apply destructive style to the confirming button.

### Cancel Button Rules
- Always include Cancel when there's a destructive action.
- Don't make Cancel the default button.
- To encourage reading the alert, consider making no button the default.
- If a single-button alert must have a default, use "Done" not "Cancel."

### Alternative Cancellation Methods

| Action | Platform |
| --- | --- |
| Exit to Home Screen | iOS, iPadOS |
| Esc or ⌘. on keyboard | iOS, iPadOS, macOS, visionOS |
| Menu button on remote | tvOS |

## Platform Considerations

### iOS / iPadOS
- **Use action sheets (not alerts) for choices related to an intentional action** — e.g., when canceling a Mail draft, offer delete/save/return options via action sheet.
- **Minimize scrolling** — keep titles short and messages brief.

### macOS
- App icon is displayed automatically; you can supply an alternative icon/symbol.
- Supports repeating alert suppression, custom accessory views, and Help buttons.
- **Use caution symbol (`exclamationmark.triangle`) sparingly** — only for unexpected data loss, not routine overwrite/delete operations.

### visionOS
- In Shared Space: alert appears in front of the window, slightly forward on z-axis.
- Alert stays anchored to window if window is moved.
- In Full Space: alert is centered in the wearer's field of view.
- Accessory view max height: **154 pt**, corner radius: **16 pt**.