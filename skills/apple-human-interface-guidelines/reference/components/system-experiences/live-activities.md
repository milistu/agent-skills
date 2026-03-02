# Live Activities

Design guidelines for Live Activities — glanceable, real-time status displays that appear across iPhone, iPad, Mac, Apple Watch, and CarPlay.

## Anatomy

Live Activities appear in the Dynamic Island, Lock Screen, and other system locations. Every Live Activity must support four presentation styles:

- **Compact**: Two elements (leading + trailing) flanking the TrueDepth camera in the Dynamic Island. Used when only one Live Activity is active.
- **Minimal**: Used when multiple Live Activities are active. One attaches to the Dynamic Island, the other appears detached (circular or oval). Tap to open app; touch and hold for expanded.
- **Expanded**: Enlarged view shown when touching and holding compact or minimal presentations.
- **Lock Screen**: Banner at the bottom of the Lock Screen. On devices without Dynamic Island, briefly overlays as a banner on the Home Screen.
- **StandBy**: Minimal presentation on iPhone in StandBy; tapping shows Lock Screen presentation scaled 2x to fill the screen.

## Best Practices

- Offer Live Activities only for tasks/events with a defined beginning and end (max ~8 hours).
- Focus on the most important glanceable information — don't display everything.
- **Never** display ads or promotions.
- Avoid displaying sensitive information; show innocuous summaries and let users tap for details. Alternatively, redact sensitive views.
- Match your app's visual aesthetic in both dark and light appearances.
- Display logo marks without a container (not the full app icon).
- Don't add UI elements that draw attention to the Dynamic Island itself.
- Use large, heavier-weight text (medium weight or higher). Use small text sparingly.

## Layout Guidelines

- **Adapt to different screen sizes and presentations.** Create layouts for various devices and scale factors using the dimension specs below.
- **Use space efficiently.** Only use the space needed to clearly display content.
- **Use familiar layouts.** Templates with default system margins and recommended text sizes are available in Apple Design Resources.
- **Use consistent margins and concentric placement.** Match margins between rounded shapes and edges. Match inner corner radius to outer corner radius minus the margin. Use `ContainerRelativeShape` in SwiftUI.
- **Keep content compact and snug** within margins concentric to the outer edge.
- **To separate content blocks**, use an inset container shape or thick line — never draw content to the Dynamic Island edge.
- **Dynamically adjust height** on Lock Screen and expanded presentation based on available information.

**Tip:** To align non-rounded content in rounded corners, blur the content in your design tool to find positioning that aligns with the outer perimeter.

## Colors

- Compact, minimal, and expanded presentations always use a **black opaque background** (not customizable).
- Lock Screen presentation supports custom background color. Ensure sufficient contrast, especially for Always-On display.
- Use **bold colors** for text and objects to convey brand personality and make your Live Activity recognizable.
- **Tint the key line color** (visible in Dark Mode around the Dynamic Island) to match your content.

## Transitions & Animation

- Max animation duration: **2 seconds**.
- No animations on Always-On displays with reduced luminance.
- Use animations to reinforce information and draw attention to updates.
- Animate layout changes — preserve existing layout by animating elements to new positions.
- Avoid overlapping elements during transitions; use fade-in/out for non-moving items.

## Interactivity

- Tapping should open your app directly to related content (deep link).
- Focus on simple, direct actions. Prefer limiting to a **single interactive element** (button/toggle).
- Only include interactive elements for essential functionality (e.g., pause/resume music, workout controls).
- Consider response buttons for event updates (e.g., contact driver button in rideshare).

## Starting, Updating & Ending

- Start at appropriate times; make it easy to turn off in your app.
- Offer an **App Shortcut** to start your Live Activity (e.g., via Action button).
- Update only when new content is available.
- **Alert sparingly** — only for essential updates. Don't duplicate alerts with push notifications.
- Prefer a **single Live Activity** that rotates through multiple events rather than separate activities.
- **End immediately** when the task/event ends. Set a custom dismissal time (typically 15–30 minutes). After ending, the activity is removed from the Dynamic Island and CarPlay immediately but remains on Lock Screen, Mac menu bar, and watchOS Smart Stack for up to 4 hours.

## Presentation-Specific Guidance

### Compact Presentation
- Show dynamic, essential, up-to-date information (e.g., team logos + score).
- Design leading and trailing elements to read as a single unified piece.
- Keep content as narrow as possible, snug against TrueDepth camera. No extra padding.
- Maintain balanced layout with similarly sized views on both sides.
- Both leading and trailing elements must deep-link to the same screen.

### Minimal Presentation
- Display updated information rather than just a logo when possible.
- Ensure people can quickly recognize your app.

### Expanded Presentation
- Maintain relative placement of elements for coherent compact→expanded transitions.
- Wrap content tightly around TrueDepth camera — avoid empty space around it.

### Lock Screen Presentation
- Don't replicate notification layouts — create unique layouts.
- Choose colors that work with personalized Lock Screens. Use custom backgrounds/tints sparingly.
- Verify design in Dark Mode and Always-On display with reduced luminance.
- Verify the system-generated dismiss button color; adjust with `activitySystemActionForegroundColor(_:)` if needed.
- Standard layout margin: **14 points**.

### StandBy Presentation
- Update layout for StandBy; ensure assets look great at larger scale.
- Consider using default background color (blends with device bezel, allows slightly larger scaling).
- Use standard margins; don't extend graphics to screen edges.
- Verify design in **Night Mode** (red tint applied by system).

## CarPlay

- System combines compact leading + trailing elements into a single CarPlay Dashboard layout.
- Design applies to both CarPlay and Apple Watch.
- Interactive elements are **deactivated** in CarPlay.
- Consider custom layout with `ActivityFamily.small` for larger text or additional info.
- If users likely interact while driving, prefer timely content over buttons/toggles.

## watchOS

- Live Activities appear at top of Smart Stack. Default view combines compact leading + trailing elements.
- Tapping opens watchOS app (if available) or a full-screen view with button to open iPhone app.
- Consider custom watchOS layout for more information and interactive functionality.
- Custom watchOS layout also applies to CarPlay — avoid buttons/toggles if users may be driving.
- Focus on: progress (e.g., delivery ETA), interactive elements (timer controls), significant updates (score changes).

## macOS

- Active Live Activities appear in Menu bar using compact, minimal, and expanded presentations.
- Clicking launches iPhone Mirroring.

## Specifications

### iOS Dimensions (points)

| Screen (portrait) | Compact Leading | Compact Trailing | Minimal (width range) | Expanded (height range) | Lock Screen (height range) |
|---|---|---|---|---|---|
| 430×932 | 62.33×36.67 | 62.33×36.67 | 36.67–45×36.67 | 408×84–160 | 408×84–160 |
| 393×852 | 52.33×36.67 | 52.33×36.67 | 36.67–45×36.67 | 371×84–160 | 371×84–160 |

Dynamic Island corner radius: **44 pt**.

#### Dynamic Island Width by Device (pt)

| Presentation | Device | Width |
|---|---|---|
| Compact/Minimal | iPhone 17 Pro Max, Air, 16 Pro Max, 16 Plus, 15 Pro Max, 15 Plus, 14 Pro Max | 250 |
| Compact/Minimal | iPhone 17 Pro, 17, 16 Pro, 16, 15 Pro, 15, 14 Pro | 230 |
| Expanded | iPhone 17 Pro Max, Air, 16 Pro Max, 16 Plus, 15 Pro Max, 15 Plus, 14 Pro Max | 408 |
| Expanded | iPhone 17 Pro, 17, 16 Pro, 16, 15 Pro, 15, 14 Pro | 371 |

### iPadOS Dimensions (points)

| Screen (portrait) | Lock Screen (height range) |
|---|---|
| 1366×1024 | 500×84–160 |
| 1194×834 | 425×84–160 |
| 1012×834 | 425×84–160 |
| 1080×810 | 425×84–160 |
| 1024×768 | 425×84–160 |

### CarPlay Dimensions (pt)

| Live Activity size |
|---|
| 240×78 |
| 240×100 |
| 170×78 |

Test with CarPlay Simulator configurations:

| Configuration | Resolution (pt) |
|---|---|
| Widescreen | 1920×720 |
| Portrait | 900×1200 |
| Standard | 800×480 |

### watchOS Dimensions (pt)

| Watch Size | Smart Stack Size |
|---|---|
| 40mm | 152×69.5 |
| 41mm | 165×72.5 |
| 44mm | 173×76.5 |
| 45mm | 184×80.5 |
| 49mm | 191×81.5 |