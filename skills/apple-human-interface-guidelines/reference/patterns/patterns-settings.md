# Settings

Guidelines for designing settings experiences across Apple platforms, including where to place settings, how to structure them, and platform-specific considerations.

## Best Practices

- **Provide sensible defaults** that work for the largest number of people, minimizing the need for manual adjustment.
- **Minimize the number of settings offered.** Too many settings make the experience less approachable and harder to navigate.
- **Make settings accessible in expected ways:**
  - Apps: Command-Comma (⌘,) keyboard shortcut
  - Games: Esc (Escape) key
- **Avoid asking for information you can detect automatically** (e.g., connected controllers, Dark Mode state).
- **Respect systemwide settings** — don't include redundant versions of global options (accessibility, scrolling behavior, authentication) in your custom settings. This confuses people about whether systemwide settings apply.

## Settings Categories

### General Settings
- Place **infrequently changed** settings in your custom settings area (window configuration, game-saving behavior, keyboard mappings, account options).
- People must suspend their current task to access these, so only include options that don't need frequent changes.

### Task-Specific Options
- Let people modify task-specific options **in context**, without going to a settings area.
- Examples: showing/hiding view elements, reordering collections, filtering lists — make these available on the screens they affect.
- In games, players adjust task-specific approaches as part of gameplay, not as settings.

### System Settings
- Add only the **most rarely changed** options to the system-provided Settings app.
- Consider providing a button that opens the system Settings app directly from your interface.

## Platform Considerations

### macOS

- **Include a Settings item in the App menu.** Don't add settings buttons to window toolbars (saves space for essential commands).
- Settings window opens via Command-Comma (⌘,).
- Settings window uses a **toolbar with buttons** for switching between panes of related settings.
- **Dim the minimize and maximize buttons** on the settings window — no need to keep it in Dock or resize it.
- Use a **noncustomizable toolbar** that remains visible and always indicates the active button.
- **Update the window title** to reflect the currently visible pane. If no multiple panes, use "*App Name* Settings".
- **Restore the most recently viewed pane** when reopening settings.
- For document-level options, add to the **File menu** instead.

### watchOS

- Apps don't add custom settings to the system Settings app.
- Instead, make essential options available at the **bottom of the main view** or use a **More menu** to reconfigure objects.

### iOS, iPadOS, tvOS, visionOS

No additional platform-specific considerations.