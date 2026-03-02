# Modality

Guidelines for presenting content in a separate, dedicated mode that prevents interaction with the parent view and requires an explicit action to dismiss.

## When to Use Modality

- Ensure people receive critical information and act on it
- Provide options to confirm or modify a recent action
- Help people perform a distinct, narrowly scoped task without losing previous context
- Give people an immersive experience or help concentrate on a complex task

## Modal Components by Platform

| Component | Platforms |
|---|---|
| Alert | All platforms |
| Sheet | iOS, iPadOS, macOS |
| Popover | iOS, iPadOS, macOS |
| Action sheet | iOS, iPadOS |
| Activity view | iOS, iPadOS |
| Confirmation dialog | macOS |
| Separate window | iPadOS, macOS, visionOS |
| Full-screen modal | All (fills window in visionOS Shared Space; can become immersive in Full Space) |

## Best Practices

- **Use modality only when there's a clear benefit.** It takes people out of their current context and requires an action to dismiss.
- **Keep modal tasks simple, short, and streamlined.** Complex modals cause people to lose track of the suspended task, especially when the modal obscures their previous context.
- **Avoid creating an app-within-an-app feel.** If a modal must contain subviews, provide a single path through the hierarchy. Avoid buttons that could be mistaken for the dismiss button.
- **Use full-screen modal style for in-depth content or complex tasks.** Works well for videos, photos, camera views, or multistep tasks like markup or photo editing.
- **Always provide an obvious dismiss mechanism.** Follow platform conventions:
  - **iOS/iPadOS/watchOS:** Button in top toolbar or swipe-down gesture
  - **macOS/tvOS:** Button in the main content view
- **Confirm before closing if data loss is possible.** Explain the situation and offer resolution options (e.g., an action sheet with a save option on iOS).
- **Provide a title or description for the modal task.** Helps people keep their place when switching contexts.
- **Don't stack multiple modal views.** Let people dismiss one modal before presenting another. Multiple visible modals create visual clutter and cognitive overload. Exception: alerts can appear on top of other modal views, but never display more than one alert simultaneously.