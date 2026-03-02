# Path Controls

A path control shows the file system path of a selected file or folder. **macOS only** — not supported on iOS, iPadOS, tvOS, visionOS, or watchOS.

## Styles

| Style | Description |
|-------|-------------|
| **Standard** | A linear list showing root disk, parent folders, and selected item, each with icon and name. Truncates middle items if space is limited. If editable, supports drag-and-drop to select an item and display its path. |
| **Pop-up** | Shows icon and name of the selected item. Clicking opens a menu with root disk, parent folders, and selected item. If editable, the menu includes a "Choose" command and supports drag-and-drop. |

## Best Practices

- **Use a path control in the window body, not the window frame.** Path controls aren't intended for toolbars or status bars. The Finder's path bar appears at the bottom of the window body, not in the status bar.

## Developer Reference

- `NSPathControl` (AppKit)

## Related

- [File management](/design/human-interface-guidelines/file-management)
- [Pop-up buttons](/design/human-interface-guidelines/pop-up-buttons)