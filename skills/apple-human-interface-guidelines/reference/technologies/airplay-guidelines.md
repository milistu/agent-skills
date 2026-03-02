# AirPlay Design Guidelines

Guidelines for integrating AirPlay wireless media streaming into apps across iOS, iPadOS, macOS, and tvOS.

## Best Practices

- **Prefer the system-provided media player** (`AVPlayerViewController`) — it supports chapter navigation, subtitles, closed captioning, and AirPlay streaming out of the box.
- **Provide content in the highest possible resolution.** HLS playlists must include the full range of available resolutions. AVFoundation auto-selects based on device. Content at 720p looks poor when AirPlay-streamed to a 4K TV.
- **Stream only expected content.** Don't stream background loops or short in-app-only video experiences. Use `usesExternalPlaybackWhileExternalScreenIsActive` to control this.
- **Support both AirPlay streaming and mirroring** for maximum flexibility.
- **Support remote control events** (play, pause, fast forward) for lock screen and Siri/HomePod interaction. See `MPRemoteCommandCenter`.
- **Don't stop playback** when app enters background or device locks.
- **Don't interrupt another app's playback** unless starting immersive content. For non-immersive content (launch videos, auto-play inline), use `AVAudioSession.Category.ambient` and play locally only.
- **Keep app functional during AirPlay playback.** If users navigate away from playback screen, don't auto-play other in-app videos that would interrupt the stream.

### Custom Media Player (if system player isn't viable)
- Custom buttons must match appearance and behavior of system-provided ones
- Provide distinct visual states: playback started, occurring, unavailable
- Use only Apple-provided symbols for AirPlay controls
- Position AirPlay icon in the **lower-right corner** (iOS 16+, iPadOS 16+)

## AirPlay Icon Usage

Two icon variants: **audio** (triangle below three concentric lines) and **video** (triangle below a rounded rectangle).

| Background | Icon Color |
|---|---|
| White/light | Black icon |
| Black/dark | White icon |
| Custom | Match color of other technology icons |

### Icon Rules
- Position consistently with other technology icons; if others are in shapes, AirPlay icon can be too
- **Don't** use the AirPlay icon or name in custom buttons or interactive elements — use only in noninteractive contexts
- Can pair icon with the name "AirPlay" below or beside it if other technologies are referenced similarly; use the same font as the rest of the layout
- Don't use the icon within text or as a replacement for the name
- Make AirPlay references less prominent than your app name/identity

## Referring to AirPlay — Terminology Rules

**Capitalization:** "AirPlay" — one word, uppercase A and P. In all-caps layouts, "AIRPLAY" is acceptable.

**Always use "AirPlay" as a noun:**

| ✅ Correct | ❌ Incorrect |
|---|---|
| Use AirPlay to listen on your speaker | AirPlay to your speaker |
| | You can AirPlay with [App Name] |

**Use terms like "works with", "use", "supports", "compatible":**

| ✅ Correct | ❌ Incorrect |
|---|---|
| [App Name] is compatible with AirPlay | [App Name] has AirPlay |
| AirPlay-enabled speaker | |
| You can use AirPlay with [App Name] | |

**Apple prefix is optional:** "Compatible with Apple AirPlay" is acceptable.

## Platform Support

Supported on iOS, iPadOS, macOS, tvOS, and visionOS. **Not supported on watchOS.**