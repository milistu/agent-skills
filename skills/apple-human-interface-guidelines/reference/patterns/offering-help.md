# Offering Help

Guidelines for providing contextual help in Apple platform apps, including tips (TipKit) and tooltips.

## Best Practices

- **Match help to task complexity.** Simple tasks → inline views with succinct descriptions. Complex/multistep tasks → tutorials for larger goals.
- **Directly relate help to the current action/task.** Make it easy to dismiss if not needed.
- **Use relevant, consistent language and images.** Don't show Siri Remote tips when someone uses a game controller. Don't say "click" on iPhone or "tap" on Mac.
- **Make help content inclusive.** Follow Apple's Inclusion guidelines.
- **Don't explain how standard components work.** Describe the specific action/task the standard element performs in your app. For unique controls or nonstandard input, orient people quickly with animation or graphics rather than lengthy text.

## Creating Tips (TipKit)

Tips are small, transient views that briefly describe how to use a feature. Use TipKit framework.

### Tip Types

| Type | When to Use |
|------|-------------|
| **Popover** | Preserve content flow; appears atop nearby content, points to a feature |
| **Annotation** (inline) | Point to a specific UI element; embedded among surrounding content |
| **Hint** (inline) | Not related to a specific UI element; embedded among content |

### Tip Content Guidelines

- **Use tips for simple features only.** If a feature requires more than 3 actions, it's too complicated for a tip.
- **Keep tips short, actionable, engaging.** 1-2 sentences max. Use direct, action-oriented language. No promotional content or unrelated features.
- **Define eligibility rules.** Use parameter-based or event-based rules. Don't show tips for features already used. Set display frequency (e.g., once every 24 hours) when multiple tips exist.

### Tip Symbols/Images

- If including an icon that people associate with the feature, **prefer the filled variant** of the symbol.
- **Don't duplicate:** If an annotation tip points to a UI element with an icon (e.g., a star), don't repeat that same icon inside the tip — use text only.

### Tip Buttons

- Use buttons to direct people to settings or additional resources (e.g., a setup flow).

## Tooltips (macOS, visionOS)

Tooltips (called "help tags" in user documentation) appear when a person holds the pointer over an element (macOS) or looks at it (visionOS). Use `help(_:)` in SwiftUI.

- **Describe only the indicated control.** Don't explain nearby controls or larger tasks.
- **Explain the action the control initiates.** Start with a verb (e.g., "Restore default settings" or "Add or remove a language from the list").
- **Don't repeat the control's name** in its tooltip.
- **Keep to 60-75 characters max** (account for localization expanding text).
- **Use sentence case.** Omit ending punctuation unless required for consistency.
- **Consider context-sensitive tooltips** with different text for different control states.

## Platform Notes

- No additional considerations for iOS, iPadOS, tvOS, or watchOS beyond the general best practices and tips guidance above.
- macOS and visionOS have tooltip-specific guidance (see above).