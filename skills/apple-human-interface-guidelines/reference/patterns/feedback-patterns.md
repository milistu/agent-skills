# Feedback Patterns

Guidelines for providing feedback that helps people understand what's happening, discover actions, understand results, and avoid mistakes.

## Types of Feedback

- **Current status** of something
- **Success or failure** of an important task or action
- **Warning** about an action with negative consequences
- **Opportunity to correct** a mistake or problematic situation

**Key principle:** Match the significance of the information to the way it's delivered. Status information → passive display. Data loss warning → interrupt the user.

## Best Practices

- **Make all feedback accessible.** Use multiple channels (color, text, sound, haptics) so people can receive feedback whether they silence their device, look away, or use VoiceOver.
- **Integrate status feedback into your interface.** Place status near the items it describes so people get information without leaving context. Example: Mail shows unread count and last update in the toolbar.
- **Use alerts only for critical, actionable information.** Alerts disrupt context — overuse diminishes their impact. Reserve for important information only.
- **Warn about unexpected, irreversible data loss only.** Don't warn when data loss is the expected result (e.g., Finder doesn't warn on every file deletion).
- **Confirm significant completed actions.** Example: Apple Pay transaction success. Reserve confirmations for important activities — people expect actions to succeed and only need to know when they don't.
- **Show when a command can't be carried out and explain why.** Example: Maps tells users it can't provide directions to and from the same location.

## Platform Considerations

### watchOS

- **Avoid indeterminate progress indicators** (e.g., loading spinners) in watchOS apps. They make people feel they must keep watching the display. Instead, reassure users they'll receive a notification when the process completes.