# Undo and Redo

Guidelines for implementing undo and redo functionality across Apple platforms.

## Best Practices

- **Help people predict results** — Describe the result in undo alerts (iOS shake) or modify menu item labels to identify the action (e.g., "Undo Typing", "Redo Bold").
- **Show results of undo/redo** — If the affected content is no longer visible, scroll or navigate to highlight the restored/changed content. Prevents users from thinking the action had no effect.
- **Support multiple undos** — Don't place unnecessary limits. Users expect to undo every action since a logical checkpoint (opening a document, saving).
- **Consider batch undo** — Let users revert multiple related changes at once (e.g., incremental adjustments to a single property) or undo all changes since last save/open.
- **Use dedicated buttons only when necessary** — Users expect system-supported methods (Edit menu, keyboard shortcuts, shake gesture, three-finger swipe). If providing buttons, use standard system-provided symbols and place them in a toolbar.

## Platform-Specific Guidelines

### iOS / iPadOS

- **Don't redefine standard undo gestures** — Three-finger swipe for undo/redo and shake-to-undo are system conventions; redefining them causes confusion.
- **Keep undo/redo alert titles brief and precise** — The system automatically prefixes "Undo " or "Redo " (with trailing space). Provide 1–2 additional words describing the operation (e.g., "Undo Name", "Redo Address Change").

### macOS

- **Place undo/redo in the Edit menu** with standard keyboard shortcuts:
  - **Undo:** ⌘Z
  - **Redo:** ⇧⌘Z

### visionOS

No additional considerations.

### tvOS / watchOS

Not supported.