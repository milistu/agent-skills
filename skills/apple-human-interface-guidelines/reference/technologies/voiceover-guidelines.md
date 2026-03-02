# VoiceOver Guidelines

Guidelines for supporting VoiceOver, Apple's screen reader, to make apps accessible to people who are blind or have low vision.

## Descriptions

- **Provide alternative labels for all key interface elements.** System controls have generic labels by default; provide more descriptive labels conveying your app's functionality. Add labels to custom elements. Keep descriptions up-to-date as UI changes.
- **Describe meaningful images.** Only describe the information the image itself conveys — VoiceOver already helps people understand surrounding interface elements like captions.
- **Make charts and infographics fully accessible.** Provide a concise description of what each infographic conveys. If interactive, make those interactions available to VoiceOver users via accessibility APIs.
- **Exclude purely decorative images from VoiceOver.** Hide images that don't convey useful or actionable information to reduce cognitive load. Use `accessibilityHidden(_:)`, `accessibilityElement`, or `isAccessibilityElement`.

## Navigation

- **Use titles and headings for information hierarchy.** The title is the first thing someone hears when arriving on a screen. Provide unique, succinct titles describing each page's content and purpose. Use accurate section headings.
- **Specify how elements are grouped, ordered, or linked.** Examine your app for visual-only relationships between elements and describe them to VoiceOver. VoiceOver reads elements in reading order (e.g., top-to-bottom, left-to-right for US English).
  - **Group related elements together** — e.g., an image and its caption should be in the same VoiceOver group so they're read together, not separately. Use `shouldGroupAccessibilityChildren`.
- **Inform VoiceOver when visible content or layout changes occur.** Report changes so VoiceOver can help people update their mental model. Use `AccessibilityNotification`.
- **Support the VoiceOver rotor.** Identify headings, links, and other content types so people can navigate via the rotor. Use `AccessibilityRotorEntry` (SwiftUI), `UIAccessibilityCustomRotor` (UIKit), or `NSAccessibilityCustomRotor` (AppKit).

## visionOS Considerations

- **Custom gestures aren't always accessible.** When VoiceOver is on in visionOS, apps with custom gestures don't receive hand input by default — this prevents accidental input while people explore the UI by voice. Users can enable Direct Gesture mode to bypass this. See [Improving accessibility support in your visionOS app](https://developer.apple.com/documentation/visionOS/improving-accessibility-support-in-your-app).