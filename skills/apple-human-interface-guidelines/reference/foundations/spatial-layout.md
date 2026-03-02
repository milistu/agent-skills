# Spatial Layout (visionOS)

Guidelines for laying out content in Apple Vision Pro's 3D spatial environment, covering field of view, depth, scale, and interaction best practices.

## Field of View

A person's field of view is the space they can see without moving their head. Dimensions vary based on Light Seal configuration and peripheral acuity.

> **Important:** The system doesn't provide information about a person's field of view.

- **Center important content within the field of view.** visionOS launches apps directly in front of people. In immersive experiences, keep important content centered; avoid distracting motion or bright, high-contrast objects in the periphery.
- **Avoid anchoring content to the wearer's head.** Head-locked content feels confining and uncomfortable, especially when it obscures passthrough and decreases apparent stability. Instead, anchor content in the person's space so they can look around naturally.

## Depth

The system automatically uses color temperature, reflections, and shadow to convey depth of virtual content. These effects update as objects or the viewer moves.

- Incorporating small amounts of depth even in standard windows makes content look more natural.
- SwiftUI automatically adds depth visual effects to views in 2D windows.
- For additional depth, use RealityKit to create 3D objects. Display them freely or within a **volume** (a window-like container without a visible frame).

### Depth Guidelines

- **Provide visual cues that accurately communicate depth.** Missing or conflicting depth cues cause visual discomfort.
- **Use depth to communicate hierarchy.** Depth makes objects stand out (e.g., a sheet appearing over a window causes the window to recede on the z-axis).
- **Avoid adding depth to text.** Text hovering above its background is hard to read and can cause vision discomfort.
- **Make sure depth adds value.** Use depth to clarify and delight, not everywhere. Good for separating large elements (tab bars, toolbars from windows), but not ideal for small objects (e.g., making a button symbol stand out from its background reduces legibility). Too many depth changes force frequent refocusing, which is tiring.

## Scale

visionOS defines two types of scale:

### Dynamic Scale
- Content automatically increases in scale as it moves away from the wearer and decreases as it moves closer.
- The window appears to maintain the same size at all distances.
- Used by default for windows.

### Fixed Scale
- Object maintains the same scale regardless of distance.
- Appears smaller when farther away (mimics real-world perception).
- **Use fixed scale when a virtual object should look exactly like a physical object** (e.g., life-size product visualization).
- Apply sparingly — reserve for noninteractive objects. Interactive content needs dynamic scaling for usability.

> In visionOS, a **point** is defined as an angle (not a pixel count), supporting dynamic scaling and depth appearance.

## Best Practices

- **Avoid displaying too many windows.** Excessive windows obscure surroundings, cause overwhelm, and make relocation cumbersome.
- **Prioritize indirect gestures.** Indirect gestures don't require moving hands into the field of view. Direct gestures (touching virtual objects) are tiring, especially at or above eye level. Reserve direct gestures for nearby objects that invite close inspection for short periods.
- **Digital Crown recentering.** People can press the Digital Crown to recenter content in front of them. Your app doesn't need to do anything to support this.
- **Space around interactive components.** visionOS displays a hover effect when people look at an interactive element. Ensure enough spacing so hover effects don't crowd other content:
  - Place regular-size buttons with centers **at least 60 points apart**
  - Leave **16 points or more** of space between buttons
  - Don't let controls overlap other interactive elements or views
- **Minimize required physical movement.** Unless physical movement is essential, let people use your app while stationary.
- **Use the floor for large immersive experiences.** Place content extending up from the floor using a flat horizontal plane aligned with the floor for seamless blending with surroundings.