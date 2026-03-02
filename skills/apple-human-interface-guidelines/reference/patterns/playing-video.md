# Playing Video

Guidelines for embedding video playback experiences across iOS, iPadOS, macOS, tvOS, visionOS, and watchOS.

## Playback Modes

The system selects a default playback mode based on aspect ratio:

- **Aspect-fill (full-screen):** Video scales to fill display; edge cropping may occur. Default for wide video (2:1 through 2.40:1). See `resizeAspectFill`.
- **Aspect (fit-to-screen):** Entire video visible; letterboxing/pillarboxing as needed. Default for standard video (4:3, 16:9, up to 2:1) and ultrawide (above 2.40:1). See `resizeAspect`.

In visionOS and tvOS, the built-in player provides **transport controls** (subtitles, audio language, favorites, library actions) and **content tabs** (Info, Episodes, Chapters). In visionOS, transport controls appear as an ornament.

## Best Practices

- **Use the system video player** for familiar, consistent interactions. If you must build a custom player, reference system player behavior closely — slight divergences frustrate users who don't know which habitual interactions still work.
- **Always display video at its original aspect ratio.** Do not use embedded letterbox/pillarbox padding. Padding causes videos to appear smaller in both full-screen and fit-to-screen modes and breaks edge-to-edge contexts like PiP on iPad.
- **Provide additional metadata** (image, title, description) when it adds value, but don't obscure playback. See `externalMetadata`.
- **Support expected input interactions** across all devices — e.g., Space on keyboard to play/pause on all platforms; Siri Remote gestures on Apple TV.
- **On tvOS, use transport controls for playback actions** (e.g., favoriting) and **custom content tabs** for supplementary info. Keep actions to 1–2 steps; keep content succinct.
- **Prevent audio mixing** when switching between modes (e.g., full-screen to PiP). Handle secondary audio correctly. See `silenceSecondaryAudioHintNotification`.

## Integrating with the TV App

- **Smooth transition:** TV app fades to black; immediately present your own black screen before playing content (no launch screen shown).
- **Show content immediately** — no splash screens, detail screens, or intro animations after transition.
- **Resume playback automatically** without prompting for confirmation.
- **Space key** plays/pauses on connected Bluetooth keyboards.
- **Handle user profiles:** If a playback request specifies a profile, switch to it automatically. If not, prompt the viewer to choose one.
- **Resume at previous end time** for long video clips.

### Loading Content

- Avoid loading screens if content loads quickly.
- If loading takes >2 seconds, show a black screen with a centered activity spinner.
- Start playback as soon as enough content loads; continue loading in background.
- Minimize branding/images on loading screens; maintain black background.

### Exiting Playback

- Show a **contextually relevant screen** (detail view with resume option, content menu, or main menu).
- **Prepare exit view immediately** after receiving playback notification for instant exits.

## Platform Considerations

### tvOS

- **Defer to content** with logos/overlays — keep them small and unobtrusive.
- Beware of **image retention** on some devices — keep overlays short; prefer translucent SDR graphics over bright opaque content.
- **Interactive overlays** (quizzes, surveys): implement minimum 0.5s delay before pausing and displaying. Provide a clear dismiss/resume path.

### visionOS

- **Help people stay comfortable:** Let them choose when to start video; use a small default window (resizable); ensure surroundings remain visible.
- **Don't let virtual content obscure playback or transport controls** in fully immersive experiences. The system auto-places the player at an optimal location.
- **Never auto-start fully immersive video** — people need control over immersion.
- **Thumbnail tracks for scrubbing:** Supply thumbnails 160 px wide. See HLS Authoring Specification > Trick Play.
- **Don't expand inline video to fill a window.** Inline video must be 2D with window content visible around it. Controls appear in-plane, not as an ornament.
- **Use RealityKit video player** for splash/transitional views where playback controls aren't needed. Supports correct aspect ratio for 2D/3D video and closed captions.

### watchOS

- **Keep clips ≤30 seconds** to conserve space and avoid wrist fatigue.
- **Don't scale video clips** — use recommended sizes.
- **Poster images** should represent clip contents; don't make them look like system controls.

#### Recommended Encoding Values (watchOS)

| Attribute | Value |
|---|---|
| Video codec | H.264 High Profile |
| Video bit rate | 160 kbps at up to 30 fps |
| Resolution (full screen) | 208×260 px (portrait) |
| Resolution (16:9) | 320×180 px (landscape) |
| Audio | 64 kbps HE-AAC |