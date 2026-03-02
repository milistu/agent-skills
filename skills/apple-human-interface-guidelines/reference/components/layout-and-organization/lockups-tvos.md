# Lockups (tvOS only)

Lockups combine multiple separate views into a single, interactive unit consisting of a content view, header, and footer. All three views expand and contract together as the lockup gets focus.

Four types: **cards**, **caption buttons**, **monograms**, and **posters**.

## Best Practices

- **Allow adequate space between lockups.** Focused lockups expand in size — leave enough room to avoid overlapping or displacing others.
- **Use consistent lockup sizes within a row or group.** Matching widths and heights is more visually appealing.

## Types

### Cards
Combines header, footer, and content view to present ratings and reviews for media items.
- API: `TVCardView`

### Caption Buttons
Includes a title and subtitle beneath the button. Can contain an image or text.
- **Tilt behavior on focus:**
  - Vertical alignment → tilt up/down
  - Horizontal alignment → tilt left/right
  - Grid layout → tilt both vertically and horizontally
- API: `TVCaptionButtonView`

### Monograms
Identify people (typically cast/crew) with a circular picture and name. Shows initials if no image is available.
- **Prefer images over initials** — images create a more intimate connection than text.
- API: `TVMonogramContentView`

### Posters
Image with optional title and subtitle, hidden until the poster comes into focus. Can be any size appropriate for content.
- API: `TVPosterView`

## Platform Support

tvOS only. Not supported on iOS, iPadOS, macOS, visionOS, or watchOS.

## Related APIs
- `TVLockupView` (TVUIKit)
- `TVLockupHeaderFooterView` (TVUIKit)