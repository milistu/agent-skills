# Dock Menus

Guidelines for macOS Dock menus — the menu revealed when secondary-clicking an app's icon in the Dock. Contains both system-provided and custom items.

**Platform:** macOS only.

## Best Practices

- Label items succinctly and organize logically (follow general [Menus] guidelines).
- **Make custom Dock menu items available elsewhere too.** Not everyone uses a Dock menu — offer the same commands in menu bar menus or within your interface.
- **Prefer high-value custom items.** Examples:
  - List all currently or recently open windows for quick navigation.
  - Include actions useful when the app isn't frontmost or has no open windows (e.g., Mail includes "Get New Mail" and "Compose New Message" alongside window list).

## Related

- iOS/iPadOS equivalent: Home Screen quick actions (long press app icon).
- Developer API: `applicationDockMenu(_:)` (AppKit, NSApplicationDelegate).