# Loading Patterns

Guidelines for designing content-loading experiences across Apple platforms.

## Best Practices

- **Show something as soon as possible.** Display placeholder text, graphics, or animations while content loads, replacing them as content becomes available. Don't make people wait for loading to complete before displaying anything.
- **Let people do other things while content loads.** Load content in the background to give access to other actions (e.g., games can show the next level info or an in-game menu).
- **If loading takes unavoidably long, provide interesting placeholder content.** Show gameplay hints, tips, or feature introductions. Gauge remaining time accurately — avoid giving too little time to enjoy placeholder content or so much that you need to repeat it.
- **Download large assets in the background.** Use the Background Assets framework to schedule downloads (game level packs, 3D models, textures) immediately after installation, during updates, or at other nondisruptive times.

## Showing Progress

- **Clearly communicate loading status and estimated duration.** Ideally content displays instantly; for longer loads, use progress indicators.
  - **Determinate** progress indicator: when you know how long loading will take
  - **Indeterminate** progress indicator: when you don't know the duration
- **For games, consider custom loading views.** Standard progress indicators can feel out of place in games — design custom animations matching your game's style.

## Platform-Specific

- **iOS, iPadOS, macOS, tvOS, visionOS:** No additional considerations.
- **watchOS:** Avoid showing loading indicators. People expect quick interactions. If content needs 1–2 seconds to load, a loading indicator is better than a blank screen, but aim to display content immediately.

## Related Patterns & Components

- [Launching](/design/human-interface-guidelines/launching) — related pattern for app launch experience
- [Progress indicators](/design/human-interface-guidelines/progress-indicators) — component guidance for determinate/indeterminate indicators