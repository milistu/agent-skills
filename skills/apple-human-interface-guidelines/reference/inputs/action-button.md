# Action Button

Design guidelines for integrating with the Action button on supported iPhone and Apple Watch models. The Action button lets people quickly run App Shortcuts or access system functionality.

A person chooses a function for the Action button during device setup and can adjust it in Settings. When associated with an App Shortcut, pressing the button runs it similarly to using Siri or tapping it in Spotlight.

**Supported platforms:** iOS, watchOS only (not iPadOS, macOS, tvOS, or visionOS).

## Best Practices

- **Support the Action button with essential app functions.** Example: a cooking app's "Start Egg Timer" action. Don't offer an action that simply opens your app — the system already provides this.
- **Write short action labels** that people see in Settings:
  - Use title-style capitalization
  - Begin with a verb, present tense
  - Exclude articles and prepositions
  - Maximum 3 words
  - Example: "Start Race" (not "Started Race" or "Start the Race")
- **Let the system show people how to use the Action button.** Avoid creating content that repeats Settings guidance or system-provided usage tips.

## iOS

- **Let people use actions without leaving their current context.** Use lightweight multitasking like Live Activities and custom snippets instead of launching your app. Example: "Set Timer" prompts for duration and launches a Live Activity countdown instead of opening Clock.

## watchOS

First press can: drop a waypoint, start a dive, or begin a specific workout. Subsequent presses support secondary actions like marking a segment or transitioning workout modalities.

- **Offer a secondary function that supports/advances the primary action.** People often press without looking at the screen, so subsequent presses must flow logically from the first press and make sense in context. Keep secondary functions simple and intuitive. Avoid more than one secondary function to reduce cognitive load.
- **Use subsequent presses for additional functionality, not stopping/concluding.** Offer stop options within your interface instead.
- **Pressing Action button + side button together should pause the current function.** Exception: diving apps where pausing could be dangerous (losing track of depth/time underwater). Unless pausing causes a negative experience, always support this expectation.