# Toolbars

Guidelines for designing toolbars that provide convenient access to frequently used commands, controls, navigation, and search across Apple platforms.

## Best Practices

- **Avoid overcrowding.** Define which items move to the overflow menu as the toolbar becomes narrower. The system automatically adds an overflow menu in macOS/iPadOS when items no longer fit — don't add one manually.
- **Add a More menu for additional actions.** Prioritize less important actions for the More menu. Only add it if truly needed.
- **In iPadOS/macOS, consider letting people customize the toolbar.** Especially useful for apps with many items, advanced functionality, or long usage sessions.
- **Reduce toolbar backgrounds and tinted controls.** Use the content layer to inform color/appearance, and use `ScrollEdgeEffectStyle` when necessary to distinguish toolbar from content.
- **Avoid similar colors for toolbar item labels and content backgrounds.** If content is colorful, prefer default monochromatic toolbar appearance.
- **Use standard components.** Default buttons, text fields, headers, and footers have corner radii concentric with bar corners. Custom components should match.
- **Consider temporarily hiding toolbars** for distraction-free experiences, with reliable ways to restore them.

## Titles

- **Provide a useful title for each window** to help confirm location during navigation.
- **Don't title windows with your app name** — it doesn't convey hierarchy information.
- **Write concise titles** — aim for a word or short phrase, under 15 characters.

## Navigation

A toolbar with navigation controls appears at the top of a window. In iOS, a navigation-specific toolbar is sometimes called a navigation bar.

- **Use standard Back and Close buttons.** Prefer standard symbols; don't use text labels saying "Back" or "Close". Custom versions must look and behave consistently throughout your app.

## Actions

- **Prioritize commands people use most frequently** or that map to the most important objects.
- **Make each control's meaning clear.** Prefer simple, recognizable symbols over text, except for actions like "Edit" not well-represented by symbols.
- **Prefer system-provided symbols without borders.** Outlined circle symbols are unnecessary — the section provides a visible container, and the system handles hover/selection states automatically.
- **Use `.prominent` style for key actions** (Done, Submit). This tints and separates the action as a focal point. Only specify one, placed on the trailing side.

## Item Groupings

Three positioning areas:

| Area | Content | Behavior |
|---|---|---|
| **Leading edge** | Back button, sidebar toggle, view title, document menu | Not customizable; always available |
| **Center area** | Common controls, optional view title | Customizable (macOS/iPadOS); auto-collapses to overflow menu |
| **Trailing edge** | Important items, inspector buttons, search field, More menu, primary action (e.g., Done) | Remains visible at all window sizes |

### Grouping Guidelines

- **Group items logically by function and frequency of use.**
- **Group navigation controls and critical actions (Done, Close, Save) in dedicated, visually distinct sections.**
- **Keep consistent groupings across platforms.**
- **Minimize the number of groups** — aim for a maximum of three.
- **Keep text-labeled actions separate from symbol actions** to avoid confusion. Use `UIBarButtonItem.SystemItem.fixedSpace` for separation between multiple text-labeled buttons.

## Platform Considerations

### iOS

- **Prioritize only the most important items** due to limited space. Use a More menu for additional items.
- **Use large titles** for orientation. They transition to standard size on scroll. See `prefersLargeTitles`.

### iPadOS

- **Consider combining a toolbar with a tab bar** in the same horizontal space at the top of the view.

### macOS

Toolbar resides in the frame at the top of a window, below or integrated with the title bar. Window titles can display inline with controls; toolbar items don't include a bezel.

- **Make every toolbar item available as a menu bar command.** The toolbar can be customized or hidden, so it can't be the sole location for a command.

### visionOS

The toolbar appears along the bottom edge of a window, above window-management controls, slightly forward on the z-axis. Uses variable blur for legibility during scrolling.

- **Prefer system-provided toolbar** — optimized for eye and hand input, correctly positioned.
- **Avoid vertical toolbars** — tab bars are vertical in visionOS, so a vertical toolbar would cause confusion.
- **Prevent windows from resizing below toolbar width** — visionOS has no menu bar, so toolbar must provide reliable access to essential controls.
- **Offer contextually relevant toolbar controls during modal states.** Reinstate standard controls when exiting modal state.
- **Avoid pull-down menus in toolbars** — they may obscure window controls below the bottom edge.

### watchOS

Toolbar buttons can be placed in top corners or along the bottom. Top buttons remain visible above scrolling content.

- Scrolling toolbar buttons remain hidden until revealed by scrolling up.
- **Use scrolling toolbar buttons for important actions that aren't primary app functions** (e.g., Mail's New Message in the Inbox view).
- Placement options: `topBarLeading`, `topBarTrailing`, `bottomBar`, `primaryAction`.