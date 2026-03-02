# Web Views

A web view loads and displays rich web content (embedded HTML, websites) directly within your app.

## Best Practices

- **Support forward and back navigation when appropriate.** Web views support forward and back navigation, but this behavior isn't available by default. If people are likely to visit multiple pages, enable forward/back navigation and provide corresponding controls.
- **Avoid using a web view to build a web browser.** Using a web view to let people briefly access a website without leaving the context of your app is fine, but Safari is the primary way people browse the web. Replicating Safari functionality is unnecessary and discouraged.

## Platform Support

- Supported on: iOS, iPadOS, macOS, visionOS
- Not supported on: tvOS, watchOS

## Implementation

- Use [`WKWebView`](https://developer.apple.com/documentation/WebKit/WKWebView) from WebKit.