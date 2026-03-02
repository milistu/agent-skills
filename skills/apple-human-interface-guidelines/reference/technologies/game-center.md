# Game Center Design Guidelines

Guidelines for integrating Apple's Game Center social gaming network into games across Apple platforms, including access points, achievements, leaderboards, challenges, and multiplayer activities.

## Accessing Game Center

- Detect whether the player is signed in to Game Center at launch; if not, initialize at that time for the most seamless experience and maximum discovery (Top Played chart, social recommendations).

### Access Point

The access point is an Apple-designed UI element letting players view their Game Center profile without leaving the game.

- **Display in menu screens.** Add to main menu or settings. Avoid during active gameplay, splash screens, cinematics, or tutorials.
- **Avoid placing controls near it.** It has collapsed and expanded versions — ensure neither overlaps important UI. It can be placed at any of the four screen corners in a fixed position.
- In iOS/iPadOS/macOS: leads to the Game Overlay (system overlay).
- In visionOS/tvOS: leads to the in-game dashboard (full-screen view).
- In visionOS: location varies based on game type (immersive or volume-based).
- **Consider pausing your game** while the Game Overlay or dashboard is present.

### Custom UI

You can deep-link from custom UI into specific Game Overlay/dashboard areas (leaderboards, profile, etc.).

- **Use official Game Center artwork** from [Apple Design Resources](https://developer.apple.com/design/resources/#technologies). Don't adjust dimensions or visual effects.
- **Use correct terminology:**

| Term | Incorrect terms | Localization |
| --- | --- | --- |
| Game Center | GameKit, GameCenter, game center | Use system-provided translation |
| Game Center Profile | Profile, Account, Player Info | System translation for "Game Center"; localize "Profile" |
| Achievements | Awards, Trophies, Medals | |
| Leaderboards | Rankings, Scores, Leaders | |
| Challenges | Competitions | |
| Add Friends | Add, Add Profiles, Include Friends | |

## Achievements

Achievements appear in a collectible card format highlighting progress and artwork.

### Integration

- **Align with Game Center achievement states:** locked, in-progress, hidden, completed. Completed achievements appear in "Completed" group; all others in "Locked" group.
- **Determine display order before uploading** — upload order = display order. Consider ordering by most common game path.
- **Be succinct:** Title and description limited to 2 lines each (truncated beyond). Use title-style capitalization for title, sentence-style for description.
- **Give progress sense:** Progressive achievements show player progress with system-generated encouraging messages.

### Achievement Image Specs

The system applies a circular mask — keep content centered.

**iOS, iPadOS, macOS, visionOS:**

| Attribute | Value |
| --- | --- |
| Format | PNG, TIF, or JPG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 512×512 pt (1024×1024 px @2x) |
| Mask diameter | 512 pt (1024 px @2x) |

**tvOS:**

| Attribute | Value |
| --- | --- |
| Format | PNG, TIF, or JPG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 320×320 pt (640×640 px @2x) |
| Mask diameter | 200 pt (400 px @2x) |

- Design rich, high-quality, unique images per achievement. Don't reuse assets across achievements.

## Leaderboards

### Leaderboard Types

- **Classic leaderboard:** Tracks all-time best score, always active. Examples: best rhythm score, most coins in a run, longest time in endless runner.
- **Recurring leaderboard:** Resets on a defined interval (daily, weekly, etc.). Increases engagement with more chances to lead. Examples: daily puzzles, seasonal events, weekly mode leaderboards.

### Leaderboard Sets

Group multiple leaderboards by themes/experiences:
- Difficulty modes (Easy, Standard, Hard)
- Activity types (Combat, Crafting, Farming)
- Genres/themes (Disco, Pop, Rock)

### Leaderboard Image Specs

Create unique images per leaderboard reflecting the gameplay involved.

**iOS, iPadOS, macOS:**

| Attribute | Value |
| --- | --- |
| Format | JPEG, JPG, or PNG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 512×512 pt (1024×1024 px @2x) |
| Cropped area | 512×312 pt (1024×624 px @2x) |

**tvOS** (provide layered images for focus animation):

| Attribute | Value |
| --- | --- |
| Format | PNG, TIF, or JPG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 659×371 pt (1318×742 px @2x) |
| Focused size | 618×348 pt (1236×696 px @2x) |
| Unfocused size | 548×309 pt (1096×618 px @2x) |

> Be mindful of cropping: iOS/iPadOS/macOS crops artwork for leaderboards in sets. tvOS focus effect may crop edges. Keep primary content comfortably visible.

## Challenges

Challenges turn single-player activities into multiplayer friend competitions with time limits, built on top of leaderboards.

- **Create engaging challenges:** Short (1-5 minutes), skill-based, individually completable. Examples: fastest lap, most enemies in a round, fewest mistakes in a puzzle.
- **Avoid tracking overall progress or personal best scores** — this advantages regular players. Track most recent score after each attempt instead.
- **Deep-link to exact mode/level** where the challenge begins. Complete any required onboarding (e.g., tutorials) first, then auto-jump into the challenge.

### Challenge Image Specs

Avoid placing primary content where title/description overlay. Provide localized text versions via App Store Connect or Xcode.

| Attribute | Value |
| --- | --- |
| Format | JPEG, JPG, or PNG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 1920×1080 pt (3840×2160 px @2x) |
| Cropped area | 1465×767 pt (2930×1534 px @2x) |

## Multiplayer Activities

Supports real-time and turn-based multiplayer. Players access via party codes, Game Overlay, dashboard, or Games app.

### Party Codes

Game Center generates alpha-numeric codes (typically 8 characters, e.g., "2MP4-9CMF").

- Allow players to join late, leave early, and return later.
- Provide a way to view the current party code in-game.
- Allow manual party code entry.

### In-Game UI

Game Center's default multiplayer interface lets players invite nearby/recent players, friends, and contacts. You can also build custom multiplayer UI.

### Multiplayer Activity Image Specs

| Attribute | Value |
| --- | --- |
| Format | JPEG, JPG, or PNG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |
| Image size | 1920×1080 pt (3840×2160 px @2x) |
| Cropped area | 1465×767 pt (2930×1534 px @2x) |

## Platform Considerations

No additional considerations for iOS, iPadOS, macOS, or visionOS.

### tvOS

- Add an optional dashboard image at the top to highlight your game's aesthetic. Use a simple, recognizable image (logo/word mark). Don't use your app icon.

| Attribute | Value |
| --- | --- |
| Image size | 600×180 pt (1200×360 px @2x) |
| Format | PNG, TIF, or JPG |
| Color space | sRGB or P3 |
| Resolution | 72 DPI (minimum) |

### watchOS

- GameKit API is available but there's no system-supported Game Center UI on watchOS. Game Center content appears on a connected iPhone.