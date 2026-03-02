# App Icons

Guidelines for designing app icons across all Apple platforms, including layer design, shapes, visual effects, appearances, and specifications.

## Layer Design

Layered app icons produce depth and vitality. The system applies visual effects that respond to environment and interactions.

- **iOS, iPadOS, macOS, watchOS**: Background layer + one or more foreground layers. Icons take on Liquid Glass attributes (specular highlights, frostiness, translucency) responding to lighting and device movement.
- **tvOS**: 2–5 layers creating parallax effect when focused. Icon elevates and sways in response to remote input.
- **visionOS**: Background layer + 1–2 layers on top, producing a 3D object. System adds shadows between layers and uses alpha channels for embossed appearance.

### Layer Design Best Practices

- **Prefer clearly defined edges in foreground layers.** Avoid soft/feathered edges — they degrade system-drawn highlights and shadows.
- **Vary opacity in foreground layers** to increase depth and liveliness. Import fully opaque layers and adjust transparency in Icon Composer.
- **Design a background that stands out and emphasizes foreground content.** Subtle top-to-bottom, light-to-dark gradients respond well to system lighting. Icon Composer supports solid colors and gradients for backgrounds. If importing a custom background layer, make it full-bleed and opaque.
- **Prefer vector graphics (SVG or PDF)** when bringing layers into Icon Composer. Outline artwork and convert text to outlines. For mesh gradients and raster artwork, use PNG (lossless).

### Tooling

- **iOS, iPadOS, macOS, watchOS**: Use Icon Composer (included with Xcode) to define background, adjust foreground placement, apply transparency, define appearance variants, and export.
- **tvOS, visionOS**: Add icon layers directly to an image stack in Xcode.

## Icon Shape

| Platform | Layout Shape | Masked Shape |
|---|---|---|
| iOS, iPadOS, macOS | Square | Rounded rectangle |
| tvOS | Rectangle (landscape) | Rounded rectangle |
| visionOS, watchOS | Square | Circle |

- **Provide unmasked layers** in the appropriate shape. The system applies masking. Pre-defined masking negatively impacts specular highlights and creates jagged edges.
- **Keep primary content centered** to avoid truncation from corner adjustment or masking. Especially important for circular visionOS/watchOS icons. Use grids from [Apple Design Resources](https://developer.apple.com/design/resources/).

## Design Principles

- **Embrace simplicity.** Fine visual features look busy with system shadows/highlights. Find a core concept and express it with minimal shapes. Prefer simple backgrounds (solid color or gradient).
- **Provide visually consistent icon design across all platforms.**
- **Base design around filled, overlapping shapes.** Overlapping solid shapes with transparency and blurring create depth.
- **Include text only when essential** to brand. Text doesn't support accessibility or localization, is hard to read at small sizes. Avoid words like "Watch," "Play," "New," or platform names. In tvOS, place text above other layers to avoid parallax cropping.
- **Prefer illustrations to photos.** Photos don't work well at small sizes or split into layers. Don't replicate UI components or use screenshots.
- **Don't use replicas of Apple hardware products** (copyrighted).

## Visual Effects

- **Let the system handle blurring and visual effects.** Don't include specular highlights, drop shadows, beveled edges, blurs, or glows — the system applies these dynamically. Custom effects are static and may conflict.
- **Create layer groupings** in Icon Composer to apply effects to multiple layers at once.

## Appearances (iOS, iPadOS, macOS)

People can choose: default, dark, clear, or tinted appearance. You can design variants for each; the system auto-generates variants you don't provide.

- **Keep core visual features consistent across appearances.** Don't swap elements between variants.
- **Dark and tinted icons should feel at home beside system icons and widgets.** Dark icons are more subdued; clear and tinted even more so.
- **Use light icon as basis for dark icon.** Choose complementary colors. Color backgrounds offer greatest contrast in dark mode.
- **Alternate app icons** (iOS, iPadOS, tvOS, compatible visionOS apps): Let users choose alternate icons in settings. Each must remain related to your content. Alternate icons require their own dark, clear, and tinted variants. All are subject to App Review.

## Platform-Specific Considerations

### tvOS
- **Include a safe zone** around content. The system may crop edges when the icon scales/moves on focus. Foreground layers are cropped more than background layers.

### visionOS
- **Avoid shapes that look like holes or concave areas** on the background layer. System shadow and highlights make them stand out instead of recede.

### watchOS
- **Avoid black backgrounds.** Lighten them so the icon doesn't blend into the display background.

## Specifications

| Platform | Layout Shape | Masked Shape | Layout Size | Style | Appearances |
|---|---|---|---|---|---|
| iOS, iPadOS, macOS | Square | Rounded rectangle | 1024×1024 px | Layered | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | Rectangle (landscape) | Rounded rectangle | 800×480 px | Layered (Parallax) | N/A |
| visionOS | Square | Circular | 1024×1024 px | Layered (3D) | N/A |
| watchOS | Square | Circular | 1088×1088 px | Layered | N/A |

The system automatically scales icons for smaller contexts (Settings, notifications).

### Supported Color Spaces
- sRGB (color)
- Gray Gamma 2.2 (grayscale)
- Display P3 (wide-gamut — iOS, iPadOS, macOS, tvOS, watchOS only)