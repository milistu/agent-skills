# The Menu Bar

Comprehensive guidelines for menu bar design on macOS and iPadOS, including standard menu order, menu item specifications, and platform-specific considerations.

## Menu Order (Anatomy)

Menus appear in this order when present:

1. **YourAppName** (short version of app name)
2. **File**
3. **Edit**
4. **Format**
5. **View**
6. **App-specific menus** (if any)
7. **Window**
8. **Help**

macOS also includes the Apple menu (leading side) and menu bar extras (trailing side).

## Best Practices

- **Support default system-defined menus and their ordering** — people expect familiar ordering
- **Always show the same set of menu items** — disable unavailable items rather than hiding them
- **Use familiar icons** for common actions (Copy, Share, Delete) matching system icons
- **Support standard keyboard shortcuts** for standard menu items (Copy, Cut, Paste, Save, Print)
- **Prefer short, one-word menu titles** — use title-style capitalization if multi-word

## App Menu

Items that apply to the app as a whole. App name displayed in bold.

| Menu Item | Action | Guidance |
|---|---|---|
| About *YourAppName* | Shows About window with copyright/version | Prefer ≤16 characters. No version number. |
| Settings… | Opens settings window (macOS) or app's page in iPadOS Settings | App-level settings only. Document-specific settings go in File menu. |
| Optional app-specific items | Custom app-level config actions | List after Settings in same group |
| Services (macOS only) | Submenu of system/other-app services | |
| Hide *YourAppName* (macOS only) | Hides app and all windows | Same short app name as About |
| Hide Others (macOS only) | Hides all other apps | |
| Show All (macOS only) | Shows all other apps | |
| Quit *YourAppName* | Quits app. Option key → Quit and Keep Windows | Same short app name as About |

Display About first, with separator after it.

## File Menu

Manages files/documents. Rename or remove if app doesn't handle files.

| Menu Item | Action | Guidance |
|---|---|---|
| New *Item* | Creates new document/file/window | Use term naming what app creates (e.g., Calendar uses *Event*, *Calendar*) |
| Open | Opens selected item or presents selection interface | Add ellipsis if more input required |
| Open Recent | Submenu of recently opened docs with Clear Menu | List recognizable names (not paths), most recent first |
| Close | Closes current window/document. Option → Close All. Tab window: Close Tab | Consider adding Close Window for tab-based windows |
| Close Tab | Closes current tab. Option → Close Other Tabs | |
| Close File | Closes file and all associated windows | For apps with multiple views of same file |
| Save | Saves current document | Auto-save periodically. Prompt new docs for name/location. Use pop-up for format selection. |
| Save All | Saves all open documents | |
| Duplicate | Duplicates current document. Option → Save As | Prefer over Save As, Export, Copy To, Save To |
| Rename… | Change document name | |
| Move To… | Choose new location | |
| Export As… | Export in different format; original stays open | Only for formats app doesn't typically handle |
| Revert To | Submenu of recent versions (with autosaving) | |
| Page Setup… | Printing parameters (paper size, orientation) | For document-specific parameters only |
| Print… | Opens standard Print panel | |

## Edit Menu

Changes to content and Clipboard commands. Useful even in non-document apps.

| Menu Item | Action | Guidance |
|---|---|---|
| Undo | Reverses previous operation | Clarify target (e.g., "Undo Paste and Match Style", "Undo Typing") |
| Redo | Reverses previous Undo | Clarify target similarly |
| Cut | Removes selection to Clipboard | |
| Copy | Duplicates selection to Clipboard | |
| Paste | Inserts Clipboard at insertion point | Clipboard unchanged after paste |
| Paste and Match Style | Inserts Clipboard matching surrounding style | |
| Delete | Removes selection (not to Clipboard) | Use "Delete" not "Erase" or "Clear" |
| Select All | Highlights all selectable content | |
| Find | Submenu: Find, Find and Replace, Find Next, Find Previous, Use Selection for Find, Jump to Selection | May belong in File menu if searching files/objects |
| Spelling and Grammar | Submenu: Show Spelling and Grammar, Check Document Now, Check Spelling While Typing, Check Grammar With Spelling, Correct Spelling Automatically | |
| Substitutions | Submenu: Show Substitutions, Smart Copy/Paste, Smart Quotes, Smart Dashes, Smart Links, Data Detectors, Text Replacement | |
| Transformations | Submenu: Make Uppercase, Make Lowercase, Capitalize | |
| Speech | Submenu: Start Speaking, Stop Speaking | |
| Start Dictation | System-added at bottom of Edit menu | |
| Emoji & Symbols | System-added at bottom of Edit menu | |

## Format Menu

Text formatting. Exclude if app doesn't support formatted text.

| Menu Item | Submenu Items |
|---|---|
| Font | Show Fonts, Bold, Italic, Underline, Bigger, Smaller, Show Colors, Copy Style, Paste Style |
| Text | Align Left, Center, Justify, Align Right, Writing Direction, Show Ruler, Copy Ruler, Paste Ruler |

## View Menu

Customizes appearance of all app windows. Provide even if only supporting a subset (e.g., just full-screen).

**Toggle item titles to reflect current state** (e.g., "Show Toolbar" when hidden, "Hide Toolbar" when visible).

| Menu Item | Action |
|---|---|
| Show/Hide Tab Bar | Toggles tab bar visibility |
| Show All Tabs / Exit Tab Overview | Mission Control-style tab overview |
| Show/Hide Toolbar | Toggles toolbar visibility |
| Customize Toolbar | Opens toolbar customization |
| Show/Hide Sidebar | Toggles sidebar visibility |
| Enter/Exit Full Screen | Full-screen in new space |

View menu does NOT include window navigation/management (that's the Window menu).

## App-Specific Menus

Appear between View and Window menus.

- List commands in menu bar even if available elsewhere — improves discoverability, keyboard shortcuts, Full Keyboard Access
- Reflect app hierarchy (e.g., Mail: Mailbox → Message → Format)
- Order from most to least general/commonly used

## Window Menu

Navigate, organize, and manage windows. **Provide even for single-window apps** (Minimize/Zoom needed for Full Keyboard Access).

| Menu Item | Action | Guidance |
|---|---|---|
| Minimize | Minimizes to Dock. Option → Minimize All | |
| Zoom | Toggles predefined/user size. Option → Zoom All | Don't use for full-screen; use View menu |
| Show Previous Tab | Previous tab | |
| Show Next Tab | Next tab | |
| Move Tab to New Window | Opens tab in new window | |
| Merge All Windows | Combines into single tabbed window | |
| Enter/Exit Full Screen | Full-screen mode | Only if app lacks View menu |
| Bring All to Front | All windows to front. Option → Arrange in Front | |
| *Open window names* | Brings selected window to front | Alphabetical order. Don't list panels/modals. |

Consider including show/hide items for panels.

## Help Menu

Trailing end of menu bar. macOS auto-includes search field with Help Book format.

| Menu Item | Guidance |
|---|---|
| Send *YourAppName* Feedback to Apple | Opens Feedback Assistant |
| *YourAppName* Help | Opens Help Viewer (Help Book format) |
| Additional items | Separator before. Keep count small. Consider linking from within help docs instead. |

## Dynamic Menu Items

Items that change behavior when chosen with a modifier key pressed.

- Don't make dynamic items the **only** way to accomplish a task
- Use primarily in menu bar menus (not contextual/Dock menus)
- Require only a **single** modifier key
- macOS auto-sizes menu width to fit widest item including dynamic variants

## Platform Considerations

**Not supported in:** iOS, tvOS, visionOS, watchOS

### iPadOS

| Aspect | iPadOS | macOS |
|---|---|---|
| Visibility | Hidden until revealed | Visible by default |
| Alignment | Centered | Leading |
| Menu bar extras | Not available | System + custom |
| Window controls | In menu bar when full screen | Never in menu bar |
| Apple menu | Not available | Always available |
| App menu | About, Services, visibility items unavailable | Always available |

- Ensure all functions accessible through UI (menu bar often hidden full screen)
- `YourAppName > Settings` opens iPadOS Settings page; internal preferences get separate menu item
- For tab-navigation apps, consider adding tabs as View menu items with key bindings
- Group items into submenus more than on Mac (larger rows, smaller screens)

### macOS Menu Bar Extras

Icon in menu bar visible even when app isn't frontmost. System may hide extras to make room.

- Use a symbol (SF Symbol or custom icon); black and clear colors, 24pt menu bar height
- Display a **menu** (not popover) on click, unless functionality is too complex
- Let **users** decide whether to show the extra (via settings)
- Don't rely on extras being visible; also provide a Dock menu
- Expose functionality through other means (Dock menus always available)