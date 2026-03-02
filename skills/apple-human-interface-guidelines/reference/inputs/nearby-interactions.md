# Nearby Interactions

Design guidelines for on-device experiences that integrate the presence of people and objects in the nearby environment using Ultra Wideband technology.

## Best Practices

- **Root tasks in the physical world.** Find physical actions that inform the concept of a task (e.g., bringing devices close together to transfer audio) to make interactions feel natural.
- **Use distance, direction, and context to inform interactions.** Prioritize nearby, contextually relevant information for organic experiences. Combine on-device knowledge (frequent contacts) with U1 chip proximity data.
- **Mirror physical-world perception with distance changes.** Feedback should sharpen as users get closer to an object (e.g., Find My transitions from a directional arrow to a pulsing circle as proximity increases).
- **Provide continuous feedback.** Reflect the dynamism of the physical world with uninterrupted updates that respond to user movements (direction + proximity).
- **Use multiple feedback types.** Fluidly transition among visual, audible, and haptic feedback based on context:
  - Screen interaction → visual feedback
  - Environment interaction → audible and haptic feedback
- **Never make nearby interaction the only way to perform a task.** Always provide alternative methods since not everyone can experience nearby interactions.

## Device Usage

- **Encourage portrait orientation.** Landscape decreases accuracy and availability of distance/direction data. Prefer implicit visual cues over explicit instructions to hold in portrait.
- **Design for the device's directional field of view.** The hardware sensor has a field of view similar to the Ultra Wide camera (iPhone 11+). Devices outside this FOV may report distance but not direction.
- **Communicate effects of intervening objects.** People, animals, or large objects between devices decrease accuracy/availability of distance and direction info. Consider addressing this in onboarding or tutorials.

## Platform Considerations

| Platform | Capabilities |
|---|---|
| **iOS (iPhone)** | Distance and direction of peer devices |
| **watchOS** | Distance only; all participating apps must be in the foreground |
| **iPadOS** | No additional considerations |
| **macOS, tvOS, visionOS** | Not supported |