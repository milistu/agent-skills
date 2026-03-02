# Token Fields

A token field is a text field that converts text into selectable, manipulable tokens. **macOS only** — not supported in iOS, iPadOS, tvOS, visionOS, or watchOS.

Example: Mail uses token fields for address fields in the compose window, converting recipient names into tokens that can be selected, reordered via drag, or moved between fields.

## Features

- **Suggestion list**: Can present suggestions as people type (e.g., Mail suggests recipients in address fields)
- **Context menus**: Individual tokens can include contextual menus with info or editing options (e.g., Mail recipient tokens offer editing name, marking as VIP, viewing contact card)
- **Search tokens**: Tokens can represent search terms in some contexts (see Search Fields)

## Best Practices

- **Add value with a context menu.** Provide a context menu with additional options or information about a token.
- **Provide additional ways to convert text into tokens.** By default, typing a comma creates a token. Consider adding shortcuts like pressing Return.
- **Customize the suggestion delay.** Suggestions appear immediately by default, which may distract users while typing. Adjust the delay to a comfortable level if your app suggests tokens.

## Related Components

- Text Fields
- Search Fields
- Context Menus

## Developer Reference

- `NSTokenField` (AppKit)