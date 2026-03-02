# Maps Design Guidelines

Guidelines for displaying outdoor or indoor geographical data using MapKit across Apple platforms.

## Best Practices

- **Make maps interactive.** People expect to zoom, pan, and interact with maps. Avoid noninteractive elements that obscure the map.
- **Pick an emphasis style:**
  - *Default* — fully saturated colors; good for standard map apps and visual alignment with Apple Maps
  - *Muted* — desaturated colors; ideal when you have information-rich content that should stand out against the map
- **Offer search and filtering.** Help people find places by combining search with category filters.
- **Clearly identify selected elements.** Use distinct styling like outlines and color variation for selections.
- **Cluster overlapping points of interest.** Use a single pin to represent multiple nearby POIs; expand clusters as users zoom in.
- **Keep the Apple logo and legal link visible:**
  - Use 7pt side padding, 10pt top/bottom padding
  - Don't make the logo/link move with your interface
  - If a custom element (e.g., pull-up card) moves, place logo/link 10pt above the lowest resting position
  - Logo and legal link are hidden on maps smaller than 200×100px

## Custom Information

### Annotations
- Default annotation: red tint, white pin icon
- Customize tint to match your app's color scheme
- Icons can be strings (including Unicode) or images; keep strings to 2–3 characters
- See `MKAnnotationView`

### Selectable Map Features
- Support selectable map features so Apple-provided features (POIs, territories, physical features) are independently selectable from your custom annotations
- Configure custom appearances for these features when selected
- See `MKMapFeatureOptions`

### Overlays
- *Above roads* (default): overlay above roads but below buildings/trees — good when you want people to see what's beneath
- *Above labels*: overlay above roads and labels, hiding everything beneath — for fully abstracted content or hiding irrelevant areas
- See `MKOverlayLevel`

### Custom Controls
- Ensure enough contrast between custom controls and the map
- Consider thin strokes, light drop shadows, or blend modes on the map area

## Place Cards

Place cards display rich place information (hours, phone, address, etc.).

### Place Card Styles

| Style | Description |
|-------|-------------|
| **Automatic** | System determines style based on map view size |
| **Full callout** | Large, detailed popover (popover on iPadOS/macOS, sheet on iOS) |
| **Compact callout** | Space-saving, concise popover |
| **Caption** | "Open in Apple Maps" link only |
| **Sheet** | Place card in a sheet |

### Place Card Best Practices
- **Match style to map context.** Full callout is richest but may be too large for small maps with many annotations — consider compact callout instead.
- **Test across devices and window sizes.** Set minimum width for full callout cards to prevent text overflow on small devices.
- **Avoid duplicating information** already shown in your app.
- **Keep location visible** when displaying a place card. Use offset distance to point the card to the selected location.

### Place Cards Outside Maps
- You can display place cards outside a map (e.g., in search results or store locators)
- **If not in a map view, you must include a map in the place card**
- Use location-related cues (place names, addresses, map pin icons) to indicate interactivity

## Indoor Maps

For venues like malls and stadiums with custom interactive maps.

- **Adjust detail by zoom level.** Show large areas (rooms, buildings) at all levels; reveal detailed features (stores, restrooms) when zoomed in.
- **Use distinctive styling** (color + icons) to differentiate feature types.
- **Offer a floor picker** for multi-level venues; keep floor numbers concise.
- **Include surrounding areas** for context (streets, parking); dim noninteractive areas with distinct color.
- **Support navigation** to/from nearby transit points (bus stops, parking, train stations).
- **Limit scrolling outside venue** — keep at least part of indoor map visible; adjust scroll limits based on zoom level.
- **Design as a natural extension of your app** — don't replicate Apple Maps appearance; match your app's visual style. Follow [Indoor Mapping Data Format (IMDF)](https://register.apple.com/resources/imdf/).

## watchOS

- Maps are **static snapshots** — tapping opens the Maps app
- Maximum **5 annotations** per map
- **Fit map to screen** without requiring scrolling
- **Show smallest region** encompassing all POIs (content doesn't scroll)
- See `WKInterfaceMap`