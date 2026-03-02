# Edit Menus

Guidelines for edit menus that let people make changes to selected content (text, images, files, objects like contact cards, charts, or map locations).

## Platform Behavior

- **iOS**: Compact horizontal list on touch-and-hold or double-tap. Trailing chevron expands to a context menu.
- **iPadOS**: Compact horizontal on touch; context menu on keyboard/pointing device.
- **macOS**: Editing commands via context menu or app's Edit menu in menu bar.
- **visionOS**: Pinch-and-hold opens horizontal bar; also available as context menu.
- **tvOS/watchOS**: Not supported.

## Best Practices

- **Prefer the system-provided edit menu.** Don't create custom menus that duplicate standard commands. See `UIResponderStandardEditActions` for standard commands.
- **Use system-defined interactions to reveal the menu.** Touch-and-hold on touchscreen, pinch-and-hold in visionOS, secondary click with trackpad/keyboard. Don't require custom interactions for standard tasks.
- **Show only relevant commands.** Remove or dim commands that don't apply. Don't show Copy/Cut with no selection; don't show Paste with nothing on the pasteboard.
- **Place custom commands near related system commands.** E.g., custom formatting commands after system formatting commands. Avoid overwhelming users with too many custom commands.
- **Allow selecting and copying noneditable text** when useful (image captions, social media statuses). Let people copy content text, but not control labels.
- **Support undo and redo.** Edit menus don't require confirmation, so undo/redo is essential for recovery.
- **Avoid redundant controls** that duplicate edit menu functions. People expect to use the edit menu or keyboard shortcuts for standard editing.
- **Differentiate deletion commands.** Delete behaves like pressing Delete key; Cut copies to pasteboard before deleting.

## Content

- Use short labels (verbs or short verb phrases) that succinctly describe the action.

## iOS & iPadOS Specifics

- **Support both styles.** Compact horizontal style appears for Multi-Touch gestures; vertical context menu style appears for keyboard/pointing device.
- **Adjust placement if necessary.** Default position is above or below insertion point/selection. You can change position to prevent covering important content (but not menu shape or pointer).

## macOS Specifics

For item ordering in the macOS Edit menu, see the menu bar Edit menu guidelines.