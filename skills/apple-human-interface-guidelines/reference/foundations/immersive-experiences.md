# Immersive Experiences (visionOS)

Guidelines for designing apps and games that extend beyond windows and volumes in visionOS, immersing people in content.

## Shared Space vs Full Space

- **Shared Space**: App runs alongside other experiences; people can switch between them
- **Full Space**: App runs alone, hiding other experiences; supports unbounded 3D content in addition to standard windows and volumes

Apps can transition fluidly between Shared Space and Full Space at any time.

## Immersion and Passthrough

**Passthrough** provides real-time video from external cameras, helping people feel comfortable and connected to surroundings.

- **Digital Crown**: People can press and hold to recenter content, or double-click to briefly hide all content and show passthrough
- **Auto-dimming in `mixed`**: If someone gets too close to a physical object, content dims briefly so they can see surroundings
- **Boundary in `progressive`/`full`**: System defines ~1.5-meter boundary from initial head position. As head approaches boundary, experience fades and passthrough increases. Beyond boundary, immersive visuals are replaced by app icon; restored when wearer returns or recenters via Digital Crown.

## Immersion Styles

| Style | Description | Boundary |
|-------|-------------|----------|
| **Dimmed passthrough** (`SurroundingsEffect`) | Subtly dim or tint passthrough in Shared Space or Full Space. Default tint is black; custom tint colors supported (visionOS 2+). | N/A |
| **`mixed`** | Blend 3D content with passthrough in Full Space. Can request ARKit room layout/physical object data. Auto-dims nearby content when person approaches physical objects. | No fixed boundary |
| **`progressive`** | Custom environment partially replaces passthrough. Digital Crown adjusts immersion within default (120°–360°) or custom range. Supports portrait or landscape orientation. | ~1.5m auto boundary |
| **`full`** | 360° custom environment completely replaces passthrough. | ~1.5m auto boundary |

**Developer APIs**: `ImmersionStyle/automatic`, `ImmersionStyle/mixed`, `ImmersionStyle/progressive`, `ImmersionStyle/full`, `SurroundingsEffect`

## Best Practices

- **Offer multiple ways to use your app** — support accessibility features
- **Prefer launching in Shared Space or `mixed` style** — lets people reference your app while using others; gives them control over when to increase immersion
- **Reserve immersion for meaningful moments** — not every task needs full immersion; let people choose when to go deeper (e.g., Photos: browse in window, expand single photo in Full Space)
- **Use subtle cues for attention** — dimming, tinting, motion, scale, Spatial Audio can guide attention at any immersion level; start subtle, strengthen only when needed
- **Prefer subtle tint colors for passthrough** — avoid bright/dramatic tints that distract and diminish immersion

## Promoting Comfort

- **Place 3D content within field of view** — even though Full Space allows placement anywhere
- **Display motion comfortably** in Full Space to avoid distraction, confusion, or discomfort
- **Choose immersion style matching expected movement** — `progressive`/`full` styles have the 1.5m boundary; if people might need to move beyond it, use `mixed` or transition back to it
- **Don't encourage movement in progressive/full experiences** — some people can't move due to disability or surroundings; let people bring objects to them instead
- **In `mixed`, don't obscure passthrough too much** — if virtual objects substantially block the view, switch to `progressive` or `full`
- **Use ARKit** to blend content with surroundings (requires permission for sensitive data like scene reconstruction, hand positions)

## Transitioning Between Styles

- **Design smooth, predictable transitions** — gentle transitions let people visually track changes; avoid sudden/jarring changes
- **Let people choose when to enter/exit immersion** — provide clear action controls; don't force people into immersion unexpectedly
- **Provide a clear exit control** (e.g., Keynote's "Exit" button in Rehearsal mode) — clarify whether it returns to less immersive context or quits entirely
- **If exiting also quits**, offer controls to pause or save progress first

## Displaying Virtual Hands

In Full Space, apps can request permission to hide real hands and show virtual representations.

- **Match familiar characteristics** — positions and gestures should feel natural
- **Avoid oversized virtual hands** — they block content view, feel clumsy, and seem out of proportion/too close to face
- **On tracking data loss**, fade out virtual hands and reveal real hands; when data returns, fade virtual hands back in

## Creating an Environment

Custom environments partially or completely surround a person in a Full Space.

- **Minimize distracting content** — avoid excessive movement or high-contrast details around primary tasks; use quality/dimming to direct attention
- **Help people distinguish interactive objects** — proximity signals interactability (far = not interactive, close = interactive)
- **Keep animation subtle** — gentle movements (drifting clouds) enrich without distracting; avoid too much movement near field-of-view edges
- **Create expansive environments** — small/restrictive spaces cause discomfort and claustrophobia
- **Use Spatial Audio for atmosphere** — avoid excessive repetition/looping; lower soundscape volume when people play other audio
- **Avoid flat 360° images** — they lack depth/scale; prefer object meshes with lighting and shaders for subtle animations
- **Always provide a ground plane mesh** — prevents floating sensation; improves realism even with 360° images
- **Minimize asset redundancy** — repeated assets/models reduce realism

## Platform Considerations

visionOS only — not supported in iOS, iPadOS, macOS, tvOS, or watchOS.