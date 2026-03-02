# Images Guidelines

Guidelines for image resolution, formats, scale factors, and platform-specific image considerations across Apple platforms.

## Resolution & Scale Factors

A **point** is an abstract measurement unit. In 2D platforms, a point maps to pixels based on display resolution. In visionOS, a point is an angular value that scales with distance.

**Scale factors** determine image resolution:
- **@1x** — 1:1 pixel density (1 pixel = 1 point)
- **@2x** — 2:1 pixel density
- **@3x** — 3:1 pixel density

**Provide high-resolution assets for all bitmap images.** Append "@1x," "@2x," or "@3x" to filenames in the asset catalog.

| Platform | Scale factors |
| --- | --- |
| iPadOS, watchOS | @2x |
| iOS | @2x and @3x |
| visionOS | @2x or higher |
| macOS, tvOS | @1x and @2x |

**Design images at the lowest resolution and scale up.** Position control points at whole values so they align cleanly at 1x and remain aligned at higher resolutions.

## Recommended Formats

| Image type | Format |
| --- | --- |
| Bitmap or raster work | De-interlaced PNG |
| PNG graphics without full 24-bit color | 8-bit color palette |
| Photos | JPEG (optimized) or HEIC |
| Stereo or spatial photos | Stereo HEIC |
| Flat icons, interface icons, flat artwork needing high-res scaling | PDF or SVG |

## Best Practices

- **Include a color profile with each image** to ensure colors appear as intended on different displays.
- **Always test images on a range of actual devices.** Images may appear pixelated, stretched, or compressed on various screens.

## tvOS: Layered Images & Parallax

Layered images combine 2–5 distinct layers with transparency to create depth. The **parallax effect** elevates focused elements, applying subtle motion and illumination.

- Layered images are **required** for tvOS app icons; strongly encouraged for other focusable images (e.g., Top Shelf).
- Use standard views and system focus APIs (e.g., `FocusState`) for automatic parallax treatment.
- **Foreground layers**: prominent elements (characters, text on covers/posters).
- **Middle layers**: secondary content, shadows.
- **Background layer**: must be **opaque** — you'll get an error otherwise.
- Keep layering **simple and subtle** to avoid unrealistic 3D effects.
- **Leave a safe zone** around foreground layers to account for scaling/cropping when focused.
- Generally **keep text in the foreground** for clarity.
- Runtime layered images from servers must use `.lcr` format (generate from LSR/PSD via `layerutil` CLI). Don't embed `.lcr` files in your app.
- Preview layered images using Xcode, Parallax Previewer, or Parallax Exporter throughout design.

## visionOS

Images can be viewed at a much larger range of sizes; the system dynamically scales resolution to match current size. Pixels may not align 1:1 with screen pixels.

- **Create a layered app icon** with 2–3 layers for depth appearance.
- **Prefer vector-based art** for 2D images. Bitmaps may not look good when scaled up.
- **Rasterized images**: @2x looks fine at common distances but won't be dynamically scaled. Higher resolutions (up to @6x) look sharper from close up but increase file size and may impact performance. Apply high-quality image filtering for resolutions above @2x (see `CALayer/filters`).

### Spatial Photos & Spatial Scenes

- **Spatial photo**: stereoscopic photo with spatial metadata (captured on iPhone 15 Pro+, Apple Vision Pro, or compatible camera).
- **Spatial scene**: 3D image generated from a 2D image with parallax responding to head movement.
- Use **stereo HEIC** format for spatial photos — visionOS applies visual treatments to minimize stereo-viewing discomfort.
- Use **feathered glass background effect** (`GlassBackgroundEffect`) when placing text over spatial photos for contrast and comfort.
- **Display spatial photos/scenes in standalone views** (sheets/windows), not inline with other content, to avoid visual discomfort. If inline is necessary, use generous spacing.
- **Spatial scenes take seconds to generate** — design experiences accordingly (e.g., explicit actions, not batch generation).
- Prefer **larger spatial scenes centered in field of view** for stronger parallax effect.
- When displaying immersively, prefer **minimal UI**.

## watchOS

- **Avoid transparency** to keep files small (except for complications, menu icons, and template images where transparency is required for color application).
- **Use autoscaling PDFs** — design for 40mm/42mm at 2x; WatchKit scales automatically:

| Screen size | Image scale |
| --- | --- |
| 38mm | 90% |
| 40mm | 100% |
| 41mm | 106% |
| 42mm | 100% |
| 44mm | 110% |
| 45mm | 119% |
| 49mm | 119% |