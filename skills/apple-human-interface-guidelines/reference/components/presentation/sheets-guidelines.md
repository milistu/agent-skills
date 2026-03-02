# Sheets

Guidelines for using sheets — scoped modal or nonmodal views closely related to the current context.

## Overview

- By default, sheets are **modal**, preventing interaction with the parent view until dismissed.
- In macOS, visionOS, and watchOS, sheets are always modal.
- In iOS/iPadOS, sheets can be **nonmodal**, letting people interact with the parent view while the sheet is visible (e.g., Notes formatting sheet).

## Best Practices

- **Use sheets for simple content or tasks.** The partially visible parent view helps retain context.
- **For complex/prolonged flows, use alternatives:**
  - iOS/iPadOS: full-screen modal (`UIModalPresentationStyle.fullScreen`)
  - macOS: new window or full-screen mode
  - visionOS: Full Space for immersive experiences
- **Display only one sheet at a time.** If a second sheet is needed, close the first before showing it. Optionally re-display the first after the second is dismissed.
- **Use nonmodal views for supplementary items affecting the parent task:**
  - visionOS: split view
  - macOS: panel
  - iOS/iPadOS: nonmodal sheet

## iOS / iPadOS

### Detents

- Sheets resize according to **detents** — specific resting heights.
- System-defined detents: **large** (fully expanded) and **medium** (≈half height).
- Sheets automatically support large. Adding medium allows both; specifying only medium prevents full expansion.
- Developer guidance: `UISheetPresentationController.detents`

### Medium Detent Usage

- Support medium detent for **progressive disclosure** (e.g., share sheet shows most relevant items at medium height).
- Omit medium detent when content is more useful at full height (e.g., compose sheets in Messages/Mail).

### Grabber

- **Include a grabber** in resizable sheets — lets people drag to resize or tap to cycle detents.
- Also works with VoiceOver for accessibility.
- Developer guidance: `UISheetPresentationController.prefersGrabberVisible`

### Dismissal

- **Support swipe-to-dismiss.** If unsaved changes exist, show an action sheet to confirm.

### Button Placement (iOS/iPadOS)

| Scenario | Done/Dismiss | Cancel |
|---|---|---|
| Single view sheet | Top-right | Top-left |
| Sheet with subviews (navigation) | — | Top-right (to leave room for Back button in top-left) |
| End of navigation flow | Top-right (replaces Cancel) | — |

### iPadOS-Specific

- **Prefer page or form sheet presentation styles** — centers content on dimmed background at default size.
- Developer guidance: `UIModalPresentationStyle`

## macOS

- Sheet is a card-like rounded view floating on a dimmed parent window.
- **Present in a reasonable default size.** Support resizing if content benefits from it.
- **Let people interact with other app windows** without dismissing the sheet. Bring the parent window (and its modeless panels) to front when sheet opens.
- **Position dismiss buttons (Done, OK, Cancel) at the bottom of the sheet, in the trailing corner.**
- **Use a panel instead of a sheet** if people need to repeatedly provide input and observe results (e.g., find and replace).

## visionOS

- Sheet floats in front of its parent window, dimming it.
- **Avoid sheets emerging from the bottom edge** — prefer centering in the field of view.
- **Use a default size that preserves context** — don't cover most/all of the window. Consider letting people resize.

## watchOS

- Sheet is a **full-screen** semitransparent view that slides over current content with a blurred/desaturated background material.
- **Use a sheet only for tasks requiring a custom title or custom content presentation.** For important info or choices, prefer alerts or action sheets.
- **Keep interactions brief and occasional** — sheets are temporary interruptions, not navigation tools.
- Default dismiss control: round **Cancel** button (upper left). Use **Done** button if sheet only presents info without enabling a task.
- **Prefer SF Symbols** for custom dismiss labels. Avoid text that looks like a page title or Back button, which would confuse users about how to dismiss.

## Developer References

| Framework | API |
|---|---|
| SwiftUI | `sheet(item:onDismiss:content:)` |
| UIKit | `UISheetPresentationController` |
| AppKit | `NSViewController.presentAsSheet(_:)` |

## Related Components

- [Modality](/design/human-interface-guidelines/modality)
- [Action Sheets](/design/human-interface-guidelines/action-sheets)
- [Popovers](/design/human-interface-guidelines/popovers)
- [Panels](/design/human-interface-guidelines/panels)