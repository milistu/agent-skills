# Designing for Games on Apple Platforms

Guidelines for integrating platform characteristics and patterns into games across Apple devices.

## Jump into Gameplay

- **Let people play as soon as installation completes.** Include as much playable content in the initial install while keeping download ≤30 minutes. Download additional content in the background.
- **Provide great default settings.** Use device info to choose best defaults (resolution, paired accessories, game controllers, accessibility settings). Support each platform's most common interaction methods.
- **Teach through play.** Integrate configuration and onboarding into a playable tutorial. Offer written tutorials as optional reference, not a prerequisite.
- **Defer requests until the right time.** Don't bombard players before gameplay. Integrate permission requests into scenarios that require the data (e.g., ask hand-tracking permission between cutscene and first hand-controlled action). Let people spend quality time before requesting ratings.

## Look Stunning on Every Display

### Text Size Requirements

| Platform | Default text size | Minimum text size |
| --- | --- | --- |
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

### Button Size Requirements

| Platform | Default button size | Minimum button size |
| --- | --- | --- |
| iOS, iPadOS | 44x44 pt | 28x28 pt |
| macOS | 28x28 pt | 20x20 pt |
| tvOS | 66x66 pt | 56x56 pt |
| visionOS | 60x60 pt | 28x28 pt |
| watchOS | 44x44 pt | 28x28 pt |

### Graphics & Layout

- **Prefer resolution-independent textures and graphics.** If not possible, match game resolution to device resolution. In visionOS, prefer vector-based art for dynamic scaling at different distances.
- **Integrate device features into layout.** Accommodate rounded corners, camera housing, etc. Use platform-provided safe areas.
- **Adapt in-game menus to different aspect ratios** (16:10, 19.5:9, 4:3). Use dynamic layouts with relative constraints. Avoid fixed layouts; create device-specific layouts only when necessary.
- **Design for full-screen.** In macOS/iOS/iPadOS, full-screen hides other apps and system UI. In visionOS, Full Space can completely surround players.

## Enable Intuitive Interactions

### Default & Additional Interaction Methods by Platform

| Platform | Default interaction methods | Additional interaction methods |
| --- | --- | --- |
| iOS | Touch | Game controller |
| iPadOS | Touch | Game controller, keyboard, mouse, trackpad, Apple Pencil |
| macOS | Keyboard, mouse, trackpad | Game controller |
| tvOS | Remote | Game controller, keyboard, mouse, trackpad |
| visionOS | Touch | Game controller, keyboard, mouse, trackpad, spatial game controller |
| watchOS | Touch | – |

- **Support physical game controllers** (every platform except watchOS), but always offer alternative interaction methods for players who can't use controllers.
- **Offer touch-based controls** on iPhone/iPad — allow direct interaction with game elements and virtual on-screen controls.
- When porting from pointer-based to touch-based context, pay special attention to control sizing and menu behavior.

## Welcome Everyone (Accessibility & Inclusion)

- **Prioritize perceivability.** Don't rely solely on color for important details. Include descriptive subtitles for cutscenes.
- **Help players personalize:** type size, control mapping, motion intensity, sound balance. Use built-in Apple accessibility technologies (system frameworks or Unity plug-ins).
- **Support self-representation.** If players create avatars or supply names, support the spectrum of self-identity.
- **Avoid stereotypes.** Review characters and scenarios for biases related to race, gender, or cultural heritage.

## Adopt Apple Technologies

- **Game Center:** Social gaming network for progress tracking, achievements, leaderboards, challenges, and multiplayer.
- **GameSave / iCloud:** Let players save game state and resume on a different device.
- **Core Haptics:** Custom haptic patterns (optionally with audio) on iOS, iPadOS, tvOS, visionOS, and many game controllers.
- **Spatial Audio:** Multichannel audio that adapts to current device for immersive sound.
- **Additional technologies:** AR, ML, HealthKit, camera, microphone, location data for unique gameplay mechanics.