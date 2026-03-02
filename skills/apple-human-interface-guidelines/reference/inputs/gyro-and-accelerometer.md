# Gyroscope and Accelerometer

Guidelines for using on-device gyroscope and accelerometer data in iOS, iPadOS, watchOS, and tvOS (Siri Remote) apps.

## Best Practices

- **Use motion data only to offer a tangible benefit to people.** For example, a fitness app might use data for activity feedback, or a game might enhance gameplay. Avoid gathering data simply to have it.

- **You must provide copy explaining why your app needs motion data access.** The system displays this copy in a permission request the first time your app tries to access motion data, where people can grant or deny access.

- **Outside of active gameplay, avoid using accelerometers or gyroscopes for direct manipulation of your interface.** Some motion-based gestures may be difficult to replicate precisely, may be physically challenging for some people to perform, and may affect battery usage.

## Platform Availability

- **iOS/iPadOS**: Accelerometer and gyroscope via Core Motion
- **watchOS**: Accelerometer and gyroscope via Core Motion
- **tvOS**: Gyroscope data from Siri Remote
- **macOS/visionOS**: Not applicable