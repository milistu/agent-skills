# Color Guidelines

Guidelines for using color effectively across Apple platforms, including system colors, Liquid Glass, accessibility, and color management.

## Best Practices

- **Avoid using the same color to mean different things.** Use color consistently — e.g., don't use your brand color for both interactive buttons and non-interactive text.
- **Support light, dark, and increased contrast contexts.** Use system colors (which have built-in variants) or supply custom light/dark variants plus increased contrast options for each. Even single-appearance apps should provide both light and dark colors for Liquid Glass adaptivity.
- **Test under varied lighting conditions.** Colors look darker/muted in bright surroundings and brighter/saturated in dark environments. In visionOS, surrounding physical objects affect color perception.
- **Test on different devices.** True Tone displays, different TV brands, and different color profiles (P3 vs sRGB) all affect appearance.
- **Consider how artwork and translucency affect nearby colors.** Adjust colors based on content context (e.g., map vs satellite mode).
- **Prefer system-provided color pickers** (`ColorPicker` in SwiftUI) when letting users choose colors.

## Inclusive Color

- **Don't rely solely on color to differentiate objects, indicate interactivity, or communicate essential info.** Provide text labels or glyph shapes as alternatives for color-blind users.
- **Ensure sufficient contrast** so icons and text don't blend with backgrounds.
- **Consider cultural meanings of color.** Red means danger in some cultures but is positive in others (e.g., green = positive trend in English Stocks app; red = positive trend in Chinese Stocks app).

## System Colors

- **Don't hard-code system color values.** Use APIs like `Color` (SwiftUI), `UIColor` (UIKit), `NSColor` (AppKit). Actual values may change between releases.
- **Don't redefine semantic meanings of dynamic system colors.** Use them as intended (e.g., don't use `separator` as a text color).
- Dynamic system colors are semantically defined by purpose (labels, links, separators, backgrounds at hierarchy levels), not appearance.

## Liquid Glass Color

By default, Liquid Glass has no inherent color — it takes on colors from content behind it. You can apply color to some Liquid Glass elements (colored/stained glass effect).

- **Apply color sparingly to Liquid Glass material and to symbols/text on it.** Reserve for elements needing emphasis (status indicators, primary actions).
- **For primary actions, apply color to the background** (not symbols/text). E.g., the system applies accent color to the background of prominent buttons like Done.
- **Don't add colored backgrounds to multiple controls** — only the primary action.
- **Avoid similar colors in control labels over colorful backgrounds.** Prefer monochromatic toolbar/tab bar appearance, or choose an accent color with sufficient differentiation.
- **Ensure interface maintains sufficient contrast** — avoid overlapping similar colors in content layer and controls. Default/resting state should maintain clear legibility.

## Color Management

- **Apply color profiles to images.** sRGB produces accurate colors on most displays.
- **Use wide color (Display P3)** for richer, more saturated colors on compatible displays. Use P3 profile at 16 bits per pixel per channel; export as PNG.
- **Provide color space–specific variations if needed.** Similar P3 colors may be indistinguishable on sRGB displays; P3 gradients can appear clipped on sRGB. Use Xcode asset catalogs for per-color-space versions.

## Platform-Specific Guidance

### iOS / iPadOS

Two sets of dynamic background colors:
- **System**: `systemBackground`, `secondarySystemBackground`, `tertiarySystemBackground`
- **Grouped** (for grouped table views): `systemGroupedBackground`, `secondarySystemGroupedBackground`, `tertiarySystemGroupedBackground`

Hierarchy: Primary → overall view; Secondary → grouping within overall view; Tertiary → grouping within secondary elements.

**Foreground dynamic colors:**

| Color | Use | UIKit API |
|---|---|---|
| Label | Primary content text | `label` |
| Secondary label | Secondary content text | `secondaryLabel` |
| Tertiary label | Tertiary content text | `tertiaryLabel` |
| Quaternary label | Quaternary content text | `quaternaryLabel` |
| Placeholder text | Placeholder in controls/text views | `placeholderText` |
| Separator | Separator allowing underlying content visibility | `separator` |
| Opaque separator | Separator blocking underlying content | `opaqueSeparator` |
| Link | Link text | `link` |

**Gray colors (iOS/iPadOS):**

| Name | UIKit API | Light | Dark | High Contrast Light | High Contrast Dark |
|---|---|---|---|---|---|
| Gray | `systemGray` | 142,142,147 | 142,142,147 | 108,108,112 | 174,174,178 |
| Gray 2 | `systemGray2` | 174,174,178 | 99,99,102 | 142,142,147 | 124,124,128 |
| Gray 3 | `systemGray3` | 199,199,204 | 72,72,74 | 174,174,178 | 84,84,86 |
| Gray 4 | `systemGray4` | 209,209,214 | 58,58,60 | 188,188,192 | 68,68,70 |
| Gray 5 | `systemGray5` | 229,229,234 | 44,44,46 | 216,216,220 | 54,54,56 |
| Gray 6 | `systemGray6` | 242,242,247 | 28,28,30 | 235,235,240 | 36,36,38 |

SwiftUI equivalent of `systemGray` is `Color.gray`.

### macOS

Key dynamic system colors (AppKit APIs):

| Color | Use | API |
|---|---|---|
| Label color | Primary label text | `labelColor` |
| Secondary label color | Subheadings, additional info | `secondaryLabelColor` |
| Tertiary label color | Lesser importance than secondary | `tertiaryLabelColor` |
| Quaternary label color | Watermark text | `quaternaryLabelColor` |
| Control accent | User's selected accent color | `controlAccentColor` |
| Control background | Large elements (browser, table) | `controlBackgroundColor` |
| Control color | Control surface | `controlColor` |
| Control text color | Available control text | `controlTextColor` |
| Unavailable control text | Disabled control text | `disabledControlTextColor` |
| Link color | Links | `linkColor` |
| Placeholder text color | Placeholder strings | `placeholderTextColor` |
| Separator color | Section separators | `separatorColor` |
| Selected content bg | Selected content in key window | `selectedContentBackgroundColor` |
| Selected control color | Selected control surface | `selectedControlColor` |
| Selected text bg | Selected text background | `selectedTextBackgroundColor` |
| Window background | Window background | `windowBackgroundColor` |
| Grid color | Table gridlines | `gridColor` |
| Alternating content bg | Alternating rows/columns | `alternatingContentBackgroundColors` |

**Accent colors (macOS 11+):** Specify an accent color for buttons, selection highlighting, sidebar icons. System applies it when user's accent setting is "multicolor." If user picks another color, it overrides yours (except fixed-color sidebar icons).

### tvOS

- Choose a limited color palette coordinating with app logo.
- **Don't use only color to indicate focus** — use subtle scaling and responsive animation.

### visionOS

- **Use color sparingly, especially on glass.** Physical surroundings show through glass material and affect legibility.
- **Prefer color in bold text and large areas.** Color in lightweight text or small areas reduces legibility.
- **Keep brightness balanced in immersive experiences.** Avoid bright objects on very dark backgrounds, especially if flashing/moving.
- visionOS system colors use the default dark color values.

### watchOS

- Use background color to communicate info (e.g., Activity ring colors), not purely as decoration.
- Avoid full-screen background color in views onscreen for long periods (workouts, audio).
- Support tinted mode for graphic complications — system may apply a single color based on wearer's selection.

## System Color Specifications (RGB)

| Name | SwiftUI | Light | Dark | HC Light | HC Dark |
|---|---|---|---|---|---|
| Red | `.red` | 255,56,60 | 255,66,69 | 233,21,45 | 255,97,101 |
| Orange | `.orange` | 255,141,40 | 255,146,48 | 197,83,0 | 255,160,86 |
| Yellow | `.yellow` | 255,204,0 | 255,214,0 | 161,106,0 | 254,223,67 |
| Green | `.green` | 52,199,89 | 48,209,88 | 0,137,50 | 74,217,104 |
| Mint | `.mint` | 0,200,179 | 0,218,195 | 0,133,117 | 84,223,203 |
| Teal | `.teal` | 0,195,208 | 0,210,224 | 0,129,152 | 59,221,236 |
| Cyan | `.cyan` | 0,192,232 | 60,211,254 | 0,126,174 | 109,217,255 |
| Blue | `.blue` | 0,136,255 | 0,145,255 | 30,110,244 | 92,184,255 |
| Indigo | `.indigo` | 97,85,245 | 109,124,255 | 86,74,222 | 167,170,255 |
| Purple | `.purple` | 203,48,224 | 219,52,242 | 176,47,194 | 234,141,255 |
| Pink | `.pink` | 255,45,85 | 255,55,95 | 231,18,77 | 255,138,196 |
| Brown | `.brown` | 172,127,94 | 183,138,102 | 149,109,81 | 219,166,121 |