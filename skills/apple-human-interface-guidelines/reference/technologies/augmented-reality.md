# Augmented Reality Design Guidelines

Guidelines for designing AR experiences that blend virtual objects with the real world using ARKit on iOS/iPadOS and visionOS.

## Best Practices

- **Use the entire display** — Devote as much screen as possible to the physical world and virtual objects. Minimize controls and overlays.
- **Create convincing illusions** — Use detailed 3D assets with lifelike textures. Scale objects properly, position on detected surfaces, reflect environmental lighting, simulate camera grain, cast diffuse shadows, and update visuals as camera moves. **Update scenes at 60fps** to prevent jumping/flickering.
- **Reflective surfaces** — Reflections are approximations. Prefer small or coarse reflective surfaces to downplay inaccuracies.
- **Use audio and haptics** — Sound effects and haptic feedback confirm virtual-physical interactions. Background music enhances immersion.
- **Minimize text in the environment** — Show only essential information.
- **Use screen space for additional info/controls** — Screen-space content stays fixed while AR environment moves with the device.
- **Indirect controls** — For persistent controls, use 2D controls in screen space. Place them so users don't have to adjust grip. Consider translucency to avoid blocking the scene.
- **Design for varied environments** — Communicate requirements up front (space, surfaces). Offer different feature sets for different environments.
- **Consider comfort** — Holding a device at angles is fatiguing. Place objects to reduce need for movement; keep game levels short with downtime.
- **Introduce motion gradually** — Give people time to adapt before encouraging movement.
- **Prioritize safety** — Avoid encouraging large or sudden movements since users may not be aware of physical surroundings.

## Coaching

- Use the **built-in coaching view** (`ARCoachingOverlayView`) to guide surface detection during initialization and relocalization.
- **Hide unnecessary UI** while coaching view is active.
- If the system coaching view doesn't meet your needs, design a **custom coaching experience** using the system view as reference.

## Helping People Place Objects

- Use coaching view to help find horizontal/vertical surfaces; display a **custom visual indicator** aligned with the detected plane when placement is possible.
- **Place objects immediately** on detected surfaces — don't wait for perfect accuracy. Subtly refine position as detection completes (use `ARTrackedRaycast`).
- **Guide to offscreen objects** — Use visual or audible cues (e.g., indicator on screen edge).
- **Don't align to surface edges precisely** — Surface boundaries are approximations that change over time.
- **Use plane classification** — e.g., only allow furniture on "floor" planes, game boards on "table" planes.

## Object Interactions

- **Prefer direct manipulation** (touching 3D objects directly) over indirect controls. Use indirect controls when users are moving around.
- **Use standard gestures** — Single-finger drag to move, two-finger rotation to spin.
- **Keep interactions simple** for the 2D-to-3D translation:
  - Limit movement to the 2D surface the object rests on
  - Limit rotation to a single axis
- **Be forgiving with gesture targeting** — When a gesture is near an interactive object, assume the user wants to affect it.
- **Allow scaling only when contextually appropriate** — Don't use scaling to simulate distance changes (enlarging a distant object makes it look larger, not closer).
- **Watch for gesture conflicts** — Test that similar gestures (e.g., pinch vs. rotation) are interpreted correctly.
- **Respect physics** — Keep objects on surfaces during movement; don't let them jump, vanish, or reappear.
- **Explore beyond gestures** — Use motion, proximity, and other inputs (e.g., a character turning to look at an approaching user).

## Multiuser Experience

- Participants map environments independently; ARKit merges maps automatically (`isCollaborationEnabled`).
- **Support people occlusion** — Let real people occlude virtual objects for realism.
- **Allow late joiners** — Use implicit map merging unless all participants must join before start.

## Reacting to Real-World Objects

- Provide 2D reference images or 3D reference objects; ARKit detects them in the environment.
- **Delay removal of virtual objects** when a detected image disappears — wait up to 1 second before fading out to prevent flickering.
- **Limit active reference images to ≤100** for best performance. Change the active set based on context (e.g., location in a museum).
- **Limit tracked images** (position-updated) since they require more resources. Use tracking only when the image may move or has small attached animations.

## Communicating with People

Use approachable, non-technical language:

| Do | Don't |
|---|---|
| Unable to find a surface. Try moving to the side or repositioning your phone. | Unable to find a plane. Adjust tracking. |
| Tap a location to place the [object name]. | Tap a plane to anchor an object. |
| Try turning on more lights and moving around. | Insufficient features. |
| Try moving your phone more slowly. | Excessive motion detected. |

- **Prefer 3D hints in 3D contexts** (e.g., 3D rotation indicator around an object) over 2D text overlays.
- **Make text readable** — Use screen space for critical labels/annotations. In 3D space, face text toward the user with consistent type size regardless of distance.
- **Provide tap-for-more indicators** when additional information is available.

## Handling Interruptions

- After interruptions (app switching, phone calls), virtual objects may appear in wrong positions. Support **relocalization** to restore positions.
- Use the **coaching view during relocalization** to guide users back to the previous position/orientation.
- **Hide virtual objects during relocalization** to avoid flickering.
- **Minimize interruptions** — Embed non-AR tasks within the AR experience (e.g., changing upholstery without leaving AR).
- **Allow canceling relocalization** — Provide a reset button if relocalization fails.
- **Indicate face tracking loss** after ~0.5 seconds with a visual indicator (front-facing camera).

## Problem Resolution

- **Let people reset** the experience if it doesn't meet expectations.
- **Suggest fixes** using friendly language:

| Problem | Suggestion |
|---|---|
| Insufficient features detected | Try turning on more lights and moving around. |
| Excessive motion detected | Try moving your phone slower. |
| Surface detection takes too long | Try moving around, turning on more lights, and point at a textured surface. |

## AR Icons and Badges

- Use the **AR glyph** only for initiating ARKit-based experiences. Don't alter it (except size/color) or use for non-ARKit experiences.
- **Minimum clear space**: 10% of glyph height around the AR glyph.
- **AR badge vs glyph-only badge**: Prefer the full AR badge; use glyph-only in constrained spaces.
- **Use badges only** when the app has a mix of AR-viewable and non-AR objects. If all objects support AR, badges are redundant.
- **Consistent badge placement** — Always in the same corner of an object's photo, clearly visible but not occluding important detail.
- **Badge clear space**: 10% of badge height.
- Never alter badges, change their color, or use for non-ARKit experiences.

## visionOS

With permission, ARKit in visionOS can:
- Detect surfaces in surroundings
- Use hand/finger positions for custom gestures
- Support interactions incorporating nearby physical objects into immersive experiences

## Device Capability

- **Offer AR only on capable devices** — If AR is primary, require ARKit support. If AR is optional, silently hide the feature on unsupported devices (don't show errors).