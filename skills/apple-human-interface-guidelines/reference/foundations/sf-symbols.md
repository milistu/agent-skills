# SF Symbols

Guidelines for using SF Symbols — thousands of configurable symbols that integrate with the San Francisco system font, aligning with text in all weights and sizes.

Use symbols to convey objects or concepts in toolbars, tab bars, context menus, and within text. Availability varies by OS version — symbols introduced in a given year aren't available in earlier systems.

**Important:** SF Symbols cannot be used in app icons, logos, or any other trademarked use. Symbols depicting Apple products are copyrighted and can't be customized.

## Rendering Modes

Four rendering modes control how color is applied. Symbols organize paths into distinct layers (primary, secondary, tertiary).

| Mode | Description |
|------|-------------|
| **Monochrome** | Applies one color to all layers. Paths render in the specified color or as transparent shapes within color-filled paths. |
| **Hierarchical** | Applies one color to all layers, varying opacity by hierarchical level. |
| **Palette** | Applies 2+ colors, one per layer. Two colors for a 3-layer symbol means secondary and tertiary share a color. |
| **Multicolor** | Applies intrinsic colors to enhance meaning (e.g., green for `leaf`, red for `trash.slash`). Some layers can receive custom colors. |

- Use system-provided colors to ensure symbols adapt to accessibility accommodations, vibrancy, and Dark Mode.
- Confirm rendering mode works well in every context — different modes affect legibility depending on size and background contrast.
- Use the `automatic` setting to get a symbol's preferred rendering mode, but verify results.

**Developer APIs:** `renderingMode(_:)` (SwiftUI), `UIImage.SymbolScale` (UIKit).

## Gradients

Available in SF Symbols 7+. Generates a smooth linear gradient from a single source color. Works across all rendering modes, system/custom colors, and custom symbols. Looks best at larger sizes.

## Variable Color

Represents characteristics that change over time (capacity, strength) by applying color to different layers as a value moves between 0–100%.

Example: `speaker.wave.3` — three wave layers map to different decibel ranges. The speaker layer itself opts out of variable color since it doesn't change.

- **Use variable color to communicate change** — don't use it to communicate depth.
- For depth and visual hierarchy, use Hierarchical rendering mode instead.

## Weights and Scales

**9 weights:** ultralight, thin, light, regular, medium, semibold, bold, heavy, black — each corresponds to a San Francisco font weight.

**3 scales:** small, medium (default), large — defined relative to the cap height of San Francisco.

Specifying a scale adjusts symbol emphasis compared to adjacent text without disrupting weight matching.

**Developer APIs:** `imageScale(_:)` (SwiftUI), `UIImage.SymbolScale` (UIKit), `NSImage.SymbolConfiguration` (AppKit).

## Design Variants

| Variant | Use Case |
|---------|----------|
| **Outline** | Default. No solid areas. Works well in toolbars, lists, alongside text. |
| **Fill** | Solid areas within shapes. More visual emphasis. Good for iOS tab bars, swipe actions, selection states. |
| **Slash** | Shows item/action is unavailable. |
| **Enclosed** (circle, square, rectangle) | Improves legibility at small sizes. |

Variants can combine (e.g., enclosed + fill, slash + outline).

Language/script-specific variants (Latin, Arabic, Hebrew, Hindi, Thai, CJK, Cyrillic, etc.) adapt automatically when the device language changes.

Many views auto-select the variant: iOS tab bar prefers fill; toolbar prefers outline.

## Animations

Expressive, configurable animations for all SF Symbols, all rendering modes, weights, scales, and custom symbols.

| Animation | Behavior | Use Case |
|-----------|----------|----------|
| **Appear** | Symbol gradually emerges into view | Introducing elements |
| **Disappear** | Symbol gradually recedes from view | Removing elements |
| **Bounce** | Brief elastic scale up/down, returns to initial state (plays once by default) | Communicating an action occurred or needs to happen |
| **Scale** | Changes symbol size; persists until reset | Drawing attention to selection, feedback on interaction |
| **Pulse** | Varies opacity over time on annotated layers | Ongoing activity |
| **Variable Color** | Incrementally varies layer opacity (cumulative or iterative; open/closed loop) | Progress, connectivity, broadcasting |
| **Replace** | Transitions between two symbols. Configs: **down-up** (state change), **up-up** (forward progression), **off-up** (emphasize next state) | State changes |
| **Magic Replace** | Smart transition between related symbols (slashes, badges). Falls back to down-up for unrelated symbols. Default replace animation. | Related state changes |
| **Wiggle** | Moves along a directional axis | Highlighting changes, calls to action, directional emphasis |
| **Breathe** | Smooth increases/decreases in opacity and size | Status changes, ongoing activity (e.g., recording) |
| **Rotate** | Rotates entire symbol or specific layers | Task in progress, visual indicators |
| **Draw On / Draw Off** | (SF Symbols 7+) Draws symbol along a path. Layers can animate all at once, staggered, or one at a time. | Progress, reinforcing meaning |

### Animation Best Practices

- Apply animations judiciously — too many overwhelm the interface.
- Ensure animations serve a clear purpose in communicating intent.
- Use animations to present complex information simply without taking up visual space.
- Consider your app's tone and brand identity when choosing animations.

**Developer APIs:** `SymbolEffect` (Symbols framework).

## Custom Symbols

Create custom symbols by exporting a template for a similar system symbol, then modifying it in a vector editor.

### Design Guidelines

- Use the template as a guide for detail level, optical weight, alignment, position, and perspective.
- Design symbols that are **simple, recognizable, inclusive**, and directly related to the action/content they represent.
- Don't design replicas of Apple products.
- Don't create custom symbols that include common variants (enclosures, badges) — use the SF Symbols app component library instead.

### Technical Considerations

- **Annotating:** Assign specific colors or hierarchical levels (primary/secondary/tertiary) to each layer.
- **Negative side margins:** Supported for optical horizontal alignment when symbols include badges or extra-width elements. Use naming pattern like "left-margin-Regular-M".
- **Animation optimization:** Annotate layers in the SF Symbols app. Z-order determines variable color application order (front-to-back or back-to-front). Use layer groups for related layers to move together.
- **Testing animations:** Test with all animation presets. Draw custom symbols with whole shapes rather than cutouts. Use erase layers to render gaps (e.g., for `person.2.fill`-style overlapping shapes).
- **Accessibility:** Provide alternative text labels (accessibility descriptions) for VoiceOver support.