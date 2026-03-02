# Playing Audio

Guidelines for handling audio playback across Apple platforms, including audio categories, interruptions, and platform-specific behaviors.

## Core Concepts

- **Silence**: In silent mode, only explicitly user-initiated audio plays (media playback, alarms, audio/video messaging). Nonessential sounds (keyboard clicks, sound effects, game soundtracks) should be silenced.
- **Volume**: Volume settings affect all sound system-wide. Exception: iPhone ringer volume is adjustable separately in Settings.
- **Headphones**: Sound reroutes automatically on connect; playback pauses immediately on disconnect.

## Best Practices

- **Adjust relative levels, not overall volume.** Your app can mix independent volume levels, but system volume always governs final output.
- **Permit audio rerouting** to different output devices (stereo, car radio, Apple TV) unless there's a compelling reason not to.
- **Use `MPVolumeView`** for the system-provided volume slider and audio output routing control.
- **Choose the right audio category** (`AVAudioSession.Category`) to match how your app uses sound.
- **Respond to external audio controls** (Control Center, headphone controls) only when your app is actively playing audio, in an audio-related context, or connected via Bluetooth/AirPlay.
- **Don't repurpose audio controls.** Never redefine the meaning of standard audio controls.
- **Create custom player controls only** if you need commands the system doesn't support (e.g., custom skip increments, related content display).
- **Flag your audio session** when finishing temporary audio so other apps can resume. Use `notifyOthersOnDeactivation`.

## Audio Categories

| Category | Meaning | Behavior |
| --- | --- | --- |
| Solo ambient | Sound isn't essential, silences other audio (e.g., game with soundtrack) | Responds to silence switch. No mixing. No background play. |
| Ambient | Sound isn't essential, doesn't silence other audio (e.g., game allowing other app's music) | Responds to silence switch. Mixes with other sounds. No background play. |
| Playback | Sound is essential, might mix (e.g., audiobook, language learning) | Ignores silence switch. May mix. Can play in background. |
| Record | Sound is recorded (e.g., note-taking with audio recording) | Ignores silence switch. No mixing. Can record in background. |
| Play and record | Sound recorded and played, potentially simultaneously (e.g., VoIP, video calling) | Ignores silence switch. May mix. Can record and play in background. |

## Handling Interruptions

- **Determine how to respond to audio-session interruptions.** Examples:
  - Recording apps can tell the system to avoid interrupting for incoming calls unless accepted.
  - VoIP apps must end calls when iPad Smart Folio closes (mutes microphone). Don't auto-restart the session on reopen — this risks unmuting without user knowledge.
- **Decide whether to auto-resume after interruptions.** Interruptions can be *resumable* (e.g., phone call) or *nonresumable* (e.g., starting a new playlist). Use `shouldResume` to check. Media playback apps should check before resuming; games can auto-resume since they play without explicit user choice.

## Platform-Specific Guidelines

### iOS, iPadOS
- Use Audio Services (`AudioToolbox`) for short sounds and vibrations.

### macOS
- Notification sounds mix with other audio by default.

### tvOS
- System plays audio only when people initiate it (in-app interactions or device calibrations). No sounds for alerts or notifications.

### visionOS
- **Prefer playing sound.** Apps without sound feel lifeless and may seem broken.
- **Design custom sounds for custom UI elements** to provide feedback and enhance spatial experience.
- **Use Spatial Audio** — sound perceived as coming from specific locations in space.
  - *Ambient audio*: pervasive sounds anchoring people in a virtual world.
  - *Audio source*: sound appearing to come from a specific object.
- **Define a range of sound origins.** Sound follows objects as they move; window audio comes from the window's position.
- **Vary repetitive sounds** — randomize pitch and volume during playback (e.g., virtual keyboard sounds).
- **Fixed vs. tracked sound:**
  - *Fixed*: always pointed at wearer regardless of head direction (e.g., Mindfulness ambient sound).
  - *Tracked*: perceived as coming from a specific object; changes with object distance/position. Preferred for realism.
- Audio from Now Playing app pauses when its window closes.
- Non-Now Playing app audio can duck when user looks away.
- Always provide non-audio alternatives for important information (accessibility).

### watchOS
- System manages audio playback. Apps play short clips in foreground or longer audio in background.
- Use **64 kbps HE-AAC** encoding for media assets.
- Consider presenting a **Now Playing view** (`WKNowPlayingView`) so people can control audio without leaving your app.