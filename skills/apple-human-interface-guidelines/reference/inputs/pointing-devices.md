# Pointing Devices

Guidelines for designing pointer/mouse/trackpad interactions across Apple platforms.

## Best Practices

- **Be consistent** when responding to mouse and trackpad gestures — people expect most gestures to work the same throughout the system.
- **Don't redefine systemwide trackpad gestures.** Even in games, keep system gestures (Dock, Mission Control) available.
- **Provide a consistent experience** whether people use gestures, eyes, a pointing device, or keyboard. People move fluidly between input types.
- **Let people use the pointer to reveal/hide auto-minimizing controls** (e.g., Safari toolbar in iPadOS).
- **Modifier key consistency:** If Option+drag duplicates an object, ensure the result is the same whether dragging with touch or pointer.

## iPadOS

iPadOS adapts the pointer to context, providing rich visual feedback. The pointer system supplements touch — it doesn't replace it.

- **Support click-and-drag multiple selection** in custom views (iPadOS 15+). Standard collection views support this by default. See `UIBandSelectionInteraction`.
- **Distinguish pointer vs. finger input only when it adds value** (e.g., precise scrubber seek with pointer).

### Pointer Shape and Content Effects

Default pointer shape is a circle. It changes shape contextually (e.g., I-beam over text fields).

**Three content effects:**

| Effect | Behavior | Default Usage |
|---|---|---|
| **Highlight** | Pointer transforms into translucent rounded rectangle background with parallax | Bar buttons, tab bars, segmented controls, edit menus |
| **Lift** | Element scales up with shadow below and specular highlight; pointer fades beneath | App icons, Control Center buttons |
| **Hover** | Custom scale, tint, or shadow values; pointer retains default shape | Custom elements |

**When to use each effect:**
- **Highlight**: Small element with transparent background
- **Lift**: Small element with opaque background
- **Hover**: Large elements — customize scale, tint, shadow as needed

### Pointer Accessories

Visual indicators showing how people can interact (e.g., resize arrows). See `UIPointerAccessory`.

- Use **clear, simple images** — accessories are small.
- Use **accessory transitions** to signal state changes (e.g., `plus` → `circle.slash`).

### Pointer Magnetism

Elements appear to attract the pointer. The system starts transforming the pointer when it reaches the element's hit region (which extends beyond visible boundaries).

- **Applied by default** to lift and highlight effects.
- **Not applied** to hover effects (would feel jarring since hover doesn't transform the pointer).
- Also applied to text-entry areas to prevent line-skipping during selection.

### Hit Region Padding

| Element Type | Recommended Padding |
|---|---|
| Elements with bezel | ~12 points around edges |
| Elements without bezel / glyphs | ~24 points around visible edges |

- **Create contiguous hit regions** for adjacent bar buttons to avoid distracting pointer shape reversion between buttons.
- **Specify corner radius** for non-standard elements using lift effect. See `UIPointerShape.roundedRect(_:radius:)`.

### Customizing Pointers

- Prefer **system-provided effects** for elements that behave like standard ones.
- Use pointer effects **consistently** throughout your app.
- **Avoid gratuitous effects** — changes should be useful, not decorative.
- Keep **custom shapes simple** — shape should signal action without drawing excessive attention.
- Consider **custom annotations** (e.g., X/Y values over a graph, width/height during resize).
- **Avoid instructional text** on pointers.
- **Hover effect considerations:**
  - Reserve scaling for elements with room to expand (not table rows).
  - For tight spacing, use tint without scale/shadow.
  - Don't use shadow without scale (unscaled element with shadow looks wrong).

## macOS

### Standard Mouse & Trackpad Interactions

| Click/Gesture | Behavior | Mouse | Trackpad |
|---|---|:---:|:---:|
| Primary click | Select/activate | ● | ● |
| Secondary click | Contextual menus | ● | ● |
| Scrolling | Move content | ● | ● |
| Smart zoom | Zoom in/out on content | ● | ● |
| Swipe between pages | Navigate forward/back | ● | ● |
| Swipe between full-screen apps | Navigate between apps/spaces | ● | ● |
| Mission Control | Activate Mission Control | ● | ● |
| Lookup/data detectors | Display lookup window | | ● |
| Tap to click | Primary click via tap | | ● |
| Force click | Quick Look / pressure-sensitive controls | | ● |
| Pinch zoom | Zoom in/out | | ● |
| Rotate (two fingers circular) | Rotate content | | ● |
| Notification Center (edge swipe) | Show Notification Center | | ● |
| App Exposé (3-4 finger swipe down) | Show app windows | | ● |
| Launchpad (pinch thumb + 3 fingers) | Show Launchpad | | ● |
| Show Desktop (spread thumb + 3 fingers) | Reveal desktop | | ● |

### Standard macOS Pointer Styles

| Name | Meaning | AppKit API |
|---|---|---|
| Arrow | Standard selection/interaction | `NSCursor.arrow` |
| Closed hand | Dragging to reposition content | `NSCursor.closedHand` |
| Contextual menu | Context menu available (Control key) | `NSCursor.contextualMenu` |
| Crosshair | Precise rectangular selection | `NSCursor.crosshair` |
| Disappearing item | Dragged item will disappear on drop | `NSCursor.disappearingItem` |
| Drag copy | Duplicate item on drop (Option key) | `NSCursor.dragCopy` |
| Drag link | Create alias on drop (Option+Command) | `NSCursor.dragLink` |
| Horizontal I-beam | Text selection/insertion (horizontal) | `NSCursor.iBeam` |
| Open hand | Content dragging possible | `NSCursor.openHand` |
| Operation not allowed | Drop not possible here | `NSCursor.operationNotAllowed` |
| Pointing hand | URL link | `NSCursor.pointingHand` |
| Resize down | Resize/move downward | `NSCursor.resizeDown` |
| Resize left | Resize/move left | `NSCursor.resizeLeft` |
| Resize left/right | Resize/move horizontally | `NSCursor.resizeLeftRight` |
| Resize right | Resize/move right | `NSCursor.resizeRight` |
| Resize up | Resize/move upward | `NSCursor.resizeUp` |
| Resize up/down | Resize/move vertically | `NSCursor.resizeUpDown` |
| Vertical I-beam | Text selection (vertical layout) | `NSCursor.iBeamCursorForVerticalLayout` |

## visionOS

- People can attach external pointing devices and keyboards alongside eyes and hands.
- Looking at an element then moving the pointer brings focus to the element under the pointer — apps get this automatically.
- The area people are looking at determines the pointer's context; shifting eyes between windows transitions the pointer context.
- Pointer hides during gestures to minimize distraction; reappears at gaze location when moved again.