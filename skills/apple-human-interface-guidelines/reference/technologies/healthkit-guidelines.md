# HealthKit Design Guidelines

Guidelines for apps that integrate with HealthKit and the Health app on iOS, iPadOS, and watchOS.

> **Important:** If your app doesn't provide health and fitness functionality, don't request access to people's private health data.

## Privacy Protection

- **Provide a coherent privacy policy.** You must provide a URL to a clearly stated privacy policy during app submission.
- **Request access to health data only when you need it.** Request access contextually (e.g., request weight access when people log their weight, not at launch). People can change permissions, so request every time you need access.
- **Clarify intent with descriptive messages on the standard permission screen.** Write succinct sentences explaining why you need the data and how people benefit. Don't add custom screens that replicate the system permission screen's behavior or content.
- **Manage health data sharing solely through the system's privacy settings.** Don't build additional screens in your app that affect health data flow. People expect to manage access in Settings > Privacy.

## Activity Rings

- **Use Activity rings for Move, Exercise, and Stand information only.** Don't replicate or modify them for other purposes or data types. Never show Move/Exercise/Stand progress in another ring-like element.
- **Use Activity rings to show progress for a single person only.** Never represent data for multiple people. Make it obvious whose progress is shown (label, photo, or avatar).
- **Don't use Activity rings for ornamentation.** Never display them in labels or background graphics.
- **Don't use Activity rings for branding.** Never use them in your app icon or marketing materials.
- **Maintain Activity ring and background colors.** Never change the look with filters, color changes, or opacity modifications. Design the surrounding interface to blend with the rings (e.g., enclose within a circle). Scale appropriately.
- **Maintain Activity ring margins.** Minimum outer margin must be no less than the distance between rings. Never allow other elements to crop, obstruct, or encroach on this margin. To display within a circle, adjust the corner radius of the enclosing view rather than applying a circular mask.
- **Differentiate other ring-like elements from Activity rings.** Use padding, lines, labels, color, or scale to separate them visually.
- **Provide app-specific information only in Activity notifications.** Don't repeat system-provided Move/Exercise/Stand progress updates. Never show an Activity ring element in notifications. You may reference Activity progress in a way unique to your app.

## Apple Health Icon

- **Use only the Apple-provided icon.** Download from [Apple Design Resources](https://developer.apple.com/design/resources/#technologies). Don't create your own.
- **Display the name *Apple Health* close to the icon.**
- **Display the icon consistently with other health-related app icons** — make it no smaller than other icons in the same view.
- **Don't use the icon as a button.** Use it only to indicate compatibility.
- **Don't alter the icon's appearance.** No masking, circular shapes, borders, color overlays, gradients, shadows, or other visual effects.
- **Maintain minimum clear space of 1/10 of icon height.** Don't composite onto another graphic element.
- **Don't use the icon within text** or as a replacement for the terms *Health*, *Apple Health*, or *HealthKit*.
- **Don't display Health app images or screenshots** — they are copyrighted.

## Editorial Guidelines

- Refer to the Health app as **Apple Health** or **the Apple Health app**.
- **Don't use the term *HealthKit*** in user-facing text — it's a developer-facing term. Say your app "works with the Apple Health app" or "uses data from the Apple Health app."
- **Capitalize correctly:** *Apple Health* — two words, uppercase A and uppercase H, then lowercase. Fully uppercase only when matching an established typographic style that capitalizes all text.
- **Use the system-provided translation of *Health*** to match what people see on their device.

## Platform Support

Supported on iOS, iPadOS, and watchOS. Not supported on macOS, tvOS, or visionOS.