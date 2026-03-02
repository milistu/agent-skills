# Dark Mode

Guidelines for supporting Dark Mode — a systemwide dark color palette for low-light environments — across iOS, iPadOS, macOS, and tvOS. Not supported in visionOS or watchOS.

## Best Practices

- **Don't offer an app-specific appearance setting.** Respect the systemwide choice; app-specific toggles create extra work and confusion.
- **Ensure your app looks good in both light and dark modes.** Users can set Auto appearance, which switches modes throughout the day while your app runs.
- **Test legibility in both modes**, including with Increase Contrast and Reduce Transparency turned on (separately and together). Dark text on dark backgrounds can become illegible.
- **In rare cases, a dark-only appearance is acceptable** — e.g., immersive media viewing apps (like Stocks) where UI should recede.

## Dark Mode Colors

Dark Mode uses dimmer backgrounds and brighter foregrounds. These are not simple inversions of light mode colors.

- **Use semantic/adaptive colors.** Use system colors like `labelColor`, `controlColor` (macOS), `separator` (iOS/iPadOS) that adapt automatically. For custom colors, add a Color Set asset in Xcode with light and dark variants. Avoid hard-coded color values.
- **Minimum contrast ratio: 4.5:1.** Strive for **7:1** especially for small text, to meet accessibility guidelines.
- **Soften white backgrounds in content images.** Slightly darken images with white backgrounds to prevent glowing in Dark Mode.

## Icons and Images

- **Use SF Symbols wherever possible** — they adapt automatically with dynamic colors and vibrancy.
- **Design separate light/dark interface icons if needed.** Example: a moon icon may need a dark outline on light backgrounds but not on dark; an oil drop icon may need a border on dark backgrounds.
- **Ensure full-color images work in both modes.** Use the same asset if it works in both, otherwise create separate light/dark assets in asset catalogs.

## Text

- **Use system label colors** (primary, secondary, tertiary, quaternary) — they adapt automatically.
- **Use system views for text fields and text views** — they adjust for vibrancy and background automatically.

## Platform-Specific

### iOS, iPadOS

Dark Mode uses two background color sets to convey depth:
- **Base**: dimmer colors for background interfaces (appear to recede)
- **Elevated**: brighter colors for foreground interfaces (appear to advance)

**Prefer system background colors.** Background color automatically shifts from base to elevated for foreground elements (popovers, modal sheets, multitasking). Custom backgrounds can break these visual distinctions.

### macOS

**Desktop tinting**: When users choose the graphite accent color, window backgrounds pick up color from the desktop picture.

- **Add transparency to custom component backgrounds when appropriate** — only for components with a visible background/bezel in a neutral (non-colored) state. This enables desktop tinting harmony. Don't add transparency when the component uses color, as it would cause color fluctuation when the desktop picture changes.