# Collections

A collection manages an ordered set of content and presents it in a customizable, highly visual layout. Ideal for showing image-based content.

## Best Practices

- **Use standard row or grid layout whenever possible.** Collections display content by default in a horizontal row or grid. Avoid custom layouts that confuse people or draw undue attention.
- **Consider using a table instead of a collection for text.** Textual information is simpler to view in a scrollable list.
- **Make it easy to choose an item.** Use adequate padding around images to keep focus/hover effects easy to see and prevent content from overlapping.
- **Add custom interactions when necessary.** Default interactions: tap to select, touch and hold to edit, swipe to scroll. Add gestures for custom actions as needed.
- **Consider animations for insert, delete, or reorder operations.** Collections support standard animations; custom animations are also possible.

## Platform Considerations

- **Not supported on watchOS.**
- No additional considerations for macOS, tvOS, or visionOS.

### iOS, iPadOS

- **Use caution with dynamic layout changes.** Avoid changing layout while people are viewing/interacting unless it's in response to an explicit action. Ensure changes make sense and are easy to track.

## Related Components

- Lists and tables
- Image views
- Layout