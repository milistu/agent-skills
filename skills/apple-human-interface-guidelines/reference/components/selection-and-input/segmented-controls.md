# Segmented Controls

A segmented control is a linear set of two or more segments, each functioning as a button. All segments are usually equal in width and can contain text or images, with optional text labels beneath them.

## Selection Modes

- **Single choice**: Only one segment can be selected at a time (e.g., text alignment)
- **Multiple choices** (macOS only): Multiple segments can be selected simultaneously (e.g., bold + italic + underline)
- **Momentary/Action**: Segments perform actions without showing selection state (e.g., Reply, Reply All, Forward). See `isMomentary` / `NSSegmentedControl.SwitchTracking.momentary`

## Best Practices

- Use for closely related choices that affect an object, state, or view
- Use when grouping functions together or clearly showing selection state is important
- **Keep control types consistent** within a single control — don't mix action segments with selection-state segments
- **Limit segments**: Max ~5–7 in wide interfaces, max ~5 on iPhone
- **Keep segment sizes consistent** — equal widths feel balanced; keep icon/title widths consistent too

## Content Guidelines

- **Don't mix text and images** in a single segmented control
- Use similarly-sized content in each segment (equal-width segments look poor with uneven content)
- Use **nouns or noun phrases** for segment labels with **title-style capitalization**
- Text-label segmented controls don't need introductory text

## Platform-Specific Guidance

**Not supported in watchOS.**

### iOS / iPadOS
- Use to switch between closely related subviews (e.g., Calendar's New Event vs New Reminder)
- For switching between completely separate app sections, use a **tab bar** instead

### macOS
- Add introductory text or per-segment labels to clarify purpose when using symbols/icons
- Provide tooltips for each segment
- Use a **tab view** (not segmented control) for view switching in the main window area
- Segmented controls are appropriate for view switching in toolbars or inspector panes
- Consider supporting **spring loading** (force click with Magic Trackpad)

### tvOS
- Prefer **split views** over segmented controls for content filtering screens
- Avoid placing other focusable elements close to segmented controls — segments become selected on focus (not click), so nearby focusable elements can cause accidental selection

### visionOS
- System automatically displays tooltips with descriptive text when people look at icon-based segmented controls

## Developer References

| Framework | API |
|-----------|-----|
| SwiftUI | `PickerStyle.segmented` |
| UIKit | `UISegmentedControl` |
| AppKit | `NSSegmentedControl` |