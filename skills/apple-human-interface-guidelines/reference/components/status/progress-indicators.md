# Progress Indicators

Guidelines for using progress indicators across Apple platforms to communicate ongoing operations.

## Types

- **Determinate** — for tasks with well-defined duration (e.g., file conversion). Shows progress by filling a track.
  - **Progress bar**: linear track filling leading to trailing
  - **Circular progress indicator**: track filling clockwise
- **Indeterminate** (activity indicator / spinner) — for unquantifiable tasks (e.g., loading complex data). Uses animated spinning image. macOS also supports an indeterminate progress bar.

SwiftUI: `ProgressView` · UIKit: `UIProgressView`, `UIActivityIndicatorView` · AppKit: `NSProgressIndicator`

## Best Practices

- **Prefer determinate progress indicators** — they help users estimate wait time and decide whether to do something else.
- **Be accurate when reporting advancement** — avoid showing 90% in 5 seconds then 10% in 5 minutes. Even out the pace to build confidence.
- **Keep indicators moving** — a stationary indicator suggests a stalled/frozen app. If a process stalls, provide feedback explaining the problem.
- **Switch from indeterminate to determinate** when possible — once duration becomes known, switch to a determinate bar.
- **Don't switch from circular to bar style** — transitioning between shapes/sizes disrupts the interface.
- **Display descriptions only if helpful** — be accurate and succinct. Avoid vague terms like "loading" or "authenticating."
- **Use a consistent location** for progress indicators across platforms and apps.
- **Let people halt processing** when feasible — use a Cancel button if interruption has no side effects. Add a Pause button alongside Cancel if interruption might cause data loss.
- **Warn about negative consequences of halting** — show an alert with options to confirm cancellation or resume.

## Platform Considerations

### iOS / iPadOS

#### Refresh Content Controls

A refresh control (`UIRefreshControl`) is a specialized activity indicator hidden by default, revealed when dragging down a view.

- **Perform automatic content updates** — don't make users responsible for every update; refresh data periodically.
- **Supply a short title only if it adds value** — don't explain how to refresh. Instead, provide useful info (e.g., last update time).

### macOS

- **Prefer a spinner for background operations or constrained spaces** — spinners are small and unobtrusive, useful for async tasks (e.g., retrieving messages) or within small areas (text fields, next to buttons).
- **Avoid labeling a spinner** — since users typically initiate the process, a label is usually unnecessary.
- macOS supports both bar and circular indeterminate indicators.

### watchOS

- Default display: white over scene background color.
- Customize color via tint color.
- Supports progress bar, circular progress indicator, and activity indicator.

### tvOS / visionOS

No additional considerations.