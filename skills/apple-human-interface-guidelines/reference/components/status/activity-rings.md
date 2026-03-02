# Activity Rings

Guidelines for displaying Activity rings (Move, Exercise, Stand progress) in iOS, iPadOS, and watchOS apps.

## Overview

- **watchOS**: Always three rings (Move, Exercise, Stand)
- **iOS**: Three rings if Apple Watch is paired; Move ring only if no watch paired
- API: [`HKActivityRingView`](https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView)

## Best Practices

- **Display only when relevant** — health/fitness apps, especially those contributing to HealthKit. Good use cases: workout metrics screens, post-workout summary screens.
- **Only for Move, Exercise, Stand data** — never replicate, modify, or repurpose rings for other data types. Never show Move/Exercise/Stand progress in a custom ring-like element.
- **Single person only** — never represent data for multiple people. Make it obvious whose progress is shown (label, photo, or avatar).
- **No notifications duplicating system Activity alerts** — the system already sends Move, Exercise, and Stand updates. Don't show Activity rings in notifications.
- **Not for decoration or branding** — never use in app icons, marketing materials, labels, or background graphics.

## Visual Requirements

- **Never change ring colors** — no filters, no opacity modifications
- **Always use a black background**
- **Prefer circular enclosure** — adjust corner radius of the enclosing view rather than applying a circular mask
- **Keep black background visible around outermost ring** — add a thin black stroke around the outer edge if needed; no gradients, shadows, or other effects
- **Scale appropriately** — rings shouldn't seem disconnected or out of place
- **Adapt the surrounding UI to match rings** — never modify rings to match the surrounding interface
- **Minimum outer margin** — at least equal to the distance between rings. Never let other elements crop, obstruct, or encroach on this margin or the rings.
- **Differentiate other ring-like elements** — use padding, lines, labels, color, or scale to visually separate from Activity rings

## Ring-Associated Label Colors (RGB)

Use these colors for labels (*Move*, *Exercise*, *Stand*) or current/goal values displayed alongside rings:

| Ring | R | G | B |
|------|-----|-----|-----|
| Move | 250 | 17 | 79 |
| Exercise | 166 | 255 | 0 |
| Stand | 0 | 255 | 246 |

## iOS-Specific Behavior

Appearance changes automatically based on Apple Watch pairing:
- **Paired**: All three rings displayed
- **Not paired**: Move ring only (approximation from steps and workout info from other apps)

Activity history can include a mix of both styles if a user sometimes exercises with and without their watch.

## Platform Support

- **Supported**: iOS, iPadOS, watchOS
- **Not supported**: macOS, tvOS, visionOS