# Materials

Guidelines for using materials (Liquid Glass and standard materials) to create depth, layering, and hierarchy between foreground and background elements across Apple platforms.

## Liquid Glass

Liquid Glass forms a distinct functional layer for controls and navigation (tab bars, sidebars) that floats above the content layer.

### Key Rules

- **Don't use Liquid Glass in the content layer.** It belongs on controls and navigation, not content. Exception: transient interactive elements like sliders and toggles take on Liquid Glass when activated.
- **Use Liquid Glass sparingly.** Standard system components get this automatically. Limit custom usage to the most important functional elements.
- **Only use clear Liquid Glass over visually rich backgrounds.**

### Variants

| Variant | Behavior | Use When |
|---------|----------|----------|
| `regular` | Blurs and adjusts luminosity of background; scroll edge effects enhance legibility | Background content might create legibility issues, or components have significant text (alerts, sidebars, popovers) |
| `clear` | Highly translucent; prioritizes visibility of underlying content | Components float above media backgrounds (photos, videos) for immersive experience |

### Clear Variant Dimming

- If underlying content is **bright**: add a dark dimming layer at **35% opacity**
- If underlying content is **sufficiently dark**, or using standard AVKit playback controls: no dimming needed

For color guidance, see the Color guidelines (Liquid Glass color section).

## Standard Materials

Use standard materials (blur, vibrancy, blending modes) for visual structure in the content layer beneath Liquid Glass.

### Key Rules

- **Choose materials by semantic meaning**, not apparent color — system settings can change appearance.
- **Use vibrant colors on top of materials** to ensure legibility. System-defined vibrant colors adapt automatically.
- **Thicker (more opaque) materials** → better contrast for text and fine features.
- **Thinner (more translucent) materials** → help people retain context by showing background content.

## Platform Considerations

### iOS / iPadOS

Four standard materials for the content layer:

| Material | Opacity |
|----------|---------|
| `ultraThin` | Most translucent |
| `thin` | Slightly more opaque |
| `regular` | Default |
| `thick` | Most opaque |

**Vibrancy for labels:**
- `label` (default, highest contrast)
- `secondaryLabel`
- `tertiaryLabel`
- `quaternaryLabel` — avoid on `thin` and `ultraThin` materials (too low contrast)

**Vibrancy for fills:**
- `fill` (default)
- `secondaryFill`
- `tertiaryFill`

**Separator:** single default vibrancy value, works on all materials.

### macOS

- Provides several standard materials with designated purposes and vibrant versions of all system colors.
- **Choose when to allow vibrancy** in custom views/controls — test in various contexts.
- **Choose a background blending mode:** behind window or within window (`NSVisualEffectView.BlendingMode`).

### tvOS

Liquid Glass appears in navigation elements and system experiences (Top Shelf, Control Center). Image views and buttons adopt Liquid Glass on focus.

Standard materials for content layer:

| Material | Recommended For |
|----------|-----------------|
| `ultraThin` | Full-screen views requiring light color scheme |
| `thin` | Overlay views partially obscuring content, light scheme |
| `regular` | Overlay views partially obscuring content |
| `thick` | Overlay views partially obscuring content, dark scheme |

### visionOS

Windows use an unmodifiable system material called **glass** that adapts to physical surroundings and virtual content.

- visionOS has **no distinct Dark Mode** — glass adapts automatically to luminance.
- **Prefer translucency over opaque colors** — opacity blocks views, feels constricting.
- Material choices for custom components:
  - `thin` → interactive elements (buttons, selected items)
  - `regular` → visual separation (sidebars, grouped table views)
  - `thick` → dark elements on top of `regular` backgrounds

**Vibrancy values (visionOS):**
- `label` — standard text
- `secondaryLabel` — descriptive text (footnotes, subtitles)
- `tertiaryLabel` — inactive elements, low-legibility text only

### watchOS

- **Use materials to provide context in full-screen modal views.** Material layers orient people and distinguish controls from content.
- **Don't remove or replace default material backgrounds** for modal sheets.