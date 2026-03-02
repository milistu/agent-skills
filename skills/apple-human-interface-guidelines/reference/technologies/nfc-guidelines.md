# NFC Design Guidelines

Guidelines for implementing NFC tag scanning experiences in iOS apps.

## In-App Tag Reading

Apps can support single- or multiple-object scanning when active, displaying a scanning sheet when people are about to scan.

**Don't encourage physical contact with objects.** The device only needs close proximity, not touch. Use terms like *scan* and *hold near* instead of *tap* and *touch*.

**Use approachable terminology.** Avoid technical terms like *NFC*, *Core NFC*, *Near-field communication*, and *tag*. Use friendly, conversational language.

| Use | Don't use |
| --- | --- |
| Scan the [*object name*]. | Scan the NFC tag. |
| Hold your iPhone near the [*object name*] to learn more about it. | To use NFC scanning, tap your phone to the [*object*]. |

**Provide succinct instructional text for the scanning sheet.** Use a complete sentence in sentence case with ending punctuation. Identify the object to scan and revise text for subsequent scans. Keep text short to avoid truncation.

| First scan | Subsequent scans |
| --- | --- |
| Hold your iPhone near the [*object name*] to learn more about it. | Now hold your iPhone near another [*object name*]. |

## Background Tag Reading

Background tag reading lets people scan tags without opening the app first. The system automatically looks for nearby compatible tags when the screen is illuminated, then shows a notification to send tag data to the app.

Background reading is **not available** when:
- An NFC scanning sheet is visible
- Wallet or Apple Pay are in use
- Cameras are in use
- Device is in Airplane Mode
- Device is locked after a restart

**Support both background and in-app tag reading.** Always provide an in-app scanning method for devices that don't support background tag reading.

## Platform Support

iOS and iPadOS only. Not supported in macOS, tvOS, visionOS, or watchOS.