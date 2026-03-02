# Steppers

A stepper is a two-segment control used to increase or decrease an incremental value. It sits next to a field that displays its current value, because the stepper itself doesn't display a value.

## Best Practices

- **Make the value that a stepper affects obvious.** A stepper doesn't display any values, so ensure people know which value they're changing.
- **Consider pairing a stepper with a text field when large value changes are likely.** Steppers work well for small changes requiring a few taps or clicks. For widely varying values, provide a text field for direct entry (e.g., number of copies on a printing screen).

## Platform Considerations

- **iOS, iPadOS, visionOS:** No additional considerations.
- **watchOS, tvOS:** Not supported.

### macOS

- **For large value ranges, consider supporting Shift-click** to change the value by more than the default increment (e.g., 10× the default).

## Related Components

- Pickers
- Text fields