# Apple Watch Complications

Design guidelines for watchOS complications — timely, relevant information displayed on watch faces. Starting in watchOS 9, complications (also called *accessories*) are organized into families: Circular, Corner, Inline, and Rectangular. Use WidgetKit for watchOS 9+.

## Best Practices

- **Show essential, dynamic content** people want at a glance. Static complications that don't display meaningful data may be removed from prominent positions.
- **Support all complication families when possible.** More families = more watch face availability. If a family can't show useful data, display an app icon image so people can still launch your app.
- **Create multiple complications per family** to leverage shareable watch faces. Example: a triathlon app could offer three circular complications (swim, bike, run), each deep-linking to the relevant section.
- **Define different deep links for each complication.** Each should open the most relevant area in your app.
- **Consider Always-On privacy.** Sensitive information may be visible to others. See Always On guidelines.
- **Update timeline data carefully.** Limited daily updates and stored entries. Choose display times that enhance usefulness (e.g., meeting info 1 hour before; weather at expected occurrence time).

## Visual Design

### Ring/Gauge Styles
- **Closed** — percentage of a whole (e.g., battery gauge)
- **Open** — arbitrary min/max range (e.g., speed indicator)
- **Segmented** — app-defined range showing rapid changes (e.g., Noise)

### Tinted Mode
- System applies solid color to text, gauges, images; desaturates full-color images
- Don't use color as the only way to communicate information
- Provide alternative tinted-mode versions if full-color images look poor desaturated

### General
- Use line widths ≥ 2 points (thinner lines hard to see in motion)
- Provide static placeholder images for each complication (used during install, in complication picker)
- Complication image sizes vary per layout; placeholder size may differ from actual image size

## Circular Family

Appears on Infograph, Infograph Modular, and X-Large watch faces. Layouts: Closed gauge image, Closed gauge text, Open gauge image, Open gauge text, Open gauge range, Image, Stack image, Stack text.

Bezel text can accompany a circular image on some faces (e.g., Infograph), curving up to ~180° before truncating.

### Regular-Size Image Dimensions

| Image | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Image | 42×42 pt (84×84 px) | 44.5×44.5 pt (89×89 px) | 47×47 pt (94×94 px) | 50×50 pt (100×100 px) |
| Closed gauge | 27×27 pt (54×54 px) | 28.5×28.5 pt (57×57 px) | 31×31 pt (62×62 px) | 32×32 pt (64×64 px) |
| Open gauge | 11×11 pt (22×22 px) | 11.5×11.5 pt (23×23 px) | 12×12 pt (24×24 px) | 13×13 pt (26×26 px) |
| Stack (not text) | 28×14 pt (56×28 px) | 29.5×15 pt (59×30 px) | 31×16 pt (62×32 px) | 33.5×16.5 pt (67×33 px) |

System applies a circular mask to each image.

**Default text:** Rounded, Medium, 12 pt (40mm) / 12.5 pt (41mm) / 13 pt (44mm) / 14.5 pt (45mm/49mm)

### Extra-Large Image Dimensions (X-Large watch face)

| Image | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Image | 120×120 pt (240×240 px) | 127×127 pt (254×254 px) | 132×132 pt (264×264 px) | 143×143 pt (286×286 px) |
| Open gauge | 31×31 pt (62×62 px) | 33×33 pt (66×66 px) | 33×33 pt (66×66 px) | 37×37 pt (74×74 px) |
| Closed gauge | 77×77 pt (154×154 px) | 81.5×81.5 pt (163×163 px) | 87×87 pt (174×174 px) | 91.5×91.5 pt (183×183 px) |
| Stack | 80×40 pt (160×80 px) | 85×42 pt (170×84 px) | 87×44 pt (174×88 px) | 95×48 pt (190×96 px) |

**Default text (XL):** Rounded, Medium, 34.5 pt (40mm) / 36.5 pt (41mm) / 36.5 pt (44mm) / 41 pt (45mm/49mm)

### Placeholder Image Sizes

| Layout | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Circular | 42×42 pt (84×84 px) | 44.5×44.5 pt (89×89 px) | 47×47 pt (94×94 px) | 50×50 pt (100×100 px) |
| Bezel | 42×42 pt (84×84 px) | 44.5×44.5 pt (89×89 px) | 47×47 pt (94×94 px) | 50×50 pt (100×100 px) |
| Extra Large | 120×120 pt (240×240 px) | 127×127 pt (254×254 px) | 132×132 pt (264×264 px) | 143×143 pt (286×286 px) |

## Corner Family

Displays in corners of watch faces like Infograph. Layouts: Circular image, Gauge image, Gauge text, Stack text, Text image.

### Image Dimensions

| Image | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Circular | 32×32 pt (64×64 px) | 34×34 pt (68×68 px) | 36×36 pt (72×72 px) | 38×38 pt (76×76 px) |
| Gauge | 20×20 pt (40×40 px) | 21×21 pt (42×42 px) | 22×22 pt (44×44 px) | 24×24 pt (48×48 px) |
| Text | 20×20 pt (40×40 px) | 21×21 pt (42×42 px) | 22×22 pt (44×44 px) | 24×24 pt (48×48 px) |

System applies circular mask. Placeholder: same as Gauge/Text sizes.

**Default text:** Rounded, Semibold, 10 pt (40mm) / 10.5 pt (41mm) / 11 pt (44mm) / 12 pt (45mm/49mm)

## Inline Family

### Utilitarian Small
For rectangular corner areas (Chronograph, Simple faces). Layouts: Flat, Ring image, Ring text, Square.

| Content | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Flat | 9–21×9 pt | 10–22×10 pt | 10.5–23.5×21 pt | N/A | 12–26×12 pt |
| Ring | 14×14 pt | 14×14 pt | 15×15 pt | 16×16 pt | 16.5×16.5 pt |
| Square | 20×20 pt | 22×22 pt | 23.5×23.5 pt | 25×25 pt | 26×26 pt |

### Utilitarian Large
Text-based, spans bottom of watch face (Utility, Motion faces). Layout: Large flat.

| Content | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Flat | 9–21×9 pt | 10–22×10 pt | 10.5–23.5×10.5 pt | N/A | 12–26×12 pt |

## Rectangular Family

Large rectangular region for full-color images, text, gauges, and optional titles. Layouts: Standard body, Text gauge, Large image.

Good for information-rich charts, graphs, and diagrams that show changes over time.

**Smart Stack (watchOS 10+):** Rectangular layouts may appear in the Smart Stack. Optimize by:
- Supplying background color/content for recognition
- Using App Intents for relevancy timing
- Creating custom layouts optimized for Smart Stack

### Image Dimensions

| Content | 40mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|
| Large image with title | 150×47 pt (300×94 px) | 159×50 pt (318×100 px) | 171×54 pt (342×108 px) | 178.5×56 pt (357×112 px) |
| Large image without title | 162×69 pt (324×138 px) | 171.5×73 pt (343×146 px) | 184×78 pt (368×156 px) | 193×82 pt (386×164 px) |
| Standard body | 12×12 pt (24×24 px) | 12.5×12.5 pt (25×25 px) | 13.5×13.5 pt (27×27 px) | 14.5×14.5 pt (29×29 px) |
| Text gauge | 12×12 pt (24×24 px) | 12.5×12.5 pt (25×25 px) | 13.5×13.5 pt (27×27 px) | 14.5×14.5 pt (29×29 px) |

Large-image layouts include a 4 pt corner radius.

**Default text:** Rounded, Medium, 16.5 pt (40mm) / 17.5 pt (41mm) / 18 pt (44mm) / 19.5 pt (45mm/49mm)

## Legacy Templates

Nongraphic styles for earlier watchOS versions. Don't take on wearer's selected color.

### Circular Small
Small image or few characters. Appears in watch face corners (e.g., Color face).

| Image | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Ring | 20×20 pt | 22×22 pt | 23.5×23.5 pt | 24×24 pt | 26×26 pt |
| Simple | 16×16 pt | 18×18 pt | 19×19 pt | 20×20 pt | 21.5×21.5 pt |
| Stack | 16×7 pt | 17×8 pt | 18×8.5 pt | 19×9 pt | 19×9.5 pt |
| Placeholder | 16×16 pt | 18×18 pt | 19×19 pt | 20×20 pt | 21.5×21.5 pt |

Stack width = maximum size.

### Modular Small
Two stacked rows with icon/content, circular graph, or single larger item.

| Image | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Ring | 18×18 pt | 19×19 pt | 20×20 pt | 21×21 pt | 22.5×22.5 pt |
| Simple | 26×26 pt | 29×29 pt | 30.5×30.5 pt | 32×32 pt | 34.5×34.5 pt |
| Stack | 26×14 pt | 29×15 pt | 30.5×16 pt | 32×17 pt | 34.5×18 pt |
| Placeholder | 26×26 pt | 29×29 pt | 30.5×30.5 pt | 32×32 pt | 34.5×34.5 pt |

### Modular Large
Up to three rows of content. Layouts: Columns, Standard body, Table, Tall body.

| Content | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| All icons | 11–32×11 pt | 12–37×12 pt | 12.5–39×12.5 pt | 14–42×14 pt | 14.5–44×14.5 pt |

### Extra Large (Legacy)
Larger text/images for X-Large watch faces.

| Image | 38mm | 40mm/42mm | 41mm | 44mm | 45mm/49mm |
|---|---|---|---|---|---|
| Ring | 63×63 pt | 66.5×66.5 pt | 70.5×70.5 pt | 73×73 pt | 79×79 pt |
| Simple | 91×91 pt | 101.5×101.5 pt | 107.5×107.5 pt | 112×112 pt | 121×121 pt |
| Stack | 78×42 pt | 87×45 pt | 92×47.5 pt | 96×51 pt | 103.5×53.5 pt |
| Placeholder | 91×91 pt | 101.5×101.5 pt | 107.5×107.5 pt | 112×112 pt | 121×121 pt |

## Platform

watchOS only. Not supported on iOS, iPadOS, macOS, tvOS, or visionOS.