# Sliders

A slider is a horizontal track with a thumb control that people adjust between a minimum and maximum value. The portion of track between the minimum value and the thumb fills with color.

**Not supported in tvOS.**

## Best Practices

- **Customize appearance if it adds value.** Adjust track color, thumb image/tint, and left/right icons to communicate intent. E.g., a size slider could show small image icon on left and large on right.
- **Use familiar slider directions.** Minimum values on the leading side (or bottom for vertical), maximum on the trailing side (or top). E.g., 0% on leading, 100% on trailing.
- **Consider supplementing with a text field and stepper.** Especially for wide ranges, let people see and enter exact values. A stepper provides convenient whole-value increments.

## Platform-Specific Guidelines

### iOS / iPadOS

- **Don't use a slider for audio volume.** Use a volume view instead, which includes a volume-level slider and audio output device control.

### macOS

- **Slider styles:**
  - **Linear without tick marks** — narrow lozenge thumb, colored track fill
  - **Linear with tick marks** — same as above with discrete marks for pinpointing values
  - **Circular** — small circle thumb; tick marks appear as dots around circumference
- **Give live feedback** as the slider value changes (e.g., Dock icon scaling).
- **Choose appropriate style:**
  - Horizontal for fixed start/end ranges (e.g., opacity 0–100%)
  - Circular for repeating/continuing values (e.g., rotation 0–360°, or multi-rotation like 1440°)
- **Use a label** to introduce a slider — sentence-style capitalization, ending with a colon.
- **Use tick marks** to increase clarity and accuracy.
- **Add labels to tick marks** for clarity — numbers or words. Often labeling only min/max is sufficient. For nonlinear scales, add periodic labels. Consider adding a tooltip showing the thumb's value on pointer hover.

### visionOS

- **Prefer horizontal sliders.** Side-to-side gestures are easier than up and down.

### watchOS

- Sliders appear as **discrete steps** or a **continuous bar** representing a finite range.
- People tap buttons on the sides to increase/decrease by a predefined amount.
- **Create custom glyphs** if needed to communicate slider purpose (default is plus/minus signs).

## Related Components

- Steppers, Pickers, Text Fields

## Developer References

- `Slider` (SwiftUI)
- `UISlider` (UIKit)
- `NSSlider` (AppKit)