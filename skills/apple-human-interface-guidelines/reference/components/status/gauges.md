# Gauges

Guidelines for displaying a specific numerical value within a range using circular or linear gauge components.

## Anatomy

- A gauge uses a **circular or linear path** to represent a range of values, mapping the current value to a specific point on the path.
- **Standard style**: Displays an indicator showing the current value's location.
- **Capacity style**: Displays a fill that stops at the value's location.
- **Accessory variant**: Visually similar to watchOS complications; works well in iOS Lock Screen widgets.

## Best Practices

- **Write succinct labels** describing the current value and both endpoints of the range. VoiceOver reads visible labels for accessibility.
- **Consider filling the path with a gradient** to communicate purpose (e.g., red-to-blue for hot-to-cold temperatures).

## Platform Support

- Supported on: iOS, iPadOS, macOS, visionOS, watchOS
- **Not supported** on tvOS

## macOS: Level Indicators

macOS also defines level indicators (capacity, rating, relevance styles).

### Capacity Style

| Type | Description |
|------|-------------|
| **Continuous** | Horizontal translucent track that fills with a solid bar to indicate the current value |
| **Discrete** | Horizontal row of separate, equally sized rectangular segments. Segments fill completely (never partially) with color |

- **Use continuous style for large ranges** — discrete segments become too small to be useful with large value ranges.
- **Change fill color to indicate significant range values.** Default fill is green. Options:
  - Change fill color at certain levels (very low, very high, past middle)
  - Use **tiered state** to show a sequence of several colors in one indicator (e.g., red → yellow → green)

### Relevance Style

Rarely used. Communicates relevancy using a shaded horizontal bar (e.g., in search results to visualize relevancy ranking).

## Related APIs

- `Gauge` (SwiftUI)
- `NSLevelIndicator` (AppKit)