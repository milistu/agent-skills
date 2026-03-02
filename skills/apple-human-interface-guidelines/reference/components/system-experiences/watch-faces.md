# Watch Faces

Guidelines for creating and sharing watch faces in watchOS.

A watch face is the primary view people see every time they raise their wrist. People customize watch faces with complications and can configure different faces for different activities. In watchOS 7+, watch faces can be shared from apps, websites, or via Messages, Mail, and social media.

## Best Practices

- **Share watch faces featuring your complications** to help people discover your app. Support multiple complications to showcase them in a shareable watch face. For some faces, you can also specify a system accent color, images, or styles. If people add your watch face but haven't installed your app, the system prompts them to install it.

- **Display a preview of each shared watch face.** Get a preview by using the iOS Watch app to email the watch face to yourself. The preview includes an illustrated device bezel suitable for websites and apps. You can replace it with a high-fidelity hardware bezel from [Apple Design Resources](https://developer.apple.com/design/resources/#product-bezels).

- **Offer shareable watch faces for all Apple Watch devices.** Some faces are only available on Series 4+ (California, Chronograph Pro, Gradient, Infograph, Infograph Modular, Meridian, Modular Compact, Solar Dial). Explorer is available on Series 3 (cellular)+. For these, consider offering an alternative configuration using a face available on Series 3 and earlier. Clearly label each shareable watch face with supported devices.

- **Respond gracefully to incompatible watch faces.** When the system sends an error for an incompatible face on Series 3 or earlier, immediately offer an alternative compatible configuration instead of displaying an error. Help people understand they might receive an alternative face.

## Platform Support

watchOS only. Not supported in iOS, iPadOS, macOS, tvOS, or visionOS.

## Developer Reference

- [Sharing an Apple Watch face](https://developer.apple.com/documentation/ClockKit/sharing-an-apple-watch-face) — ClockKit