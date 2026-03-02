# Eyes Input — visionOS

Guidelines for designing eye-based interactions in visionOS, including hover effects, visual comfort, and custom hover behaviors.

## How It Works

- People look at a virtual object to identify it as an interaction target
- visionOS highlights interactive elements with a **hover effect** when looked at, confirming they can be tapped
- The system can auto-display expanded views after gaze (e.g., tab bar resizes to show labels, buttons reveal tooltips)
- **Privacy**: visionOS doesn't provide direct info about where people look before they tap. System-provided components automatically report taps.
- Focus effects (keyboard/game controller navigation) are separate from hover effects — see Focus and Selection

## Best Practices

- **Always provide multiple interaction methods** — support accessibility features
- **Design for visual comfort** — keep needed objects within field of view; avoid requiring multiple quick eye adjustments over large areas or through multiple depth levels
- **Place content at comfortable viewing distance** — at least **1 meter away** for content people read or engage with over time; closer only for brief interactions
- **Prefer standard UI components** — they respond consistently to gaze; custom visual cues are harder to learn

## Making Items Easy to See

- **Minimize visual distractions** — movement in peripheral vision causes involuntary gaze shifts; avoid revealing content near a button people are looking at
- **Provide enough space around items** — use a margin of at least **16 points** around each interactive item's bounds, OR place items so their centers are at least **60 points apart**
- **Avoid repeating patterns/textures that fill the field of view** — eyes can lock onto different pattern elements, creating false depth perception; use patterns in smaller areas

## Encouraging Interaction

- Use subtle visual cues to draw attention: center placement, gentle motion, increased contrast, color/scale variation — noticeable but not flashy
- **Give interactive items a rounded shape** — eyes are drawn to corners, making it hard to target a shape's center. More rounded = easier to target
- For multi-element interactive components, **define a custom containing shape** that encompasses all elements so visionOS highlights the entire region

## Custom Hover Effects

Custom hover effects animate in a custom way when people look at an element (UI elements or RealityKit entities). Can replace or augment standard effects.

### How Custom Hover Effects Work

- You define **two states**: one with the hover effect, one without
- The system applies the effect **out of process** — you don't know when it's applied or what state the element is in
- The effect **cannot run code** that requires knowing when people are looking
- Example: A photo app can specify a favorites symbol for a hover effect, but the hover effect can't perform the favoriting action

### Custom Hover Effect Guidelines

- **Use sparingly** to emphasize special moments — overuse dilutes impact and can cause visual discomfort
- **Choose the right delay:**
  - **No delay (default)**: Best for subtle effects or interaction invitations (e.g., knob appearing on slider)
  - **Short delay**: Lets people look and quickly interact without waiting (e.g., tab bar expansion)
  - **Long delay**: Good for additional info like tooltips — most people won't need it every time
- **Keep one or more primary views unchanged** between both states — provides visual stability during animation; changing everything disorients users
- **Test on Apple Vision Pro** — only way to verify effects look good, respond well, and don't distract

## Platform Support

visionOS only. Not supported in iOS, iPadOS, macOS, tvOS, or watchOS.