# Layout Guidelines

Guidelines for creating adaptive, consistent layouts across Apple platforms, including visual hierarchy, safe areas, platform-specific rules, and device specifications.

## Best Practices

- **Group related items** using negative space, background shapes, colors, materials, or separator lines. Ensure content and controls remain clearly distinct.
- **Give essential information sufficient space.** Don't obscure important info with nonessential details. Place secondary info in other parts of the window or additional views.
- **Extend content to fill the screen or window.** Backgrounds and full-screen artwork should extend to display edges. Scrollable layouts should continue to bottom and sides. Controls (sidebars, tab bars) appear on top of content.
- Use `backgroundExtensionEffect()` (SwiftUI) or `UIBackgroundExtensionView` (UIKit) to extend content appearance beneath sidebars/inspectors.

## Visual Hierarchy

- **Differentiate controls from content** using Liquid Glass material for consistent control appearance across iOS, iPadOS, macOS. Use scroll edge effects instead of backgrounds for content-to-control transitions.
- **Place items by importance** following reading order (top-to-bottom, leading-to-trailing). Account for RTL languages.
- **Align components** with one another for easier scanning and to communicate organization/hierarchy.
- **Use progressive disclosure** — disclosure controls, partial item display — to indicate hidden content.
- **Provide enough space around controls** and group them in logical sections. Don't crowd unrelated controls together.

## Adaptability

Common variations to handle:
- Different screen sizes, resolutions, color spaces
- Portrait/landscape orientations
- System features (Dynamic Island, camera controls)
- External display, Display Zoom, resizable iPad windows
- Dynamic Type text-size changes
- Locale-based internationalization (LTR/RTL, date/number formats, font/text length variation)

**Key guidance:**
- Design layouts that adapt gracefully while remaining consistent. Respect system-defined safe areas, margins, and guides.
- Support Dynamic Type. Use `UserInterfaceSizeClass` for adaptive layouts.
- Preview on multiple devices with different orientations, localizations, and text sizes. Test largest and smallest layouts first.
- Scale artwork in response to display changes — don't change aspect ratio; scale so important content remains visible.

## Guides and Safe Areas

- **Layout guide**: Rectangular region for positioning, aligning, spacing content. See `UILayoutGuide` / `NSLayoutGuide`.
- **Safe area**: Area within a view not covered by toolbars, tab bars, or system features (Dynamic Island, camera housing). See `SafeAreaRegions`.
- Always respect safe areas to accommodate display/system features and interactive components like bars.

## Platform-Specific Guidelines

### iOS

- **Support both portrait and landscape.** If single-orientation only, support both rotation directions for landscape.
- **Games should use full-bleed interfaces** accommodating corner radius, sensor housing, Dynamic Island.
- **Avoid full-width buttons.** Respect system margins; inset from screen edges. If full-width is needed, harmonize with hardware curvature.
- **Keep the status bar visible** unless in immersive experiences (games, media playback).

### iPadOS

- Windows can be freely resized down to minimum width/height (similar to macOS).
- **Defer switching to compact view as long as possible.** Design for full-screen first; only switch when full layout no longer fits.
- **Test at common system-provided sizes** (halves, thirds, quadrants). Minimize unexpected UI changes during resize.
- **Consider convertible tab bar** (`sidebarAdaptable`) for adaptive navigation — switches between sidebar and tab bar based on width.

### macOS

- **Avoid controls or critical info at window bottom** — people often move windows so bottom edge is below screen.
- **Avoid content within camera housing** at top edge. See `NSPrefersDisplaySafeAreaCompatibilityMode`.

### tvOS

- Layouts don't auto-adapt to screen size — same interface on every display. Design for variety of screen sizes.
- **Safe area**: Inset primary content **60pt** top/bottom, **80pt** sides.
- **Provide padding between focusable elements** — elements grow when focused; prevent overlap.
- Use consistent spacing in grids.
- Make partially hidden offscreen content symmetrical on each side.

#### tvOS Grid Specifications

All grids use **40pt horizontal spacing** and **100pt minimum vertical spacing**.

| Columns | Unfocused Content Width |
|---------|------------------------|
| 2 | 860 pt |
| 3 | 560 pt |
| 4 | 410 pt |
| 5 | 320 pt |
| 6 | 260 pt |
| 7 | 217 pt |
| 8 | 184 pt |
| 9 | 160 pt |

- Add extra vertical spacing for titled rows between bottom of previous unfocused row and center of title.

### visionOS

- **Center the most important content** in windows, especially large ones.
- **Keep content within window bounds.** System controls (Share, resize, close) appear just outside the window's XY bounds.
- **Use ornaments** for additional controls that don't belong in the window (toolbars, tab bars appear as ornaments).
- **Space interactive components** so button centers are at least **60pt apart** for comfortable eye-based targeting.
- Content extending along z-axis beyond window bounds gets clipped by system.

### watchOS

- **Extend content edge to edge** — the bezel provides natural padding. Minimize padding between elements.
- **Max 2-3 controls side by side**: up to 3 glyph buttons or 2 text buttons per row.
- **Support autorotation** in views people might show others (images, QR codes). See `WKExtension.isAutorotating`.

## Device Screen Dimensions

### iPhone

| Model | Dimensions (portrait) |
|-------|----------------------|
| iPhone 17 Pro Max | 440×956 pt (1320×2868 px @3x) |
| iPhone 17 Pro | 402×874 pt (1206×2622 px @3x) |
| iPhone Air | 420×912 pt (1260×2736 px @3x) |
| iPhone 17 | 402×874 pt (1206×2622 px @3x) |
| iPhone 16 Pro Max | 440×956 pt (1320×2868 px @3x) |
| iPhone 16 Pro | 402×874 pt (1206×2622 px @3x) |
| iPhone 16 Plus | 430×932 pt (1290×2796 px @3x) |
| iPhone 16 | 393×852 pt (1179×2556 px @3x) |
| iPhone 16e | 390×844 pt (1170×2532 px @3x) |
| iPhone 15 Pro Max | 430×932 pt (1290×2796 px @3x) |
| iPhone 15 Pro | 393×852 pt (1179×2556 px @3x) |
| iPhone 15 Plus | 430×932 pt (1290×2796 px @3x) |
| iPhone 15 | 393×852 pt (1179×2556 px @3x) |
| iPhone 14 Pro Max | 430×932 pt (1290×2796 px @3x) |
| iPhone 14 Pro | 393×852 pt (1179×2556 px @3x) |
| iPhone 14 Plus | 428×926 pt (1284×2778 px @3x) |
| iPhone 14 | 390×844 pt (1170×2532 px @3x) |
| iPhone 13 Pro Max | 428×926 pt (1284×2778 px @3x) |
| iPhone 13 Pro | 390×844 pt (1170×2532 px @3x) |
| iPhone 13 | 390×844 pt (1170×2532 px @3x) |
| iPhone 13 mini | 375×812 pt (1125×2436 px @3x) |
| iPhone SE 4.7" | 375×667 pt (750×1334 px @2x) |
| iPhone SE 4" | 320×568 pt (640×1136 px @2x) |

### iPad

| Model | Dimensions (portrait) |
|-------|----------------------|
| iPad Pro 12.9" | 1024×1366 pt (2048×2732 px @2x) |
| iPad Pro 11" | 834×1194 pt (1668×2388 px @2x) |
| iPad Pro 9.7" | 768×1024 pt (1536×2048 px @2x) |
| iPad Air 13" | 1024×1366 pt (2048×2732 px @2x) |
| iPad Air 11" | 820×1180 pt (1640×2360 px @2x) |
| iPad Air 10.9" | 820×1180 pt (1640×2360 px @2x) |
| iPad Air 10.5" | 834×1112 pt (1668×2224 px @2x) |
| iPad Air 9.7" | 768×1024 pt (1536×2048 px @2x) |
| iPad 11" | 820×1180 pt (1640×2360 px @2x) |
| iPad 10.2" | 810×1080 pt (1620×2160 px @2x) |
| iPad 9.7" | 768×1024 pt (1536×2048 px @2x) |
| iPad mini 8.3" | 744×1133 pt (1488×2266 px @2x) |
| iPad mini 7.9" | 768×1024 pt (1536×2048 px @2x) |

Note: All scale factors are UIKit scale factors, which may differ from native scale factors.

## Size Classes

Size classes: **regular** (larger screen / landscape) or **compact** (smaller screen / portrait). See `UserInterfaceSizeClass`.

| Device Category | Portrait | Landscape |
|----------------|----------|----------|
| All iPads | Regular W, Regular H | Regular W, Regular H |
| iPhone Plus/Max/Pro Max/Air | Compact W, Regular H | Regular W, Compact H |
| iPhone standard/Pro/mini/SE | Compact W, Regular H | Compact W, Compact H |

## Apple Watch Screen Dimensions

| Series | Size | Width (px) | Height (px) |
|--------|------|-----------|------------|
| Ultra 3 | 49mm | 422 | 514 |
| 10, 11 | 42mm | 374 | 446 |
| 10, 11 | 46mm | 416 | 496 |
| Ultra 1 & 2 | 49mm | 410 | 502 |
| 7, 8, 9 | 41mm | 352 | 430 |
| 7, 8, 9 | 45mm | 396 | 484 |
| 4, 5, 6, SE | 40mm | 324 | 394 |
| 4, 5, 6, SE | 44mm | 368 | 448 |
| 1, 2, 3 | 38mm | 272 | 340 |
| 1, 2, 3 | 42mm | 312 | 390 |