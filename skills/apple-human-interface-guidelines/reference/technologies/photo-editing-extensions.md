# Photo Editing Extensions

Guidelines for photo-editing extensions that let people modify photos and videos within the Photos app.

Edits are always saved as new files, preserving originals. Users access photo editing extensions via the extension icon in the toolbar while in edit mode, which displays in a modal view with a top toolbar.

## Best Practices

- **Confirm cancellation of edits.** If someone taps Cancel, don't immediately discard changes. Ask them to confirm, and inform them edits will be lost. Skip this confirmation if no edits have been made yet.
- **Don't provide a custom top toolbar.** The extension loads within a modal view that already includes a toolbar. A second toolbar is confusing and wastes space.
- **Let people preview edits.** Allow people to see the result of their work before closing the extension and returning to Photos.
- **Use your app icon for the extension icon.** This instills confidence the extension is provided by your app.

## Platform Support

Supported on iOS, iPadOS, and macOS. Not supported on tvOS, visionOS, or watchOS.