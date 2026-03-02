# iMessage Apps and Stickers

Design guidelines for iMessage apps and sticker packs available within Messages conversations and effects in Messages and FaceTime.

## Best Practices

- **Provide one primary experience.** People are in a conversational flow — functionality/content must be easy to understand and immediately available. Consider separate iMessage apps for distinct types of functionality.
- **Surface content from your iOS/iPadOS app.** Offer app-specific info people might want to share (shopping lists, trip itineraries) or support simple collaborative tasks.
- **Present essential features in the compact view.** Most frequently used items should be available in compact view; reserve additional content for expanded view.
- **Let people edit text only in the expanded view.** Compact view occupies roughly the same space as the keyboard — display the keyboard in expanded view to keep content visible.
- **Create stickers that are expressive, inclusive, and versatile.** Each sticker should remain legible against a wide range of backgrounds when rotated or scaled. Use transparency to help integrate stickers with text, photos, and other stickers.
- **Provide localized alternative descriptions for each sticker** for VoiceOver accessibility.

## Icon Sizes

Supply a square-cornered icon; the system applies a rounded-corner mask automatically.

| Usage | @2x (pixels) | @3x (pixels) |
| --- | --- | --- |
| Messages, notifications | 148×110 | — |
| | 143×100 | — |
| | 120×90 | 180×135 |
| | 64×48 | 96×72 |
| | 54×40 | 81×60 |
| Settings | 58×58 | 87×87 |
| App Store | 1024×1024 | 1024×1024 |

## Sticker Sizes

Messages supports small, regular, and large stickers. Pick one size for all stickers in a pack — don't mix sizes. Messages displays stickers in a grid organized by size.

Provide sticker images at @3x. The system generates @2x and @1x by downscaling at runtime.

| Sticker size | @3x dimensions (pixels) |
| --- | --- |
| Small | 300×300 |
| Regular | 408×408 |
| Large | 618×618 |

### File Requirements

- Maximum file size: **500 KB** per sticker

| Format | Transparency | Animation |
| --- | --- | --- |
| PNG | 8-bit | No |
| APNG | 8-bit | Yes |
| GIF | Single-color | Yes |
| JPEG | No | No |

## Platform Support

iOS and iPadOS only. Not supported on macOS, tvOS, visionOS, or watchOS.