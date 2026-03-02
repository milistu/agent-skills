# Camera Control

Design guidelines for the Camera Control on iPhone 16 and iPhone 16 Pro models. The Camera Control is a physical button that opens camera experiences. Light press shows an overlay extending from the device bezel; light double-press reveals available controls; sliding adjusts values.

**Platform support:** iOS only (not iPadOS, macOS, watchOS, tvOS, or visionOS).

## Anatomy

Two types of controls in the overlay:

- **Slider** — provides a range of values (e.g., contrast amount)
- **Picker** — offers discrete options (e.g., grid on/off)

System-provided standard controls (optional to include):
- **Zoom factor** control
- **Exposure bias** control

## Best Practices

**Use SF Symbols for control icons.** Custom symbols are not supported. Choose from the Camera & Photos section in SF Symbols. Symbols represent functionality, not current state.

**Keep control names short.** Labels follow Dynamic Type sizing; long names may obscure the viewfinder.

**Include units or symbols with slider values.** Add context like EV, %, or custom strings so people understand what the slider controls. See `localizedValueFormat` in AVFoundation.

**Define prominent values for sliders.** Set frequently chosen or evenly spaced values (e.g., major zoom increments). The system "snaps" to prominent values during sliding. See `prominentValues` in AVFoundation.

**Make space for the overlay.** The overlay and labels occupy screen area adjacent to the Camera Control in both portrait and landscape. Place UI outside overlay areas. Maximize viewfinder height/width and let the overlay appear/disappear over it.

**Minimize viewfinder distractions.** Avoid duplicating controls in both your UI and the overlay. When the overlay is visible, hide redundant on-screen controls.

**Enable/disable controls per camera mode.** For example, disable video controls when taking photos. Controls cannot be added or removed at runtime — only enabled/disabled.

**Arrange controls thoughtfully.** Place commonly used controls toward the middle for quick access; lesser-used controls on either side. The system remembers the last control used in your app when reopening the overlay.

**Support launching from anywhere.** Create a locked camera capture extension so people can configure the Camera Control to launch your camera experience from the Lock Screen, Home Screen, or other apps. See `LockedCameraCapture` framework.

## Key API References

- `AVCaptureControl` — base class for camera controls
- `AVCaptureSlider` — slider control (`localizedValueFormat`, `prominentValues`)
- `LockedCameraCapture` — framework for locked device camera experiences