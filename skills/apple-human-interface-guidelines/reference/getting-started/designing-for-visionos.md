# Designing for visionOS

Guidelines for designing apps and games for Apple Vision Pro's spatial computing environment.

## Fundamental Concepts

- **Space**: Limitless canvas for windows, volumes, and 3D objects; supports deeply immersive experiences
- **Immersion**: Fluid transitions between levels — *Shared Space* (multiple apps side-by-side) and *Full Space* (single app with 3D content blended with surroundings, portals, or full worlds)
- **Passthrough**: Live video from external cameras; people control amount via Digital Crown
- **Spatial Audio**: Automatically models sonic characteristics of surroundings; can be fine-tuned with surroundings permission
- **Eyes and Hands**: Primary input is eyes (look at object) + indirect gesture (tap to activate); also supports direct gestures (touching with finger)
- **Ergonomics**: System places content relative to wearer's head regardless of posture; content comes to people rather than requiring movement
- **Accessibility**: Supports VoiceOver, Switch Control, Dwell Control, Guided Access, Head Pointer; system UI components have built-in accessibility

## Best Practices

- **Embrace unique features**: Use space, Spatial Audio, and immersion; integrate passthrough and spatial input naturally
- **Choose minimum immersion level**: For each key moment, find the minimum level that suits it — don't assume everything needs full immersion. Options: windowed/UI-centric, fully immersive, or in between
- **Use windows for standard tasks**: Standard windows appear as planes in space with familiar controls; people can relocate them; dynamic scaling keeps content legible at any distance

### Comfort Guidelines

- Display content within the person's field of view, positioned relative to their head
- **Don't** place content where people must turn their head or change position to interact
- **Avoid** overwhelming, jarring, or too-fast motion; always provide a stationary frame of reference
- **Support indirect gestures** so people can interact with hands resting in lap or at sides
- For direct gestures, keep interactive content within reach and avoid extended interaction periods
- **Avoid** encouraging excessive movement during fully immersive experiences

### Shared Experiences

- Use SharePlay to support shared activities with spatial Personas, making participants feel present in the same space