# Pull-Down Buttons

Guidelines for pull-down buttons — buttons that display a menu of items or actions directly related to the button's purpose. After choosing an item, the menu closes and the app performs the chosen action.

## Best Practices

- **Use for commands/items directly related to the button's action.** Examples:
  - An **Add** button presenting a menu to specify what to add
  - A **Sort** button letting people select a sort attribute
  - A **Back** button letting people choose a specific location to revisit

- **Use a pop-up button (not pull-down) for mutually exclusive choices that aren't commands.**

- **Don't hide all of a view's primary actions in one pull-down button.** Primary actions must be easily discoverable.

- **List a minimum of 3 items** to make the interaction feel worthwhile. For 1–2 items, consider using standalone buttons, toggles, or switches instead. Avoid too many items — it slows people down.

- **Only display a menu title if it adds meaning.** The button content combined with descriptive menu items usually provides sufficient context.

- **For destructive actions:** Use red text and confirm intent via an action sheet (iOS) or popover (iPadOS) before executing.

- **Include icons with menu items only when they add value.** Use SF Symbols for consistent alignment at every scale.

## iOS / iPadOS

- Pull-down menus can also be triggered via gestures (e.g., touch-and-hold on Safari's Tabs button reveals tab-related actions).

- **More button (ellipsis icon):** Use to present secondary items that don't need prominent positions. Weigh the convenience of its compact size against reduced discoverability. People understand More buttons offer additional functionality but can't predict the contents from the ellipsis icon alone.

## Platform Support

- **Supported:** iOS, iPadOS, macOS, visionOS
- **Not supported:** tvOS, watchOS

## Related Components

- [Pop-up buttons](/design/human-interface-guidelines/pop-up-buttons) — for mutually exclusive selections
- [Buttons](/design/human-interface-guidelines/buttons)
- [Menus](/design/human-interface-guidelines/menus)

## Developer References

- `MenuPickerStyle` (SwiftUI)
- `showsMenuAsPrimaryAction` (UIKit)
- `pullsDown` (AppKit)