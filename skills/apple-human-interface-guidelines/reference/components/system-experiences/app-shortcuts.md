# App Shortcuts

Design guidelines for App Shortcuts — system-wide access to your app's key functions via Siri, Spotlight, Shortcuts app, Action button, or Apple Pencil squeeze.

## Key Concepts

- App Shortcuts are available immediately after installation, before the user opens the app
- They use App Intents to define actions available to the system
- Each app can include **up to 10 App Shortcuts**
- People can also create custom shortcuts by combining your App Intents actions in the Shortcuts app

## Best Practices

- **Offer shortcuts for your app's most common and important tasks.** Straightforward tasks people can complete without leaving their current context work best. Open your app only for multistep tasks.
- **Add flexibility with optional parameters.** An App Shortcut can include a single optional value (parameter). Example: "Start [morning, daily, sleep] meditation." Use predictable, familiar values since people won't see a list for reference.
- **Ask for clarification when optional info is missing.** Suggest the most likely option as default based on usage patterns or context (e.g., time of day), and provide a short list of alternatives.
- **Keep voice interactions simple.** If the phrase feels complicated when spoken aloud, it's too difficult to remember. Avoid multiple parameters in one phrase — ask for additional info in subsequent steps.
- **Make App Shortcuts discoverable in your app.** Show occasional tips when people perform common actions to let them know a shortcut exists. Use `SiriTipUIView`.

## Responding to App Shortcuts

Your app can respond with spoken dialogue, custom visuals, or both:

| Response Type | Use When | Developer API |
|---|---|---|
| **Snippets** | Static info or dialog options (e.g., weather, order confirmation) | `ShowsSnippetView` |
| **Live Activities** | Continuous, changing info over time (timers, countdowns) | `LiveActivityIntent` |

- **Include all critical information in full dialogue text** for audio-only devices (AirPods, HomePod). Use `init(full:supporting:systemImageName:)`.

## Editorial Guidelines

- **Activation phrases:** Brief, memorable, with natural variants. Must include app name, but be creative. Example: Keynote accepts both "Create a Keynote" and "Add a new presentation in Keynote."
- **"App Shortcuts" and "Shortcuts" (the app):** Always title case, always plural. Example: *MyApp integrates with Shortcuts to provide a quick way to get things done.*
- **Individual shortcuts (not App Shortcuts or the app):** Use lowercase. Example: *Run a shortcut by asking Siri.*

## Platform Considerations

### iOS, iPadOS

- App Shortcuts appear in Spotlight's Top Hit area and Shortcuts area below
- Each includes an SF Symbol you choose, or a preview image of linked content
- **Order shortcuts based on importance** — the order determines initial appearance in Spotlight and Shortcuts app. System later prioritizes based on user frequency.
- **Offer an App Shortcut that starts a Live Activity** — useful for trackable events (e.g., cooking timer) that people can place on the Action button

### macOS

- App Shortcuts are **not supported** on macOS
- However, App Intents actions are supported — people can build custom shortcuts with them in the Shortcuts app on Mac

### visionOS, watchOS

No additional considerations.

### tvOS

Not supported.