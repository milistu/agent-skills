# File Management

Guidelines for document-based apps that help people create, edit, save, and browse files across Apple platforms.

## Creating and Opening Files

- **Use app menus and keyboard shortcuts** for creating and opening documents. In iPadOS and macOS, people expect familiar menu commands (New, Open). iPadOS shows them in the shortcuts interface when holding Command on hardware keyboard; macOS shows them in the File menu.
- Always include an **Add (+) button** for creating new documents regardless of keyboard shortcut availability.
- **Custom file browsers should respect the platform's file system.** Default to showing the most relevant location (Documents, iCloud, or most recently selected), but let people navigate the full file system.

## Saving Work

- **Auto-save by default** — perform periodic saves during editing and when closing a file or switching apps. Avoid requiring explicit save actions.
- **Hide file extensions by default**, but let people view them if they choose. Reflect this choice in all save/open interfaces.

## Quick Look Previews

- **Use a Quick Look viewer** to let people preview files your app can't open, so they don't have to leave your app.
- **Implement a Quick Look generator** if your app produces custom file types, enabling Finder, Files, and Spotlight to display previews.

## iOS / iPadOS

### Document Launcher (iOS 18+ / iPadOS 18+)

Document-based apps can use the system's document launcher — a full-screen browsing experience. See [`DocumentGroupLaunchScene`](https://developer.apple.com/documentation/SwiftUI/DocumentGroupLaunchScene).

**Three main parts:**
1. **Title card** — displays app title and two app-specific buttons
2. **Background image** — behind the title card, plus optional *accessory* images around it
3. **File browser sheet** — contains a file browser and optional custom toolbar controls

**Guidelines:**
- **Title card buttons** should map to the app's most important functions. Primary button typically creates a new document; secondary provides additional options (e.g., "Start Writing" / "Choose a Template").
- **Background** should be clearly distinct from accessories and title card — use solid color, gradient, or simple pattern. Avoid complex images.
- **Accessories:** Can be placed in front of and behind the title card for depth, but ensure app name and buttons remain visible. Avoid clutter. Test across screen sizes and orientations.
- **Use animation sparingly.** Prefer gentle, repeating animations (e.g., breathing, soft swaying). See Motion guidelines.

### File Provider App Extension

For sharing files with other apps via a custom interface for importing, exporting, opening, and moving documents.

- **Display only appropriate documents** for the current context (e.g., only PDFs when loaded by a PDF editor). Show metadata like modification dates, sizes, local/remote status.
- **Let people select a destination** when exporting/moving documents unless your app uses a single directory. Allow creating new subdirectories.
- **Avoid a custom top toolbar** — the extension loads in a modal view that already has one.

## macOS

### Custom File Management

Use the default file browser unless you have an important reason to customize.

- **Custom file-opening interface:** Consider "open recent" actions, filtering criteria, and multi-document selection. Customize the Open button title to reflect the task (e.g., "Insert").
- **Save interface:** Let people change file name, format, and location. Default title is "Untitled". Default to a logical save location. Provide format selection if multiple formats are supported.
- **Extend the Save dialog** with a custom accessory view for useful settings (e.g., Mail's "include attachments" option).

### Finder Sync Extensions

For apps that sync local and remote files. Can:
- Display badges for sync status
- Provide custom contextual menu items (favoriting, password-protection)
- Provide custom toolbar buttons (initiating sync)

### Autosave Considerations (macOS)

- **When autosaving is off** (user preference "Ask to keep changes when closing documents"):
  - Show unsaved changes with a dot on the window's close button and next to the document name in the Window menu
  - Present a save dialog when closing, quitting, logging out, or restarting
- **When autosaving is on:** Do NOT show the dot (it implies user action is needed)
- Regardless of autosave status, you can append "Edited" to the document title in the title bar, but remove it as soon as autosave occurs or the user saves explicitly.