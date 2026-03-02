# SharePlay Design Guidelines

Guidelines for designing SharePlay experiences that let multiple people share activities during FaceTime calls or Messages conversations.

## Best Practices

- **Indicate SharePlay support in your UI.** Use the `shareplay` SF Symbol to identify shareable content/experiences.
- **Handle subscriptions gracefully for nonsubscribers.** Offer temporary access, one-time passes, or support Family Sharing. If sign-up is needed during SharePlay, present a streamlined flow so others don't wait.
- **Support Picture in Picture (PiP)** on iPhone/iPad when possible. On Mac, shared video opens in a background window.
- **Use the term "SharePlay" correctly:**
  - As a noun: "Join SharePlay"
  - As a verb for direct actions: "SharePlay Movie"
  - Don't add adjectives (no "virtual" or "spatial" prefixes)
  - Don't modify the word (no "SharePlayed", "SharePlays", "SharePlaying")

## Sharing Activities

An *activity* is an app-defined shareable experience type. Define as many as needed.

- **Briefly describe each activity** — shown in invitations; keep short enough to avoid truncation.
- **Make it easy to start sharing** — if no session exists, present UI to start a group activity. The system then asks people to share or go solo.
- **Help people prepare before displaying the activity** — handle login, downloads, or payments first. Make these tasks simple.
- **Defer app tasks that might delay shared activity** — e.g., ask for profile info during playback pauses, not before.

## Platform Considerations

No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS.

### visionOS

People expect most visionOS apps to support SharePlay. FaceTime can show *spatial Personas* — representations of participants within each wearer's space.

#### Spatial Persona Templates

Choose the template that suits your shared activity:

| Template | Layout | Best For | Interaction Level |
|---|---|---|---|
| **Side-by-side** | Participants along a curved line, all facing content | Watching media together | Less nonverbal interaction |
| **Surround** | Participants arranged all around central content | 3D content viewed from different angles | Promotes verbal and nonverbal interaction |
| **Conversational** | Participants around center point; content along the circle (not center) | Background activities like music; social focus | High social interaction; not ideal for content interaction |

Developer APIs: `SystemCoordinator`, `SpatialTemplatePreference`

#### visionOS Best Practices

- **Launch directly into the shared activity** — avoid unrelated windows. Present sign-in in autodismissible windows.
- **Help people enter together, but don't force them** — when immersion level changes, check if transitioning would disrupt someone's task; offer choice if so.
- **Smoothly integrate new participants** — update shared immersive content to keep all synchronized. Accommodate up to 5 participants.

#### Maintaining a Shared Context

In a Full Space, the system uses a single coordinate system for content and participants, auto-synchronizing size, position, and orientation.

- **Ensure everyone views the same app state** — different states diminish the sense of togetherness.
- **Use Spatial Audio** to strengthen realism.
- **Let people find natural, social solutions to conflicts** — e.g., for shared virtual tools, let people communicate rather than adding tool-use controls. For simultaneous edits, consider "last change wins."
- **Keep private and shared content separate** — the system differentiates shared from unshared windows. Help people share the right window and distinguish between them. Let people drag content from private to shared windows.

#### Adjusting a Shared Context

- **Let people personalize without affecting others** — volume, subtitles, accessibility settings.
- **Consider unique views per participant** when content has an ideal viewing angle (e.g., Spatial Captures need specific perspective for depth perception). Continue synchronizing positions and app context.
- **Make it easy to exit and rejoin** — provide a quick-rejoin control. Consider continuing to display shared content so people stay informed while hiding their spatial Persona.