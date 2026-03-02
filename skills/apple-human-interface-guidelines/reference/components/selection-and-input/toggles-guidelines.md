# Toggles

Guidelines for toggles (switches, checkboxes, radio buttons) across Apple platforms.

## Best Practices

- **Use a toggle for two opposing values that affect state**, not for choosing from a list (use a pop-up button instead).
- **Clearly identify what the toggle affects.** Surrounding context usually suffices. For buttons acting as toggles, use an interface icon and change background appearance based on state.
- **Make visual state differences obvious.** Use color fill, background shape, or inner details (checkmark, dot) — don't rely solely on color differences for accessibility.

## iOS / iPadOS

- **Use switch toggle style only in list rows.** The row content provides context; no separate label needed.
- **Default green switch color is preferred.** Only change to accent color if necessary; ensure sufficient contrast with the off state.
- **Outside lists, use a button that behaves like a toggle, not a switch.** Example: Phone app's filter button uses a blue highlight when active, removes it when inactive.
- **Avoid labels on toggle buttons.** The icon plus background appearance changes should communicate purpose.

## macOS

Supports switch, checkbox, and radio button styles.

**General:** Use switches, checkboxes, and radio buttons in the window body — never in toolbars or status bars.

### Switches

- **Prefer a switch for settings you want to emphasize** — it has more visual weight than a checkbox. Good for controlling groups of settings.
- **Use mini switches in grouped forms** for consistent row height. Use regular switches for primary settings and mini switches for subordinate ones.
- **Don't replace existing checkboxes with switches.**

### Checkboxes

Small square button: empty (off), checkmark (on), dash (mixed). Typically includes a trailing title; in editable checklists, can appear without a title.

- **Use checkboxes (not switches) for hierarchies of settings.** Alignment and indentation communicate grouping and dependencies.
- **Consider radio buttons for more than two mutually exclusive options.**
- **Use a label to introduce a group of checkboxes** if their relationship isn't clear; align label baseline with first checkbox.
- **Show mixed state accurately** when a parent checkbox controls subordinate checkboxes with different states (e.g., a "text styles" parent with bold/italic/underline children).

### Radio Buttons

Small circular button with label, displayed in groups of 2–5 for mutually exclusive choices. States: selected (filled circle) or deselected (empty circle).

- **Use radio buttons for mutually exclusive options.** Use checkboxes for multiple selections.
- **Limit to ~5 options.** For more, use a pop-up button.
- **For a single on/off setting, prefer a checkbox.** Use a pair of radio buttons only when a single checkbox doesn't clearly communicate both states.
- **Use consistent horizontal spacing** based on the longest label width.

## Developer References

| Component | Framework | API |
|-----------|-----------|-----|
| Toggle | SwiftUI | `Toggle`, `ToggleStyle` |
| Switch | UIKit | `UISwitch` |
| Toggle Button | UIKit | `UIButton.changesSelectionAsPrimaryAction` |
| Toggle | AppKit | `NSButton.ButtonType.toggle` |
| Switch | AppKit | `NSSwitch` |
| Mixed state | AppKit | `NSButton.allowsMixedState` |
| Grouped forms | SwiftUI | `GroupedFormStyle`, `ControlSize` |