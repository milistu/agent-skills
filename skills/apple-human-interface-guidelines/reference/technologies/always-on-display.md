# Always On Display

Guidelines for designing app interfaces that work well with the Always On display state on iPhone (14 Pro+) and Apple Watch.

In Always On, the system dims the display and minimizes onscreen motion to preserve power and privacy.

- **iPhone**: Displays Lock Screen items (Widgets, Live Activities) when the device is set aside face up.
- **Apple Watch**: Dims the watch face and continues displaying the frontmost app or apps with a background session when the wrist drops.

On both devices, notifications are displayed and a tap exits Always On.

## Best Practices

- **Hide sensitive information.** Redact personal data people wouldn't want casual observers to see (bank balances, health data). Also hide personal info in notifications.

- **Keep non-sensitive personal info glanceable when useful.** Examples: workout pace/heart rate on Apple Watch, flight arrival updates on iPhone. Users can disable Always On if they prefer no information visible.

- **Increase dimming on secondary content.** Dim secondary text, images, and color fills to give prominence to important information. For rich images or large color areas, consider removing images and using dimmed colors. Example: a to-do list app could remove row backgrounds and dim item details to highlight titles.

- **Maintain a consistent layout.** Don't make distracting interface changes when Always On begins/ends. Transition interactive components to an unavailable appearance rather than removing them. Make only infrequent, subtle updates within Always On. Example: a sports app might pause play-by-play updates and only update the score when it changes. Unnecessary motion is especially distracting on iPhone since the device is often face up on a surface.

- **Gracefully transition motion to a resting state.** Smoothly finish current motion rather than stopping instantly to communicate the transition and avoid confusion.

## Platform Support

- **Supported**: iOS (iPhone 14 Pro+), watchOS
- **Not supported**: iPadOS, macOS, tvOS, visionOS