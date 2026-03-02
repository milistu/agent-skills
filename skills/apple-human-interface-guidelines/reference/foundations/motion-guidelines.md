# Motion Guidelines

Guidelines for using animation and motion in Apple platform apps and games.

## Best Practices

- **Add motion purposefully** — Don't add motion for its own sake. Gratuitous or excessive animation can distract people and cause physical discomfort.
- **Make motion optional** — Never use motion as the only way to communicate important information. Supplement with [haptics](/design/human-interface-guidelines/playing-haptics) and [audio](/design/human-interface-guidelines/playing-audio).

## Providing Feedback

- **Follow people's gestures and expectations** — Feedback motion should be realistic. If someone reveals a view by sliding down, they expect to dismiss it by sliding up, not sideways.
- **Aim for brevity and precision** — Brief, precise feedback animations feel lightweight and unobtrusive, conveying information more effectively than prominent animation.
- **Avoid adding motion to frequently-used UI interactions** — System already provides subtle animations for standard elements. Custom elements generally shouldn't add unnecessary motion to repeated interactions.
- **Let people cancel motion** — Don't force people to wait for animations to complete before they can act, especially for repeated animations.
- **Consider animated SF Symbols** — SF Symbols 5+ supports symbol animations for custom and system symbols.

## Game-Specific Guidance

- **Target 30–60 fps** for smooth, visually appealing experiences on each platform.
- **Use device graphics capabilities** to set good defaults so people can enjoy the game without changing settings first.
- **Let people customize visual settings** to optimize performance or battery life (e.g., power modes when external power is detected).

## Platform Considerations

### visionOS

Motion in visionOS combines with depth to provide essential feedback when people look at interactive elements.

- **Avoid motion at edges of field of view** — Peripheral motion is distracting and can cause discomfort by making people feel like they or their surroundings are moving. If needed, match the object's brightness to surrounding content.
- **Large virtual objects** — If an object fills much of the field of view (occluding passthrough), people perceive it as part of their surroundings. Increase translucency or lower contrast to make movement less disorienting. Keep window sizes fairly small.
- **Use fades to relocate objects** — If movement doesn't communicate useful information, fade out before moving and fade in after.
- **Avoid letting people rotate a virtual world** — Rotation upsets stability sense even when subtle and user-controlled. Use instantaneous directional changes during a quick fade-out instead.
- **Provide a stationary frame of reference** — Motion contained within a non-moving area is easier to handle. If the entire surrounding area moves (e.g., automatic player movement), people can feel unwell.
- **Avoid sustained oscillation** — Especially at ~0.2 Hz frequency. If needed, keep amplitude low and consider translucent content.

### watchOS

- Use SwiftUI for motion. For WatchKit animations, see `WKInterfaceImage`.
- All layout/appearance animations automatically include built-in easing at start and end — this cannot be turned off or customized.