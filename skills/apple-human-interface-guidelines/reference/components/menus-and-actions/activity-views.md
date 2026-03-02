# Activity Views (Share Sheets)

Guidelines for presenting sharing and action tasks via activity views on iOS, iPadOS, and visionOS. Not supported in macOS, tvOS, or watchOS.

An activity view presents tasks people can perform in the current context — sharing (messaging, social media) and actions (Copy, Print). It appears as a sheet or popover depending on device/orientation.

## Best Practices

- **Don't duplicate existing system actions.** If you need similar functionality, give it a custom title (e.g., "Print Transaction" instead of duplicating Print).
- **Use SF Symbols for custom activity icons.** If creating a custom icon, center it in ~70×70 px area.
- **Write succinct, descriptive action titles.** Use a single verb or brief verb phrase. Avoid company/product names in action titles. (Share extensions display company name below the icon automatically.)
- **Filter activities by context.** Exclude system tasks that aren't applicable (e.g., exclude Print if printing doesn't apply). Show only relevant custom tasks.
- **Use the Share button to trigger activity views.** Don't provide alternative mechanisms for the same sharing functionality.

## Share and Action Extensions

Share extensions let people share content with apps/services. Action extensions let people initiate content-specific tasks (bookmark, copy link, edit image, translate text) without leaving context.

### Platform Presentation

| Platform | Share Extensions | Action Extensions |
|----------|-----------------|-------------------|
| iOS/iPadOS | Displayed in share sheet via Action button | Displayed in share sheet via Action button |
| macOS | Share button in toolbar or Share in context menu | Hover over content, toolbar button, or Finder quick action |

### Extension Guidelines

- **Prefer the system composition view for share extensions** for a consistent experience.
- **Include your app name in action extension UI** and use elements of your app's interface to show the relationship.
- **Streamline interaction** — let people complete tasks in just a few steps (e.g., single tap to post).
- **Avoid placing modal views above your extension.** Alerts are acceptable; additional modal views are not.
- **Use appropriate imagery:** Share extensions auto-use your app icon. Action extensions should use an SF Symbol or custom icon that identifies the task.
- **Handle lengthy operations in your main app.** The activity view dismisses immediately after the user completes the extension task. Continue time-consuming work in the background and let users check status in the main app. Use notifications only for errors, not completion.