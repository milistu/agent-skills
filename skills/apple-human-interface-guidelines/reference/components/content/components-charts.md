# Charts Component Guidelines

Guidelines for designing effective charts in Apple platform apps using Swift Charts.

## Anatomy

A chart comprises:
- **Marks** — visual representations of data values (bar, line, point, etc.)
- **Plot area** — the area containing the marks
- **Axes** — define the frame of reference (typically one horizontal, one vertical)
- **Ticks** — reference points along axes for important values
- **Grid lines** — extend from ticks across the plot area to help estimate values
- **Labels** — name axes, grid lines, ticks, or marks
- **Accessibility labels** — describe chart elements for assistive technologies
- **Legend** — describes properties not related to position (e.g., color or shape for categories)

Each mark type uses visual attributes determined by a **scale**, which maps data values (numbers, dates, categories) to visual characteristics (position, color, height).

## Marks

**Choose mark type based on the information to communicate:**

| Mark Type | Best For | Example |
|-----------|----------|---------|
| **Bar** | Comparing values across categories, relative proportions, sums over time (e.g., total steps per day) | Category comparisons, part-of-whole |
| **Line** | Showing change over time; slope reveals magnitude of change and trends | Stock performance over years |
| **Point** | Depicting individual values; showing relationships between two properties; identifying outliers and clusters | Heart rate readings over months |

- **Consider combining mark types** when it adds clarity. E.g., add point marks on top of a line chart to highlight individual data points while showing overall trend.

## Axes

- **Fixed range**: Upper/lower bounds never change. Use when specific min/max values are inherently meaningful (e.g., battery charge: 0%–100%).
- **Dynamic range**: Bounds vary with current data. Use when possible values vary widely and you want marks to fill the plot area (e.g., Steps chart where Y axis adapts to the data).
- **Define the lower bound based on mark type and usage:**
  - Bar charts: zero works well for the lower bound so people can visually compare relative heights.
  - Other charts (e.g., heart rate): zero as lower bound can obscure meaningful differences that occur far from zero.
- **Use familiar value sequences** for tick/grid-line labels (e.g., 0, 5, 10 — not 1, 6, 11).
- **Tailor grid line density and visual weight** to context. Too many = overwhelming; too few = hard to estimate values. If people can inspect individual data points via interaction, use fewer grid lines with light label colors.

## Descriptive Content

- **Write descriptions that help people understand what a chart does before they view it.** Provide information-rich titles and labels describing purpose and functionality.
- **Summarize the main message.** Display key information so people can grasp it quickly (e.g., Weather shows a title/subtitle describing expected precipitation without requiring chart examination).

## Best Practices

- **Establish consistent visual hierarchy** — data most prominent, descriptions and axes provide context without competing.
- **In compact environments, maximize plot area width.** Keep vertical axis labels short; consider describing units in titles; place longer axis labels inside the plot area if they don't obscure data.
- **Make every chart accessible** — support VoiceOver and Audio Graphs.
- **Let people interact with data when sensible, but don't require interaction for critical information.** E.g., show the main trend by default; allow drag to reveal individual values.
- **Expand hit targets** to the entire plot area when marks are too small to target, allowing scrub-to-reveal.
- **Support keyboard navigation and Switch Control** — provide logical navigation paths (e.g., along X axis) using accessibility APIs like `accessibilityRespondsToUserInteraction(_:)`. For large datasets, let people move focus among subsets rather than all individual points.
- **Animate changes** in marks or axes so people notice them, and also notify assistive technologies via `UIAccessibility.Notification` or `NSAccessibility.Notification`.
- **Align charts with surrounding interface elements** — align leading edge of chart with other views. Display vertical grid line labels on trailing side. Consider shifting Y axis to trailing side so tick labels don't protrude past the leading edge.

## Color

- **Don't rely solely on color** to differentiate data or communicate essential information. Supplement with different shapes or patterns (e.g., Health uses red circles for systolic and black/white diamonds for diastolic blood pressure).
- **Add visual separation between contiguous color areas** — e.g., separators between stacked bar segments.

## Accessibility

Swift Charts provides default Audio Graphs implementation and default accessibility elements for each mark/group.

- **Use Audio Graphs** to give VoiceOver users chart title, descriptive summary, and audible tone representations of data.
- **If not using Audio Graphs**, provide an overview: chart type, what each axis represents, upper/lower bounds.
- **Decide granularity of accessibility labels**: describe each mark individually or groups of marks, depending on chart purpose and data density. Small chart-in-a-button may need only a single high-level label.
- **Write labels that support the chart's purpose** — Maps elevation chart summarizes elevation changes over route portions; Health Steps chart labels each bar with actual step count.

### Writing Accessibility Labels

- **Prioritize clarity and comprehensiveness** — include context (date, location) alongside values; don't repeat information available from Audio Graphs or overview.
- **Avoid subjective terms** (rapidly, gradually, almost) — use actual values.
- **Avoid ambiguous formats/abbreviations** — "June 6" not "6/6"; "60 minutes" not "60m".
- **Describe what details represent, not what they look like** — identify what each series represents, not the colors used.
- **Be consistent** when referring to axes (e.g., always mention X axis first).
- **Hide visible axis/tick text labels from assistive technologies** — VoiceOver users get this information through accessibility labels and Audio Graphs.

## watchOS

- Avoid requiring complex chart interactions. Prefer at-a-glance information with simple interactions.
- Use other platforms (e.g., iPhone) to display more details and support additional chart interactions.