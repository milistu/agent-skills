# Context Menus

Guidelines for designing context menus that provide quick access to relevant functionality without cluttering the interface.

## Activation Methods
- **visionOS, iOS, iPadOS**: Touch/pinch and hold gesture
- **macOS, iPadOS**: Control-click or secondary click on trackpad

## Best Practices

- **Prioritize relevancy** — Include only commands people are most likely to need in their current context, not advanced or rarely used items.
- **Aim for a small number of items** — Long menus are hard to scan and scroll.
- **Support context menus consistently** — If you provide them for items in some places, provide them everywhere similar items appear.
- **Always make context menu items available in the main interface too** — Context menus are shortcuts, not the only way to access functionality.
- **Keep submenus to one level** — Give submenus intuitive titles that predict their contents.
- **Hide unavailable items, don't dim them** — Unlike regular menus, context menus should only show relevant actions. Exception in macOS: Cut, Copy, Paste may appear dimmed.
- **Place most-used items where people encounter them first** — The menu may open above or below content; consider reversing item order based on menu position.
- **Don't show keyboard shortcuts** — Context menus already are shortcuts; displaying keyboard shortcuts is redundant.
- **Use separators sparingly** — No more than about three groups in a context menu.
- **In iOS, iPadOS, visionOS: place destructive items at the end** — Use the `destructive` attribute to display them in red.

## Content & Labels

- Context menus seldom need a title. Include one only if it clarifies the menu's effect (e.g., showing the number of selected items).
- Each item needs a short, clear label describing what it does.
- Use familiar system icons for common actions (Copy, Share, Delete).

## Platform-Specific Guidelines

### iOS & iPadOS
- Provide either a context menu **or** an edit menu for an item, never both.
- In iPadOS, consider using context menus to let people create new objects (e.g., long press in empty area to create a folder).
- Context menus can display a **preview** of content near the command list. People can tap the preview to open it or drag it elsewhere.
- Use a graphical preview that clarifies the target of commands (e.g., condensed version of actual content).
- Adjust the preview's clipping path to match the preview shape so contours (e.g., rounded corners) don't visually change during animation. See `UIContextMenuInteractionDelegate`.

### macOS
- Context menus are sometimes called *contextual* menus.

### visionOS
- Prefer context menus over panels or inspector windows for frequently used functionality to keep the space uncluttered.
- Avoid letting a context menu's height exceed the window height — tall menus may obscure system-provided window controls.
- Consider the app's complexity: specialist apps may warrant more items; simple apps benefit from short menus.

## Developer APIs
- SwiftUI: `contextMenu(menuItems:)`
- UIKit: `UIContextMenuInteraction`
- AppKit: `popUpContextMenu(_:with:for:)`