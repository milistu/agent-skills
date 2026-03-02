# Designing for watchOS

Guidelines for designing Apple Watch apps that deliver essential information through quick, glanceable interactions.

## Device Characteristics

- **Display**: Small, high-resolution wrist-mounted screen
- **Ergonomics**: Usually <1 foot from user's eyes; raised wrist to view, opposite hand to interact; Always On display visible when wrist is lowered
- **Inputs**: Digital Crown (vertical navigation, data inspection), standard gestures (tap, swipe, drag), Action button (essential action without looking), Siri shortcuts, device sensors (GPS, blood oxygen, heart, altimeter, accelerometer, gyroscope)
- **App interactions**: Glanceable; typically <1 minute per session; related experiences (complications, notifications, Siri) are used more than the app itself

## Key System Features

- **Complications** — data/graphics on the watch face
- **Notifications** — timely information delivery
- **Always On** — persistent display when wrist is lowered
- **Watch faces** — primary user touchpoint

## Best Practices

- **Quick, glanceable, single-screen interactions** — deliver critical info succinctly; enable targeted actions with 1-2 gestures
- **Minimize navigation depth** — use Digital Crown for vertical navigation (scrolling or switching between screens)
- **Personalize proactively** — anticipate needs using on-device data; provide actionable content relevant now or very soon
- **Leverage complications** — show relevant, potentially dynamic data/graphics on the watch face; tap to launch directly into your app
- **Use notifications effectively** — deliver timely, high-value info; let people act without opening the app
- **Use color and materials** — background color conveys supporting information; materials illustrate hierarchy and sense of place
- **Design for independence** — app should function standalone, complementing notifications and complications with additional details and functionality