# Keyboards

Guidelines for physical keyboard input support, standard keyboard shortcuts, and creating custom shortcuts across Apple platforms.

## Best Practices

- **Support Full Keyboard Access** (iOS, iPadOS, macOS, visionOS) — lets people navigate and activate windows, menus, controls, and system features using only the keyboard.
- **iPadOS note:** Supports keyboard navigation in text fields, text views, and sidebars. Do NOT add keyboard navigation for buttons, segmented controls, and switches — let Full Keyboard Access handle those.
- **Respect standard keyboard shortcuts.** Don't repurpose standard shortcuts people rely on across the system. Create custom shortcuts for unique frequent actions instead.
- Only repurpose a standard shortcut if its action doesn't apply (e.g., Command-I for Get Info if app has no text editing).

## Standard Keyboard Shortcuts Reference

| Primary Key | Shortcut | Action |
|---|---|---|
| Space | Cmd-Space | Show/hide Spotlight |
| | Opt-Cmd-Space | Show Spotlight results window |
| | Ctrl-Cmd-Space | Show Special Characters window |
| Tab | Shift-Tab | Navigate controls in reverse |
| | Cmd-Tab | Switch to next recent app |
| | Shift-Cmd-Tab | Switch to previous app |
| | Ctrl-Tab | Move focus to next control group |
| | Ctrl-Shift-Tab | Move focus to previous control group |
| Esc | Esc | Cancel current action |
| | Opt-Cmd-Esc | Force Quit dialog |
| Comma (,) | Cmd-Comma | Open app settings |
| Period (.) | Cmd-Period | Cancel an operation |
| ? | Cmd-? | Open Help menu |
| ` | Cmd-` | Activate next open window in frontmost app |
| | Shift-Cmd-` | Activate previous window |
| - | Cmd-Hyphen | Decrease selection size |
| = | Shift-Cmd-= | Increase selection size |
| : | Cmd-: | Spelling window |
| ; | Cmd-; | Find misspelled words |
| A | Cmd-A | Select All |
| B | Cmd-B | Bold |
| C | Cmd-C | Copy |
| | Shift-Cmd-C | Colors window |
| | Opt-Cmd-C | Copy style |
| D | Opt-Cmd-D | Show/hide Dock |
| | Ctrl-Cmd-D | Dictionary definition |
| E | Cmd-E | Use selection for Find |
| F | Cmd-F | Find |
| | Opt-Cmd-F | Jump to search field |
| | Ctrl-Cmd-F | Enter full screen |
| G | Cmd-G | Find next |
| | Shift-Cmd-G | Find previous |
| H | Cmd-H | Hide app |
| | Opt-Cmd-H | Hide all other apps |
| I | Cmd-I | Italic / Info window |
| | Opt-Cmd-I | Inspector window |
| J | Cmd-J | Scroll to selection |
| M | Cmd-M | Minimize window |
| | Opt-Cmd-M | Minimize all windows |
| N | Cmd-N | New document |
| O | Cmd-O | Open document dialog |
| P | Cmd-P | Print |
| | Shift-Cmd-P | Page Setup |
| Q | Cmd-Q | Quit app |
| | Shift-Cmd-Q | Log out |
| S | Cmd-S | Save |
| | Shift-Cmd-S | Save As / Duplicate |
| T | Cmd-T | Fonts window |
| | Opt-Cmd-T | Show/hide toolbar |
| U | Cmd-U | Underline |
| V | Cmd-V | Paste |
| | Shift-Cmd-V | Paste As |
| | Opt-Cmd-V | Paste Style |
| | Opt-Shift-Cmd-V | Paste and Match Style |
| W | Cmd-W | Close window |
| | Shift-Cmd-W | Close file and windows |
| | Opt-Cmd-W | Close all windows |
| X | Cmd-X | Cut |
| Z | Cmd-Z | Undo |
| | Shift-Cmd-Z | Redo |
| 3 | Shift-Cmd-3 | Screenshot to file |
| | Ctrl-Shift-Cmd-3 | Screenshot to clipboard |
| 4 | Shift-Cmd-4 | Selection screenshot to file |
| | Ctrl-Shift-Cmd-4 | Selection screenshot to clipboard |
| 8 | Opt-Cmd-8 | Toggle screen zoom |
| Arrows | Shift-Cmd-Arrow | Extend selection to semantic boundary |
| | Shift-Arrow | Extend selection one unit |
| | Opt-Shift-Arrow | Extend selection to word/paragraph boundary |
| | Ctrl-Arrow | Move focus within views/tables |

### Localization Shortcuts

| Shortcut | Action |
|---|---|
| Ctrl-Space | Toggle between current and last input source |
| Ctrl-Opt-Space | Switch to next input source |
| Cmd-Right arrow | Change to Roman script layout |
| Cmd-Left arrow | Change to system script layout |

## Custom Keyboard Shortcuts

- **Define custom shortcuts only for the most frequently used app-specific commands.** Too many shortcuts make apps harder to learn.
- **Avoid using Control as a modifier** — the system uses it extensively for systemwide features.
- **Don't add a modifier to an existing shortcut for an unrelated command** (e.g., don't use Shift-Cmd-Z for something unrelated to undo/redo).
- **Don't add Shift to shortcuts using the upper character of a two-character key.** Use Command-Question mark, not Shift-Command-Slash.
- **Let the system localize and mirror shortcuts** — it handles right-to-left layout mirroring automatically.

### Modifier Key Order and Usage

Always list modifier keys in this order: **Control → Option → Shift → Command**

| Modifier | Usage |
|---|---|
| **Command** | Prefer as the main modifier key in custom shortcuts |
| **Shift** | Prefer as secondary modifier complementing a related shortcut |
| **Option** | Use sparingly for less-common commands or power features |
| **Control** | Avoid — system uses it for many systemwide features |

**Tip:** Some languages require modifier keys for certain characters (e.g., Option-5 for "{" on French keyboards). Prefer using Command only, and if using additional modifiers, use them only with alphabetic characters.

### Modifier Key Behaviors in Direct Manipulation

- **Command + drag** → moves items as a group
- **Shift + drag-resize** → constrains to aspect ratio
- **Holding arrow key** → moves by smallest app-defined distance unit

## visionOS

- Keyboard shortcuts appear in a shortcut interface when people hold Command on a connected keyboard, organized by system-defined menu categories (File, Edit, View, etc.).
- **Write descriptive shortcut titles** — the interface shows a flat list per category (no submenus for context). Use `discoverabilityTitle` in UIKit.
- A virtual keyboard overlay appears above the physical keyboard, providing typing completion and controls.