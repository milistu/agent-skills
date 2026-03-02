# Live-Viewing Apps

Design guidelines for live-viewing apps — prioritizing live content, creating immersive playback experiences, EPG design, and cloud DVR features.

## Best Practices

- **Feature live content prominently.** Minimize the interval between app launch and content playback. Place live content in the first tab so people can start viewing with one tap.
- **Let people tap once — or not at all — to start playback.** Display a Watch Now button on featured/recently viewed live content that immediately starts full-screen playback.
- **Make live content look live.** Distinguish live from VOD content using badges, symbols, sashes, or a "Live" collection row title.
- **Consider indicating progress of currently playing live content.** Use a progress bar to show how much content remains.
- **Give people additional actions and viewing alternatives.** Beyond playback (always primary), support record, restart, download, favorite. Display actions in consistent order throughout the app (e.g., Watch → Start Over → Record → Favorite). Show future airing times.
- **Match audio to current context.** Audio should match live content during playback/browsing, but stop when navigating away from the live tab.
- **Provide instant visual feedback when changing channels.** Confirms arrival at correct channel and covers streaming load time.

## Content Footer

A content footer lets people browse channels during playback without leaving the experience.

- Use subtle treatment (e.g., darkening) to keep text legible and items visually distinct from playing content
- Make the currently playing content's thumbnail identifiable (badge it or tint its progress bar)
- Match categories to those in your EPG
- Design predictable invoke/dismiss gestures (e.g., swipe up to invoke, swipe down to dismiss)

## EPG Experience

Electronic Program Guide (EPG) design guidelines:

- **Prominently display current info** — current program, channel, and time should be instantly visible so people can return to playback quickly
- **Make browsing effortless** — support paging, scrolling, or jumping; consider My Channels / Favorites groups
- **Group content into familiar categories** — e.g., Movies, TV Shows, Kids, Sports, Popular; match content footer categories
- **Let people browse EPG without leaving current content** — use PiP or background playback

## Cloud DVR

- Let people start/stop recording from the info panel during live-streaming
- Let people record future programs from content detail views; offer single episode or all episodes options
- Let people customize recordings (current episode only, new episodes only, specific teams, etc.)
- Allow playback, deletion, and recording settings adjustment within the cloud DVR area
- Consider offering storage management controls — delete watched content, auto-overwrite oldest/viewed content to prevent running out of space

## Platform Considerations

No additional platform-specific considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.