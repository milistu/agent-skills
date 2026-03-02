# Status Bars

Guidelines for the system status bar that appears along the upper edge of the screen showing time, carrier, and battery level. Applies to iOS and iPadOS only (not supported in macOS, tvOS, visionOS, or watchOS).

## Best Practices

- **Obscure content under the status bar.** The status bar background is transparent by default, so content shows through. Ensure the status bar remains readable and don't imply that content behind it is interactive. Use a scroll edge effect to place a blurred view behind the status bar (see `ScrollEdgeEffectStyle` in SwiftUI, `UIScrollEdgeEffect` in UIKit).

- **Consider temporarily hiding the status bar for full-screen media.** This provides a more immersive experience (e.g., Photos app hides status bar when browsing full-screen photos).

- **Avoid permanently hiding the status bar.** Users need access to time, Wi-Fi status, etc. Let users redisplay a hidden status bar with a simple, discoverable gesture (e.g., single tap).

## Developer References

- `UIStatusBarStyle` — UIKit
- `preferredStatusBarStyle` — UIKit (UIViewController)