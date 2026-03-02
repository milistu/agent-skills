# Image Wells

An image well is an editable version of an image view. People can copy/paste images, delete them, or drag new images into a well without selecting it first.

**Platform support:** macOS only (not supported in iOS, iPadOS, tvOS, visionOS, or watchOS).

## Best Practices

- **Revert to a default image when necessary.** If your image well requires an image, display the default image again if people clear the content.
- **Support standard copy and paste menu items.** People expect to use standard menu items and keyboard shortcuts to interact with an image well. See Edit menu guidelines.

## Related

- [Image views](/design/human-interface-guidelines/image-views) — Non-editable counterpart
- Developer: `NSImageView` (AppKit)