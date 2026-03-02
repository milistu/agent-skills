# Widgets Design Guidelines

Comprehensive guidelines for designing widgets across Apple platforms (iOS, iPadOS, macOS, watchOS, visionOS).

## Widget Families & Sizes

### System Family Widgets
Offer a broad range of sizes with optional interactive elements: **Small**, **Medium**, **Large**, **Extra Large**, **Extra Large Portrait**.

| Widget Size | iPhone | iPad | Mac | Apple Vision Pro |
|---|---|---|---|---|
| System small | Home Screen, Today View, StandBy, CarPlay | Home Screen, Today View, Lock Screen | Desktop, Notification Center | Horizontal & vertical surfaces |
| System medium | Home Screen, Today View | Home Screen, Today View | Desktop, Notification Center | Horizontal & vertical surfaces |
| System large | Home Screen, Today View | Home Screen, Today View | Desktop, Notification Center | Horizontal & vertical surfaces |
| System extra large | Not supported | Home Screen, Today View | Desktop, Notification Center | Horizontal & vertical surfaces |
| System extra large portrait | Not supported | Not supported | Not supported | Horizontal & vertical surfaces |

### Accessory Widgets
Display very limited information due to size: **Circular**, **Corner**, **Inline**, **Rectangular**.

| Widget Size | iPhone | iPad | Apple Watch |
|---|---|---|---|
| Accessory circular | Lock Screen | Lock Screen | Complications & Smart Stack |
| Accessory corner | Not supported | Not supported | Complications |
| Accessory inline | Lock Screen | Lock Screen | Complications |
| Accessory rectangular | Lock Screen | Lock Screen | Complications & Smart Stack |

## Appearances & Rendering Modes

### Appearance Contexts
- **iPhone/iPad Home Screen**: People choose light, dark, clear, or tinted. Light/dark = full-color. Clear = desaturated + translucency + Liquid Glass. Tinted = desaturated + person's tint color.
- **Apple Vision Pro**: 3D object with frame, full-color with glass/paper coating, optional tinted appearance from system palettes.
- **iPad Lock Screen**: Monochromatic without tint.
- **iPhone StandBy**: Scaled up, background removed. Low-light = monochromatic red tint.
- **Apple Watch**: Full-color and tinted in complications and Smart Stack.

### Rendering Modes

| Platform | Full-color | Accented | Vibrant |
|---|---|---|---|
| iPhone | Home Screen, Today view, StandBy, CarPlay (bg removed) | Home Screen, Today view | Lock Screen, StandBy low-light |
| iPad | Home Screen, Today view | Home Screen, Today view | Lock Screen |
| Apple Watch | Smart Stack, complications | Smart Stack, complications | Not supported |
| Mac | Desktop, Notification Center | Not supported | Desktop |
| Apple Vision Pro | Horizontal & vertical surfaces | Horizontal & vertical surfaces | Not supported |

#### Full-color Mode
- Support light and dark appearances. Use light backgrounds for light mode, dark backgrounds for dark mode.
- Use semantic system colors for dynamic adaptation.

#### Accented Mode
- Group widget components into **accent group** and **primary group**.
- iPhone/iPad/Mac: both groups tinted white. Apple Watch: primary = white, accent = watch face color.
- Use `widgetAccentable(_:)` to define groups.

#### Vibrant Mode
- Pixel opacity determines background material effect strength. Brightness determines vibrancy.
- Use white/light gray for prominent content, darker grayscale for secondary.
- Use opaque grayscale values rather than white opacities for best vibrant material effect.

## Best Practices

- Choose **simple ideas** related to your app's main purpose with timely content.
- Give people **quick access** to content they want; don't replicate an app icon.
- Prefer **dynamic information** that changes throughout the day.
- Look for opportunities to **surprise and delight** (birthdays, holidays).
- Offer **multiple sizes only when it adds value**; avoid stretching small content to fill larger sizes.
- **Balance information density**: sparse = unnecessary; dense = not glanceable.
- Display only information **directly related to the widget's main purpose**.
- Use **brand elements thoughtfully** — colors, typefaces, glyphs for recognition without overpowering. Small logo in top-right corner if needed.
- Choose between **automatic content** vs. **user-configurable** information.
- Don't mirror widget appearance within your app.
- Inform users when **authentication adds value** (e.g., "Sign in to view reservations").

### Updating Content
- Find appropriate update frequency; widgets don't support real-time updates.
- Use system functionality to refresh dates/times automatically.
- Use animated transitions (up to 2 seconds) for data updates.

### Interactivity
- Widgets can include **buttons and toggles** for actions without launching the app.
- Tapping non-interactive areas launches the app.
- **Deep link** to the right location in your app.
- Keep interactions **glanceable and uncluttered**; avoid app-like layouts.
- Inline accessory widgets offer only **one tap target**.

## Margins & Padding

- Standard margin: **16 points** for most widgets.
- Tighter margin: **11 points** for content groupings, graphics, buttons, background shapes.
- Widgets use smaller margins on Mac desktop and Lock Screen (including StandBy).
- Coordinate content corner radius with widget corner radius using `ContainerRelativeShape`.

## Typography

- Prefer **system font, text styles, and SF Symbols**.
- Custom fonts: use sparingly, typically for large text only; SF Pro for smaller text.
- **Minimum font size: 11 points**.
- Never rasterize text — use text elements for scaling and VoiceOver.
- Supports Dynamic Type sizes Large to AX5 (iOS, iPadOS, visionOS).

## Color

- Use color to **enhance** without competing with content.
- **Don't rely solely on color** to convey meaning (widgets may render monochrome).
- Use full-color images **judiciously** — system desaturates by default in tinted/clear modes. Reserve full-color for media content (album art) and keep dimensions smaller than widget size.

## Previews & Placeholders

- Design **realistic previews** for the widget gallery with real or simulated data.
- Create **placeholder content** with semi-opaque shapes standing in for dynamic content (rectangles for text, circles/squares for glyphs/images).
- Write **succinct descriptions** starting with an action verb (e.g., "See the current weather…").
- **Group widget sizes together** with a single description.
- Consider **coloring the Add button** with your brand color.

## Platform-Specific Guidance

### iOS / iPadOS
- Lock Screen widgets follow [Complications] design principles in addition to widget guidelines.
- Lock Screen shapes: inline text (above clock), circular and rectangular (below clock).
- Support **Always-On display**: use gray levels with enough contrast, ensure legibility at reduced luminance.
- Use **Live Activities** for real-time updates instead of widgets.

#### StandBy & CarPlay
- Two small widgets side-by-side, scaled up to fill screen.
- Limit rich images/color; scale up text for distance viewing.
- **Remove background colors** for StandBy (blend with black background).
- Low-light: monochromatic red tint.

### visionOS
- Widgets are **3D objects** placed on horizontal or vertical surfaces; they persist across sessions.
- Full-color by default; accented mode with system color palettes.
- No systemwide light/dark; apps can offer their own theme options.

#### Thresholds & Sizes
- Two proximity thresholds: `simplified` (distant) and `default` (nearby).
- Distant: fewer details, larger type, no interactive elements.
- Nearby: more details, smaller type, interactive elements.
- Maintain shared elements across both thresholds.
- People can scale widgets 75%–125%.
- Use **high-resolution assets** and clear hierarchy.

#### Mounting Styles
- **Elevated** (default): works on horizontal and vertical surfaces. On horizontal = tilted back with shadow. On vertical = flush like picture frame. People can choose frame widths.
- **Recessed**: vertical surfaces only. Content set back into surface (cutout illusion). Ideal for immersive/ambient content.
- Use `supportedMountingStyles(_:)` to declare supported styles.

#### Treatment Styles
- **Paper**: print-like, solid, responds to lighting changes. Good for artwork/media.
- **Glass**: lighter, layered look. Foreground stays bright/legible regardless of lighting. Good for information-rich widgets.

### watchOS
- Provide **colorful backgrounds** conveying meaning (e.g., red for falling stocks, green for rising).
- Use relevancy information (location, ongoing activities) to help system elevate widget position in Smart Stack.

## Specifications

### iOS Dimensions

| Screen (portrait, pt) | Small (pt) | Medium (pt) | Large (pt) | Circular (pt) | Rectangular (pt) | Inline (pt) |
|---|---|---|---|---|---|---|
| 430×932 | 170×170 | 364×170 | 364×382 | 76×76 | 172×76 | 257×26 |
| 428×926 | 170×170 | 364×170 | 364×382 | 76×76 | 172×76 | 257×26 |
| 414×896 | 169×169 | 360×169 | 360×379 | 76×76 | 160×72 | 248×26 |
| 414×736 | 159×159 | 348×157 | 348×357 | 76×76 | 170×76 | 248×26 |
| 393×852 | 158×158 | 338×158 | 338×354 | 72×72 | 160×72 | 234×26 |
| 390×844 | 158×158 | 338×158 | 338×354 | 72×72 | 160×72 | 234×26 |
| 375×812 | 155×155 | 329×155 | 329×345 | 72×72 | 157×72 | 225×26 |
| 375×667 | 148×148 | 321×148 | 321×324 | 68×68 | 153×68 | 225×26 |
| 360×780 | 155×155 | 329×155 | 329×345 | 72×72 | 157×72 | 225×26 |
| 320×568 | 141×141 | 292×141 | 292×311 | N/A | N/A | N/A |

### iPadOS Dimensions

| Screen (portrait, pt) | Target | Small (pt) | Medium (pt) | Large (pt) | Extra Large (pt) |
|---|---|---|---|---|---|
| 768×1024 | Canvas | 141×141 | 305.5×141 | 305.5×305.5 | 634.5×305.5 |
| | Device | 120×120 | 260×120 | 260×260 | 540×260 |
| 744×1133 | Canvas | 141×141 | 305.5×141 | 305.5×305.5 | 634.5×305.5 |
| | Device | 120×120 | 260×120 | 260×260 | 540×260 |
| 810×1080 | Canvas | 146×146 | 320.5×146 | 320.5×320.5 | 669×320.5 |
| | Device | 124×124 | 272×124 | 272×272 | 568×272 |
| 820×1180 | Canvas | 155×155 | 342×155 | 342×342 | 715.5×342 |
| | Device | 136×136 | 300×136 | 300×300 | 628×300 |
| 834×1112 | Canvas | 150×150 | 327.5×150 | 327.5×327.5 | 682×327.5 |
| | Device | 132×132 | 288×132 | 288×288 | 600×288 |
| 834×1194 | Canvas | 155×155 | 342×155 | 342×342 | 715.5×342 |
| | Device | 136×136 | 300×136 | 300×300 | 628×300 |
| 954×1373* | Canvas | 162×162 | 350×162 | 350×350 | 726×350 |
| | Device | 162×162 | 350×162 | 350×350 | 726×350 |
| 970×1389* | Canvas | 162×162 | 350×162 | 350×350 | 726×350 |
| | Device | 162×162 | 350×162 | 350×350 | 726×350 |
| 1024×1366 | Canvas | 170×170 | 378.5×170 | 378.5×378.5 | 795×378.5 |
| | Device | 160×160 | 356×160 | 356×356 | 748×356 |
| 1192×1590* | Canvas | 188×188 | 412×188 | 412×412 | 860×412 |
| | Device | 188×188 | 412×188 | 412×412 | 860×412 |

\* When Display Zoom is set to More Space.

### visionOS Dimensions

| Widget | Size (pt) | Size (mm, 100%) |
|---|---|---|
| Small | 158×158 | 268×268 |
| Medium | 338×158 | 574×268 |
| Large | 338×354 | 574×600 |
| Extra large | 450×338 | 763×574 |
| Extra large portrait | 338×450 | 574×763 |

### watchOS Dimensions

| Apple Watch Size | Smart Stack Widget (pt) |
|---|---|
| 40mm | 152×69.5 |
| 41mm | 165×72.5 |
| 44mm | 173×76.5 |
| 45mm | 184×80.5 |
| 49mm | 191×81.5 |