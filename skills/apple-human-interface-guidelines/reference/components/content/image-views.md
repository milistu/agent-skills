# Image Views

Guidelines for displaying images using image view components across Apple platforms.

## Best Practices

- **Use an image view only when the primary purpose is to display an image.** For interactive images, use a system-provided button configured to display the image instead of adding button behaviors to an image view.
- **Prefer SF Symbols or interface icons over image views for icons.** SF Symbols are vector-based, support dynamic coloring/opacity, and respect user accent colors.

## Content

- Image views support various formats: PNG, JPEG, PDF, and more.
- **Take care when overlaying text on images.** Ensure text contrasts well with the image; consider adding a text shadow or background layer to improve legibility.
- **Use consistent sizes for all images in an animated sequence.** Pre-scale images to fit the view to avoid runtime scaling. If scaling is needed, keep all images the same size and shape for better performance.

## Platform-Specific Guidance

### macOS
- **Use an image well for editable image views.** Image wells support copy, paste, drag, and delete operations.
- **Use an image button (not image view) for clickable images.** Image buttons contain an image/icon and initiate app-specific actions.

### tvOS
- Many tvOS images combine multiple layers with transparency to create depth (layered images).

### visionOS
- Windows can display 2D images, stereoscopic images, and spatial photos via image views.
- With RealityKit, images can be displayed outside image views alongside 3D content, or used to generate spatial scenes from 2D images.
- See `ImagePresentationComponent` for implementation.

### watchOS
- **Use SwiftUI for animations when possible.** Alternatively, use WatchKit's `WKImageAnimatable` to animate image sequences.

## Developer References

| Framework | Class |
|-----------|-------|
| SwiftUI | `Image` |
| UIKit | `UIImageView` |
| AppKit | `NSImageView` |