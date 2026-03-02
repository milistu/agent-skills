# Typography Guidelines

Comprehensive typography reference for Apple platforms including system fonts, text styles, Dynamic Type sizes, tracking values, and best practices for legibility and hierarchy.

## Default and Minimum Text Sizes by Platform

| Platform | Default size | Minimum size |
| --- | --- | --- |
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

## Legibility Best Practices

- Use font sizes most people can read easily at various viewing distances
- Avoid light font weights (Ultralight, Thin, Light) — prefer Regular, Medium, Semibold, or Bold
- If using thin custom fonts, aim larger than recommended sizes
- Test legibility on each target platform; increase size/contrast or use system fonts if needed

## Conveying Hierarchy

- Adjust font weight, size, and color to emphasize important information
- Minimize the number of typefaces — too many obscure hierarchy and hinder readability
- Prioritize important content when responding to text-size changes (e.g., body text should scale, tab titles may not need to)
- Maintain relative hierarchy and visual distinction at all text sizes

## System Fonts

**San Francisco (SF)**: Sans serif family — SF Pro, SF Compact, SF Arabic, SF Armenian, SF Georgian, SF Hebrew, SF Mono. Rounded variants available.

**New York (NY)**: Serif family designed to work alongside SF.

Both available in variable font format with dynamic optical sizes. Available at [developer.apple.com/fonts](https://developer.apple.com/fonts/).

Weights range from Ultralight to Black. SF also offers Condensed and Expanded widths. SF Symbols use equivalent weights for precise matching.

### Accessing System Fonts in Code

Use `Font.Design` constants — don't embed system fonts:
- `Font.Design.default` — system font (SF) on all platforms
- `Font.Design.serif` — New York font

## Text Styles

Text styles specify font weight, point size, and leading for each Dynamic Type size. They form a typographic hierarchy and support Dynamic Type scaling.

- Use built-in text styles for consistent hierarchy via font size and weight
- Modify with symbolic traits (e.g., bold trait via `bold()` in SwiftUI or `traitBold` in UIKit)
- Adjust leading with `leading(_:)`: loose leading for wide columns/long passages, tight leading for constrained height (avoid tight leading for 3+ lines)

## Custom Fonts

- Ensure custom fonts are legible at various sizes and conditions
- Implement Dynamic Type support and accessibility features (Bold Text, etc.)
- SwiftUI: see `Applying-Custom-Fonts-to-Text`
- Unity games: use [Apple's Unity plug-ins](https://github.com/apple/unityplugins)

## Supporting Dynamic Type

Available on iOS, iPadOS, tvOS, visionOS, and watchOS (not macOS).

- Ensure layout adapts to all font sizes; test with Larger Accessibility Text Sizes enabled
- Scale meaningful interface icons with font size (SF Symbols scale automatically)
- Minimize text truncation at large sizes; use multi-line labels as needed (`numberOfLines`)
- Consider stacked layouts at large sizes to prevent crowding; reduce columns
- Maintain consistent information hierarchy regardless of font size
- Use `isAccessibilityCategory` to detect accessibility size categories

## Platform-Specific Notes

### iOS, iPadOS
System font: SF Pro. NY also available.

### macOS
System font: SF Pro. NY available via Mac Catalyst. **No Dynamic Type support.**

macOS dynamic font variants:

| Variant | API |
| --- | --- |
| Control content | `controlContentFont(ofSize:)` |
| Label | `labelFont(ofSize:)` |
| Menu | `menuFont(ofSize:)` |
| Menu bar | `menuBarFont(ofSize:)` |
| Message | `messageFont(ofSize:)` |
| Palette | `paletteFont(ofSize:)` |
| Title | `titleBarFont(ofSize:)` |
| Tool tips | `toolTipsFont(ofSize:)` |
| Document text | `userFont(ofSize:)` |
| Monospaced document | `userFixedPitchFont(ofSize:)` |
| Bold system | `boldSystemFont(ofSize:)` |
| System | `systemFont(ofSize:)` |

### tvOS
System font: SF Pro. NY also available.

### visionOS
System font: SF Pro. Uses bolder Dynamic Type body/title styles. Introduces Extra Large Title 1 and Extra Large Title 2.

- **Prefer 2D text** — 3D text is harder to read
- Test legibility at different scales
- Maximize contrast between text and container background (default: white text on system background material)
- For text without background, consider bold; avoid shadows
- Use **billboarding** for text in 3D space — rotate text around y-axis to always face the viewer

### watchOS
System font: SF Compact. NY also available. Complications use SF Compact Rounded.

## Specifications

Emphasized variants use symbolic traits (`bold()` in SwiftUI, `traitBold` in UIKit). Emphasized weights can be Medium, Semibold, Bold, or Heavy.

### iOS/iPadOS Dynamic Type Sizes

#### Large (Default)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 34 | 41 | Bold |
| Title 1 | Regular | 28 | 34 | Bold |
| Title 2 | Regular | 22 | 28 | Bold |
| Title 3 | Regular | 20 | 25 | Semibold |
| Headline | Semibold | 17 | 22 | Semibold |
| Body | Regular | 17 | 22 | Semibold |
| Callout | Regular | 16 | 21 | Semibold |
| Subhead | Regular | 15 | 20 | Semibold |
| Footnote | Regular | 13 | 18 | Semibold |
| Caption 1 | Regular | 12 | 16 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

#### xSmall

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 31 | 38 | Bold |
| Title 1 | Regular | 25 | 31 | Bold |
| Title 2 | Regular | 19 | 24 | Bold |
| Title 3 | Regular | 17 | 22 | Semibold |
| Headline | Semibold | 14 | 19 | Semibold |
| Body | Regular | 14 | 19 | Semibold |
| Callout | Regular | 13 | 18 | Semibold |
| Subhead | Regular | 12 | 16 | Semibold |
| Footnote | Regular | 12 | 16 | Semibold |
| Caption 1 | Regular | 11 | 13 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

#### Small

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 32 | 39 | Bold |
| Title 1 | Regular | 26 | 32 | Bold |
| Title 2 | Regular | 20 | 25 | Bold |
| Title 3 | Regular | 18 | 23 | Semibold |
| Headline | Semibold | 15 | 20 | Semibold |
| Body | Regular | 15 | 20 | Semibold |
| Callout | Regular | 14 | 19 | Semibold |
| Subhead | Regular | 13 | 18 | Semibold |
| Footnote | Regular | 12 | 16 | Semibold |
| Caption 1 | Regular | 11 | 13 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

#### Medium

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 33 | 40 | Bold |
| Title 1 | Regular | 27 | 33 | Bold |
| Title 2 | Regular | 21 | 26 | Bold |
| Title 3 | Regular | 19 | 24 | Semibold |
| Headline | Semibold | 16 | 21 | Semibold |
| Body | Regular | 16 | 21 | Semibold |
| Callout | Regular | 15 | 20 | Semibold |
| Subhead | Regular | 14 | 19 | Semibold |
| Footnote | Regular | 12 | 16 | Semibold |
| Caption 1 | Regular | 11 | 13 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

#### xLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 36 | 43 | Bold |
| Title 1 | Regular | 30 | 37 | Bold |
| Title 2 | Regular | 24 | 30 | Bold |
| Title 3 | Regular | 22 | 28 | Semibold |
| Headline | Semibold | 19 | 24 | Semibold |
| Body | Regular | 19 | 24 | Semibold |
| Callout | Regular | 18 | 23 | Semibold |
| Subhead | Regular | 17 | 22 | Semibold |
| Footnote | Regular | 15 | 20 | Semibold |
| Caption 1 | Regular | 14 | 19 | Semibold |
| Caption 2 | Regular | 13 | 18 | Semibold |

#### xxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 38 | 46 | Bold |
| Title 1 | Regular | 32 | 39 | Bold |
| Title 2 | Regular | 26 | 32 | Bold |
| Title 3 | Regular | 24 | 30 | Semibold |
| Headline | Semibold | 21 | 26 | Semibold |
| Body | Regular | 21 | 26 | Semibold |
| Callout | Regular | 20 | 25 | Semibold |
| Subhead | Regular | 19 | 24 | Semibold |
| Footnote | Regular | 17 | 22 | Semibold |
| Caption 1 | Regular | 16 | 21 | Semibold |
| Caption 2 | Regular | 15 | 20 | Semibold |

#### xxxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 40 | 48 | Bold |
| Title 1 | Regular | 34 | 41 | Bold |
| Title 2 | Regular | 28 | 34 | Bold |
| Title 3 | Regular | 26 | 32 | Semibold |
| Headline | Semibold | 23 | 29 | Semibold |
| Body | Regular | 23 | 29 | Semibold |
| Callout | Regular | 22 | 28 | Semibold |
| Subhead | Regular | 21 | 28 | Semibold |
| Footnote | Regular | 19 | 24 | Semibold |
| Caption 1 | Regular | 18 | 23 | Semibold |
| Caption 2 | Regular | 17 | 22 | Semibold |

### iOS/iPadOS Larger Accessibility Type Sizes

#### AX1

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 44 | 52 | Bold |
| Title 1 | Regular | 38 | 46 | Bold |
| Title 2 | Regular | 34 | 41 | Bold |
| Title 3 | Regular | 31 | 38 | Semibold |
| Headline | Semibold | 28 | 34 | Semibold |
| Body | Regular | 28 | 34 | Semibold |
| Callout | Regular | 26 | 32 | Semibold |
| Subhead | Regular | 25 | 31 | Semibold |
| Footnote | Regular | 23 | 29 | Semibold |
| Caption 1 | Regular | 22 | 28 | Semibold |
| Caption 2 | Regular | 20 | 25 | Semibold |

#### AX2

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 48 | 57 | Bold |
| Title 1 | Regular | 43 | 51 | Bold |
| Title 2 | Regular | 39 | 47 | Bold |
| Title 3 | Regular | 37 | 44 | Semibold |
| Headline | Semibold | 33 | 40 | Semibold |
| Body | Regular | 33 | 40 | Semibold |
| Callout | Regular | 32 | 39 | Semibold |
| Subhead | Regular | 30 | 37 | Semibold |
| Footnote | Regular | 27 | 33 | Semibold |
| Caption 1 | Regular | 26 | 32 | Semibold |
| Caption 2 | Regular | 24 | 30 | Semibold |

#### AX3

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 52 | 61 | Bold |
| Title 1 | Regular | 48 | 57 | Bold |
| Title 2 | Regular | 44 | 52 | Bold |
| Title 3 | Regular | 43 | 51 | Semibold |
| Headline | Semibold | 40 | 48 | Semibold |
| Body | Regular | 40 | 48 | Semibold |
| Callout | Regular | 38 | 46 | Semibold |
| Subhead | Regular | 36 | 43 | Semibold |
| Footnote | Regular | 33 | 40 | Semibold |
| Caption 1 | Regular | 32 | 39 | Semibold |
| Caption 2 | Regular | 29 | 35 | Semibold |

#### AX4

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 56 | 66 | Bold |
| Title 1 | Regular | 53 | 62 | Bold |
| Title 2 | Regular | 50 | 59 | Bold |
| Title 3 | Regular | 49 | 58 | Semibold |
| Headline | Semibold | 47 | 56 | Semibold |
| Body | Regular | 47 | 56 | Semibold |
| Callout | Regular | 44 | 52 | Semibold |
| Subhead | Regular | 42 | 50 | Semibold |
| Footnote | Regular | 38 | 46 | Semibold |
| Caption 1 | Regular | 37 | 44 | Semibold |
| Caption 2 | Regular | 34 | 41 | Semibold |

#### AX5

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 60 | 70 | Bold |
| Title 1 | Regular | 58 | 68 | Bold |
| Title 2 | Regular | 56 | 66 | Bold |
| Title 3 | Regular | 55 | 65 | Semibold |
| Headline | Semibold | 53 | 62 | Semibold |
| Body | Regular | 53 | 62 | Semibold |
| Callout | Regular | 51 | 60 | Semibold |
| Subhead | Regular | 49 | 58 | Semibold |
| Footnote | Regular | 44 | 52 | Semibold |
| Caption 1 | Regular | 43 | 51 | Semibold |
| Caption 2 | Regular | 40 | 48 | Semibold |

### macOS Built-in Text Styles

| Style | Weight | Size (pt) | Line height (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 26 | 32 | Bold |
| Title 1 | Regular | 22 | 26 | Bold |
| Title 2 | Regular | 17 | 22 | Bold |
| Title 3 | Regular | 15 | 20 | Semibold |
| Headline | Bold | 13 | 16 | Heavy |
| Body | Regular | 13 | 16 | Semibold |
| Callout | Regular | 12 | 15 | Semibold |
| Subheadline | Regular | 11 | 14 | Semibold |
| Footnote | Regular | 10 | 13 | Semibold |
| Caption 1 | Regular | 10 | 13 | Medium |
| Caption 2 | Medium | 10 | 13 | Semibold |

### tvOS Built-in Text Styles

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Title 1 | Medium | 76 | 96 | Bold |
| Title 2 | Medium | 57 | 66 | Bold |
| Title 3 | Medium | 48 | 56 | Bold |
| Headline | Medium | 38 | 46 | Bold |
| Subtitle 1 | Regular | 38 | 46 | Medium |
| Callout | Medium | 31 | 38 | Bold |
| Body | Medium | 29 | 36 | Bold |
| Caption 1 | Medium | 25 | 32 | Bold |
| Caption 2 | Medium | 23 | 30 | Bold |

### watchOS Dynamic Type Sizes

#### Large (Default 40mm/41mm/42mm)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 36 | 38.5 | Bold |
| Title 1 | Regular | 34 | 36.5 | Semibold |
| Title 2 | Regular | 27 | 30.5 | Semibold |
| Title 3 | Regular | 19 | 21.5 | Semibold |
| Headline | Semibold | 16 | 18.5 | Semibold |
| Body | Regular | 16 | 18.5 | Semibold |
| Caption 1 | Regular | 15 | 17.5 | Semibold |
| Caption 2 | Regular | 14 | 16.5 | Semibold |
| Footnote 1 | Regular | 13 | 15.5 | Semibold |
| Footnote 2 | Regular | 12 | 14.5 | Semibold |

#### xSmall

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 30 | 32.5 | Bold |
| Title 1 | Regular | 28 | 30.5 | Semibold |
| Title 2 | Regular | 24 | 26.5 | Semibold |
| Title 3 | Regular | 17 | 19.5 | Semibold |
| Headline | Semibold | 14 | 16.5 | Semibold |
| Body | Regular | 14 | 16.5 | Semibold |
| Caption 1 | Regular | 13 | 15.5 | Semibold |
| Caption 2 | Regular | 12 | 14.5 | Semibold |
| Footnote 1 | Regular | 11 | 13.5 | Semibold |
| Footnote 2 | Regular | 10 | 12.5 | Semibold |

#### Small (Default 38mm)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 32 | 34.5 | Bold |
| Title 1 | Regular | 30 | 32.5 | Semibold |
| Title 2 | Regular | 26 | 28.5 | Semibold |
| Title 3 | Regular | 18 | 20.5 | Semibold |
| Headline | Semibold | 15 | 17.5 | Semibold |
| Body | Regular | 15 | 17.5 | Semibold |
| Caption 1 | Regular | 14 | 16.5 | Semibold |
| Caption 2 | Regular | 13 | 15.5 | Semibold |
| Footnote 1 | Regular | 12 | 14.5 | Semibold |
| Footnote 2 | Regular | 11 | 13.5 | Semibold |

#### xLarge (Default 44mm/45mm/49mm)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 40 | 42.5 | Bold |
| Title 1 | Regular | 38 | 40.5 | Semibold |
| Title 2 | Regular | 30 | 32.5 | Semibold |
| Title 3 | Regular | 20 | 22.5 | Semibold |
| Headline | Semibold | 17 | 19.5 | Semibold |
| Body | Regular | 17 | 19.5 | Semibold |
| Caption 1 | Regular | 16 | 18.5 | Semibold |
| Caption 2 | Regular | 15 | 17.5 | Semibold |
| Footnote 1 | Regular | 14 | 16.5 | Semibold |
| Footnote 2 | Regular | 13 | 15.5 | Semibold |

#### xxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 41 | 43.5 | Bold |
| Title 1 | Regular | 39 | 41.5 | Semibold |
| Title 2 | Regular | 31 | 33.5 | Semibold |
| Title 3 | Regular | 21 | 23.5 | Semibold |
| Headline | Semibold | 18 | 20.5 | Semibold |
| Body | Regular | 18 | 20.5 | Semibold |
| Caption 1 | Regular | 17 | 19.5 | Semibold |
| Caption 2 | Regular | 15 | 18.5 | Semibold |
| Footnote 1 | Regular | 15 | 17.5 | Semibold |
| Footnote 2 | Regular | 14 | 16.5 | Semibold |

#### xxxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 42 | 44.5 | Bold |
| Title 1 | Regular | 40 | 42.5 | Semibold |
| Title 2 | Regular | 32 | 34.5 | Semibold |
| Title 3 | Regular | 22 | 24.5 | Semibold |
| Headline | Semibold | 19 | 21.5 | Semibold |
| Body | Regular | 19 | 21.5 | Semibold |
| Caption 1 | Regular | 18 | 20.5 | Semibold |
| Caption 2 | Regular | 17 | 19.5 | Semibold |
| Footnote 1 | Regular | 16 | 18.5 | Semibold |
| Footnote 2 | Regular | 15 | 17.5 | Semibold |

### watchOS Larger Accessibility Type Sizes

#### AX1

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 44 | 46.5 | Bold |
| Title 1 | Regular | 42 | 44.5 | Semibold |
| Title 2 | Regular | 34 | 41 | Semibold |
| Title 3 | Regular | 24 | 26.5 | Semibold |
| Headline | Semibold | 21 | 23.5 | Semibold |
| Body | Regular | 21 | 23.5 | Semibold |
| Caption 1 | Regular | 18 | 20.5 | Semibold |
| Caption 2 | Regular | 17 | 19.5 | Semibold |
| Footnote 1 | Regular | 16 | 18.5 | Semibold |
| Footnote 2 | Regular | 15 | 17.5 | Semibold |

#### AX2

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 45 | 47.5 | Bold |
| Title 1 | Regular | 43 | 46 | Semibold |
| Title 2 | Regular | 35 | 37.5 | Semibold |
| Title 3 | Regular | 25 | 27.5 | Semibold |
| Headline | Semibold | 22 | 24.5 | Semibold |
| Body | Regular | 22 | 24.5 | Semibold |
| Caption 1 | Regular | 19 | 21.5 | Semibold |
| Caption 2 | Regular | 18 | 20.5 | Semibold |
| Footnote 1 | Regular | 17 | 19.5 | Semibold |
| Footnote 2 | Regular | 16 | 17.5 | Semibold |

#### AX3

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
| --- | --- | --- | --- | --- |
| Large Title | Regular | 46 | 48.5 | Bold |
| Title 1 | Regular | 44 | 47 | Semibold |
| Title 2 | Regular | 36 | 38.5 | Semibold |
| Title 3 | Regular | 26 | 28.5 | Semibold |
| Headline | Semibold | 23 | 25.5 | Semibold |
| Body | Regular | 23 | 25.5 | Semibold |
| Caption 1 | Regular | 20 | 22.5 | Semibold |
| Caption 2 | Regular | 19 | 21.5 | Semibold |
| Footnote 1 | Regular | 18 | 20.5 | Semibold |
| Footnote 2 | Regular | 17 | 19.5 | Semibold |

## Tracking Values

### SF Pro (iOS, iPadOS, visionOS, macOS, tvOS)

| Size (pt) | Tracking (1/1000 em) | Tracking (pt) |
| --- | --- | --- |
| 6 | +41 | +0.24 |
| 7 | +34 | +0.23 |
| 8 | +26 | +0.21 |
| 9 | +19 | +0.17 |
| 10 | +12 | +0.12 |
| 11 | +6 | +0.06 |
| 12 | 0 | 0.0 |
| 13 | -6 | -0.08 |
| 14 | -11 | -0.15 |
| 15 | -16 | -0.23 |
| 16 | -20 | -0.31 |
| 17 | -26 | -0.43 |
| 18 | -25 | -0.44 |
| 19 | -24 | -0.45 |
| 20 | -23 | -0.45 |
| 21 | -18 | -0.36 |
| 22 | -12 | -0.26 |
| 23 | -4 | -0.10 |
| 24 | +3 | +0.07 |
| 25 | +6 | +0.15 |
| 26 | +8 | +0.22 |
| 27 | +11 | +0.29 |
| 28 | +14 | +0.38 |
| 29–30 | +14 | +0.40 |
| 31 | +13 | +0.39 |
| 32 | +13 | +0.41 |
| 33–34 | +12 | +0.40 |
| 35 | +11 | +0.38 |
| 36 | +10 | +0.37 |
| 37 | +10 | +0.36 |
| 38–40 | +10 | +0.37 |
| 41 | +9 | +0.36 |
| 42–43 | +9 | +0.37–0.38 |
| 44 | +8 | +0.37 |
| 45 | +8 | +0.35 |
| 46–48 | +8 | +0.35–0.37 |
| 49–50 | +7 | +0.33–0.34 |
| 51 | +7 | +0.35 |
| 52–54 | +6 | +0.30–0.33 |
| 56 | +6 | +0.30 |
| 58 | +5 | +0.28 |
| 60 | +4 | +0.26 |
| 62–64 | +4 | +0.22–0.24 |
| 66 | +3 | +0.19 |
| 68 | +2 | +0.17 |
| 70–72 | +2 | +0.14 |
| 76 | +1 | +0.07 |
| 80–96 | 0 | 0 |

### SF Pro Rounded (iOS, iPadOS, visionOS)

| Size (pt) | Tracking (1/1000 em) | Tracking (pt) |
| --- | --- | --- |
| 6 | +87 | +0.51 |
| 7 | +80 | +0.54 |
| 8 | +72 | +0.57 |
| 9 | +65 | +0.57 |
| 10 | +58 | +0.57 |
| 11 | +52 | +0.56 |
| 12 | +46 | +0.54 |
| 13 | +40 | +0.51 |
| 14 | +35 | +0.48 |
| 15 | +30 | +0.44 |
| 16 | +26 | +0.41 |
| 17 | +22 | +0.37 |
| 18 | +21 | +0.37 |
| 19 | +20 | +0.37 |
| 20 | +18 | +0.36 |
| 21 | +17 | +0.35 |
| 22 | +16 | +0.34 |
| 23–24 | +15–16 | +0.35 |
| 25–26 | +14 | +0.35–0.36 |
| 27–28 | +13–14 | +0.36 |
| 29 | +13 | +0.37 |
| 30 | +12 | +0.37 |
| 31 | +12 | +0.36 |
| 32–34 | +12 | +0.38–0.39 |
| 35 | +11 | +0.38 |
| 36 | +11 | +0.39 |
| 37–39 | +10 | +0.38–0.39 |
| 40–42 | +10 | +0.38–0.39 |
| 43 | +9 | +0.38 |
| 44–48 | +8 | +0.35–0.37 |
| 49 | +8 | +0.36 |
| 50 | +7 | +0.34 |
| 51–54 | +6 | +0.30–0.33 |
| 56 | +6 | +0.30 |
| 58 | +4 | +0.25 |
| 60–62 | +4 | +0.21–0.23 |
| 64 | +3 | +0.19 |
| 66 | +2 | +0.16 |
| 68 | +2 | +0.13 |
| 70 | +2 | +0.14 |
| 72 | +2 | +0.11 |
| 76 | +1 | +0.07 |
| 80–96 | 0 | 0 |

### New York (iOS, iPadOS, visionOS)

| Size (pt) | Tracking (1/1000 em) | Tracking (pt) |
| --- | --- | --- |
| 6 | +40 | +0.23 |
| 7 | +32 | +0.22 |
| 8 | +25 | +0.20 |
| 9 | +20 | +0.18 |
| 10 | +16 | +0.15 |
| 11 | +11 | +0.12 |
| 12 | +6 | +0.07 |
| 13 | +4 | +0.05 |
| 14 | +2 | +0.03 |
| 15 | 0 | 0.00 |
| 16 | -2 | -0.03 |
| 17 | -4 | -0.07 |
| 18 | -6 | -0.11 |
| 19 | -8 | -0.15 |
| 20 | -10 | -0.20 |
| 21 | -10 | -0.21 |
| 22 | -10 | -0.23 |
| 23 | -11 | -0.25 |
| 24 | -11 | -0.26 |
| 25 | -11 | -0.27 |
| 26 | -12 | -0.29 |
| 27 | -12 | -0.32 |
| 28 | -12 | -0.33 |
| 29 | -12 | -0.34 |
| 30 | -12 | -0.37 |
| 31 | -13 | -0.39 |
| 32 | -13 | -0.41 |
| 33 | -13 | -0.42 |
| 34 | -14 | -0.45 |
| 35 | -14 | -0.48 |
| 36 | -14 | -0.49 |
| 38 | -14 | -0.52 |
| 40 | -14 | -0.55 |
| 48 | -14 | -0.68 |
| 54 | -15 | -0.79 |
| 72 | -16 | -1.09 |
| 96 | -16 | -1.50 |
| 140 | -16 | -2.26 |
| 200 | -17 | -3.32 |
| 260 | -18 | -4.57 |

### SF Compact (watchOS)

Key tracking values:

| Size (pt) | Tracking (1/1000 em) | Tracking (pt) |
| --- | --- | --- |
| 6 | +50 | +0.29 |
| 10 | +30 | +0.29 |
| 12 | +20 | +0.23 |
| 14 | +14 | +0.19 |
| 16 | 0 | 0.00 |
| 17 | -4 | -0.07 |
| 18 | -8 | -0.14 |
| 19 | -12 | -0.22 |
| 20 | 0 | 0.00 |
| 24 | -8 | -0.19 |
| 28 | -12 | -0.34 |
| 32 | -16 | -0.50 |
| 36 | -20 | -0.69 |
| 40 | -20 | -0.78 |
| 48 | -20 | -0.96 |
| 64 | -23 | -1.44 |
| 80 | -26 | -1.99 |
| 96 | -28 | -2.62 |

### SF Compact Rounded (watchOS)

Key tracking values:

| Size (pt) | Tracking (1/1000 em) | Tracking (pt) |
| --- | --- | --- |
| 6 | +28 | +0.16 |
| 10 | +20 | +0.20 |
| 12 | +16 | +0.19 |
| 14 | +12 | +0.16 |
| 16 | +8 | +0.12 |
| 18 | +4 | +0.07 |
| 20 | 0 | 0.00 |
| 24 | -8 | -0.19 |
| 28 | -12 | -0.34 |
| 32 | -16 | -0.50 |
| 36 | -20 | -0.69 |
| 40 | -20 | -0.78 |
| 48 | -20 | -0.96 |
| 64 | -23 | -1.44 |
| 80 | -26 | -1.99 |
| 96 | -28 | -2.62 |