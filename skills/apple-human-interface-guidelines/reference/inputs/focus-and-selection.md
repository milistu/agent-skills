# Focus and Selection

Guidelines for implementing focus-based navigation across Apple platforms. Focus helps people visually confirm the object their interaction targets.

## Best Practices

- **Rely on system-provided focus effects.** System-defined effects are tuned for Apple devices. Only create custom focus effects if absolutely necessary.
- **Avoid changing focus without people's interaction.** Exception: when a previously focused item disappears during directional navigation (keyboard/remote/game controller), move focus to a nearby remaining item. When people aren't using such an input device, simply hide the focus indicator when the focused object disappears.
- **Be consistent with platform conventions:**
  - iPadOS/macOS: Support focus for content elements (list items, text fields, search fields), not controls (buttons, sliders, toggles) — full keyboard access handles those.
  - tvOS: Every onscreen element must be focusable via directional gestures.
- **Use platform-consistent visual focus indicators:**
  - iPadOS/macOS: Focused list items use white text + accent-color background highlight; unfocused items use standard text + gray background.
- **Use focus rings for text/search fields; use highlights in lists/collections.** Highlighting entire rows is easier to scan than focus rings on individual cells.

## Platform Considerations

**Not supported in iOS or watchOS.**

### iPadOS

iPadOS 15+ defines a focus system supporting keyboard navigation for text fields, text views, sidebars, and collection views.

**Focus Groups vs Directional Focus:**
- **Tab key** moves focus among focus groups (sidebars, grids, app areas)
- **Arrow keys** move focus among items within the same focus group (directional, similar to tvOS)

**Focus Indicators:**

| Type | Usage |
|------|-------|
| **Halo (focus ring)** | Customizable outline around a component. Apply to custom views and opaque content in collection/list cells (e.g., images). |
| **Highlighted appearance** | Text uses app's accent color. Occurs automatically on collection view cells with content configurations. Not a focus effect per se. |

**Halo Customization:**
- System infers halo shape from item shape by default
- Refine to match rounded corners or Bézier paths
- Adjust position if another component occludes or clips it (e.g., badges above halo, parent view clipping)
- See `UIFocusHaloEffect`

**Focus Group Guidance:**
- Focus moves through groups in reading order (leading→trailing, top→bottom)
- Adjust custom view focus order by identifying stack containers as single focus groups via `focusGroupIdentifier`
- Set primary item in a group via `UIFocusGroupPriority` so it auto-receives focus when the group is focused

### tvOS

**Key Guidelines:**
- In full-screen experiences, let gestures interact with content, not move focus
- Avoid displaying a pointer — use the focus model for menus and UI; pointers only during gameplay if needed
- Design for components in various focus states — focused items often scale up, so supply assets for larger sizes and ensure they don't crowd surrounding UI

**Five Focus States:**

| State | Description |
|-------|-------------|
| **Unfocused** | Less prominent; small drop shadow, translucent background infused by nearby colors, high-contrast text |
| **Focused** | Visually stands out via elevation, illumination, and animation; larger with more shadow, opaque white background, black text |
| **Highlighted** | Instant visual feedback when chosen (e.g., brief color inversion); same size as unfocused, opaque white background |
| **Selected** | Indicates activation (e.g., filled heart icon); same size as unfocused, opaque white background |
| **Unavailable** | Can't receive focus; no drop shadow, translucent tinted background, low-contrast text |

### visionOS

visionOS supports the same focus system as iPadOS/tvOS for connected input devices (keyboard, game controller).

**Important:** When people look at a virtual object, the system uses the **hover effect** (not a focus effect) for visual feedback. The hover effect is separate from the focus system. See [Eyes](/design/human-interface-guidelines/eyes) for guidance.