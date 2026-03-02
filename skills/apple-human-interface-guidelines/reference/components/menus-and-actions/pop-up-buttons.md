# Pop-up Buttons

A pop-up button displays a menu of mutually exclusive options. After selection, the menu closes and the button updates to indicate the current selection.

## Best Practices

- **Use for flat lists of mutually exclusive options or states.** Use a pull-down button instead if you need to:
  - Offer a list of actions
  - Let people select multiple items
  - Include a submenu

- **Provide a useful default selection.** Make the default an item most people are likely to want.

- **Help people predict options without opening the menu.** Use an introductory label or a button label that describes the button's effect, giving context to the options.

- **Use when space is limited** and you don't need to display all options all the time.

- **Include a Custom option if needed** to provide additional items useful in some situations, avoiding interface clutter. You can display explanatory text below the list to help people understand how options work.

## Platform Considerations

Supported on iOS, iPadOS, macOS, and visionOS. **Not supported on tvOS or watchOS.**

### iPadOS

- **Within a popover or modal view, prefer a pop-up button over a disclosure indicator** to present multiple options for a list item. This lets people quickly choose without navigating to a detail view. Best for fairly small, well-defined sets of options that work well in a menu.

## Related Components

- Pull-down buttons
- Buttons
- Menus

## Developer References

| Framework | API |
|-----------|-----|
| SwiftUI | `MenuPickerStyle` |
| UIKit | `UIButton.changesSelectionAsPrimaryAction` |
| AppKit | `NSPopUpButton` |