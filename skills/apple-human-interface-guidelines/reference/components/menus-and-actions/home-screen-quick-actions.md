# Home Screen Quick Actions

Guidelines for the touch-and-hold (or 3D Touch) menu that appears on app icons on the Home Screen (iOS/iPadOS only).

## Overview

- Each quick action includes a **title**, an **interface icon** (left or right depending on icon position), and an optional **subtitle**
- Title and subtitle are always left-aligned in LTR languages
- Quick actions can be updated dynamically when new information is available
- Maximum of **4** app-specific quick actions
- The menu also includes system items (remove app, edit Home Screen)

## Best Practices

- **Create quick actions for compelling, high-value tasks** — actions people would want to perform without opening the app first
- **Avoid unpredictable changes to quick actions** — dynamic updates are fine (e.g., based on location, recent activity, time of day) but changes should be predictable to users
- **Use succinct titles that communicate results instantly** — e.g., "Directions Home," "Create New Contact," "New Message"
  - Don't include app name or extraneous info in title/subtitle
  - Keep text short to avoid truncation
  - Account for localization
- **Provide a subtitle** only if more context is needed (e.g., Mail shows unread message counts)
- **Use SF Symbols** for quick action icons; see standard icons for common actions
- **Don't use emoji in place of symbols** — emojis are full color, while quick action symbols are monochromatic and adapt for Dark Mode contrast
- If designing a custom icon, use the Quick Action Icon Template from [Apple Design Resources for iOS and iPadOS](https://developer.apple.com/design/resources/#ios-apps)

## Platform Support

- **Supported:** iOS, iPadOS
- **Not supported:** macOS, tvOS, visionOS, watchOS