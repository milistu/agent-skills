# Workouts Pattern

Guidelines for designing workout and fitness experiences on Apple Watch, iPhone, and iPad.

## Best Practices

### watchOS Workout Session Layout

Use workout sessions to provide useful data and relevant controls. During active sessions, watchOS continues displaying the app between wrist raises. Standard three-screen arrangement:

1. **Leftmost screen**: Large buttons controlling the in-progress session (End, Resume, New, Segment)
2. **Middle screen**: Metrics and data people can read at a glance (elapsed/remaining time, calories, heart rate, pace, elevation)
3. **Rightmost screen**: Media playback controls (if supported)

### Active Session Indicators

- Use a **distinct visual appearance** to indicate an active workout — real-time updating metric values help convey active state
- Use a unique layout to further distinguish the metrics screen

### Controls

- Provide workout controls that are **easy to find and tap**
- Make it easy to pause, resume, and stop
- Provide clear feedback when a session starts or stops

### During-Workout Focus

- **Avoid distracting** people with non-relevant information during workouts
- Don't show workout selection lists or other app sections during an active session

### Sensor Data Unavailability

If sensor data is unavailable (e.g., water preventing heart-rate measurement in swimming), explain what data is still being recorded. Example language patterns:

| Example text |
|---|
| "GPS is not used during a Pool Swim, and water may prevent a heart-rate measurement, but Apple Watch will still track your calories, laps, and distance using the built-in accelerometer." |
| "In this type of workout, you earn the calorie equivalent of a brisk walk anytime sensor readings are unavailable." |
| "GPS will only provide distance when you do a freestyle stroke. Water might prevent a heart-rate measurement, but calories will still be tracked using the built-in accelerometer." |

### Session End

- **Provide a summary** at the end of a session confirming the workout is finished and displaying recorded information
- Consider including **Activity rings** in the summary so people can check current progress
- **Discard extremely brief sessions** — if a session ends a few seconds after starting, either discard automatically or ask users if they want to record it

### Text Legibility

- Use **large font sizes** for motion contexts
- Use **high-contrast colors**
- Arrange text so the most important information is easiest to read

### Activity Rings

- Use Activity rings **only for their documented purpose** — they are an Apple-designed element with specific ring colors and meanings matching the Activity app

## Platform Support

Supported on **iOS, iPadOS, and watchOS**. Not supported on macOS, tvOS, or visionOS.