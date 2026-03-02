# Popovers

A popover is a transient view that appears above other content when people click or tap a control or interactive area.

## Best Practices

- **Use for small amounts of information or functionality.** Limit content to a few related tasks. The popover disappears after interaction.
- **Consider popovers for temporary content** instead of space-consuming sidebars/panels.
- **Position appropriately.** Arrow should point directly to the element that revealed it. Don't cover the revealing element or essential content.
- **Use a Close button only for confirmation/guidance** (e.g., saving vs. discarding changes). Otherwise, popovers close when clicking/tapping outside bounds or selecting an item.
- **Always save work when auto-closing a nonmodal popover.** Only discard work on explicit Cancel.
- **Show one popover at a time.** No cascading or hierarchies. Close the open one before showing a new one.
- **Don't show another view over a popover** — only alerts can appear on top.
- **Let people close one and open another with a single tap/click** when multiple bar buttons each open popovers.
- **Size appropriately.** Only big enough to display contents and point to origin. System may adjust size to fit.
- **Animate size changes** to avoid the impression a new popover replaced the old one.
- **Don't use the word "popover" in help documentation.** Refer to specific tasks/selections instead.
- **Don't use popovers for warnings.** Use alerts instead — popovers can be missed or accidentally closed.

## Platform Considerations

> Not supported in tvOS or watchOS. No additional considerations for visionOS.

### iOS, iPadOS

- **Avoid popovers in compact size classes.** Use full-screen modal views (sheets) instead. Reserve popovers for wide/regular size class layouts.

### macOS

- Popovers can be **detachable** — people drag them to become a separate panel that persists while interacting with other content.
- **Consider letting people detach a popover** when they may want to view other information simultaneously.
- **Make minimal appearance changes to a detached popover** so it looks similar to the original, maintaining context.

## Related Components

- Sheets, Action Sheets, Alerts, Modality (see respective guidelines)

## Developer References

- SwiftUI: `popover(isPresented:attachmentAnchor:arrowEdge:content:)`
- UIKit: `UIPopoverPresentationController`
- AppKit: `NSPopover`