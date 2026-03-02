# Panels (macOS)

Guidelines for using panels — floating windows that provide supplementary controls, options, or information related to the active window or current selection. macOS only.

## Best Practices

- **Use panels for quick access** to important controls or information related to current content (e.g., controls affecting the selected item in the active document).
- **Consider panels for inspector functionality** — displays details of the currently selected item, auto-updating when selection changes. For *Info* windows (static content regardless of selection), use a regular window. Also consider a split view pane for inspectors.
- **Prefer simple adjustment controls** — use sliders and steppers over text fields or item selectors to minimize multi-step interactions.
- **Write a brief noun title** using title-style capitalization (e.g., "Fonts", "Colors", "Inspector") so people can recognize the panel onscreen.
- **Show/hide panels appropriately** — bring all open panels to front when app becomes active; hide all panels when app is inactive.
- **Don't include panels in the Window menu's documents list** — commands to show/hide panels are fine in the Window menu, but panels aren't documents.
- **Avoid making the minimize button available** — panels display only when needed and disappear when app is inactive.
- **Refer to panels by title** — in menus, use the title without "panel" (e.g., "Show Fonts"). In help docs, use the title alone or append "window" for clarity (e.g., "Fonts window").

## HUD-Style Panels

Darker, translucent panels for media-oriented or immersive apps (e.g., media editing, full-screen slideshows).

**Prefer standard panels.** Only use a HUD when:
- In a media-oriented app (movies, photos, slides)
- A standard panel would obscure essential content
- You don't need to include controls (most system controls don't match HUD appearance; disclosure triangles are an exception)

**HUD guidelines:**
- Maintain one panel style when switching modes (e.g., keep HUD style when exiting full-screen)
- Use color sparingly — small amounts of high-contrast color only
- Keep HUDs small — don't let them obscure the content they adjust or compete for attention

## Platform Support

macOS only. Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS. On other platforms, consider modal views for supplementary content.

## Developer Reference

- [`NSPanel`](https://developer.apple.com/documentation/AppKit/NSPanel) — AppKit
- [`hudWindow`](https://developer.apple.com/documentation/AppKit/NSWindow/StyleMask-swift.struct/hudWindow) — AppKit