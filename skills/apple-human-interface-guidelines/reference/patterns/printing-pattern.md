# Printing Pattern

Guidelines for integrating system-provided print functionality in iOS, iPadOS, macOS, and visionOS apps.

## Best Practices

- **Make printing discoverable:** Place print actions in standard system locations:
  - macOS: Include a Print item in the File menu; optionally add a Print button to the toolbar (consider making it an optional toolbar button people can add via customization)
  - iOS/iPadOS: Add a toolbar button that opens an action sheet

- **Present printing only when possible:** If nothing is printable or no printers are available:
  - macOS: Dim the Print item in the File menu
  - iOS/iPadOS: Remove the Print action from the action sheet
  - Custom print buttons: Dim or hide when printing isn't possible

- **Present relevant printing options:** Use the system-provided view to offer options like page range, multiple copies, or double-sided printing when the printer supports them.

## Platform Support

- **Supported:** iOS, iPadOS, macOS, visionOS
- **Not supported:** tvOS, watchOS

## macOS-Specific Guidelines

- **Custom print panel categories:** If your app offers print options not provided by the system, create a custom category in the print panel. Name it uniquely (e.g., your app name). Example: Keynote offers options for printing presenter notes, slide backgrounds, and skipped slides.

- **Page setup dialog:** If your app supports document-specific page settings (page size, orientation, scaling), consider presenting a page setup dialog. Don't reimplement options the system already provides (e.g., page orientation, reverse order).

- **Make option interdependencies clear:** e.g., if double-sided printing is selected, disable transparency printing.

- **Separate advanced from common features:** Use a disclosure control to hide advanced options until needed. Label them "Advanced Options."

- **Preview setting effects:** Consider updating a thumbnail to show the effect of changing settings (e.g., tone control).

- **Store modified settings with the document:** At minimum, persist print settings until the document is closed.