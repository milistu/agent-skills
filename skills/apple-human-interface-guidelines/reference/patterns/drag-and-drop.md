# Drag and Drop

Guidelines for implementing drag and drop interactions across Apple platforms (iOS, iPadOS, macOS, visionOS). Not supported in tvOS or watchOS.

## Core Concepts

- **Source**: where content is dragged from; **Destination**: where it's dropped
- Dropping within the same container generally **moves** content; dropping in a different container **copies** it
- Dragging between apps always results in a **copy**

## Best Practices

- **Support drag and drop throughout your app.** Use system-provided components (text fields, text views) for built-in support.
- **Offer alternative ways** to accomplish drag-and-drop actions (e.g., menu commands for copy/move). Use accessibility APIs (`accessibilityDragSourceDescriptors`, `accessibilityDropPointDescriptors`) for assistive technology support.
- **Move vs. copy**: Same container → move; different container → copy. Deviate only when it reduces frustration or data loss.
- **Support multi-item drag and drop** where it makes sense. In iPadOS, people can add items to an in-progress drag session sequentially.
- **Support undo** for drag-and-drop operations. Ask for confirmation before irreversible drops (e.g., macOS Finder dropping into write-only folders).
- **Offer multiple representations** of dragged content ordered from highest to lowest fidelity (e.g., PDF → PNG → JPEG) so the destination can choose the best it supports.
- **Consider supporting spring loading** — activating controls (buttons, segmented controls) by dragging content over them.

## Providing Feedback

- **Display a drag image** (translucent representation) when dragging begins (~3 points of movement). Keep it visible until drop.
- **Modify the drag image** when it adds clarity (e.g., expand to show default photo size in document). Use **drag flocking** to visually group multiple items.
- **Indicate destination acceptance**: Show insertion point or highlight when destination can accept content. Show no feedback or "not allowed" indicator (`circle.slash` SF Symbol) when it can't. Only show feedback while content hovers over the destination.
- **On failed drop**: Animate the item back to source or scale up and fade out.

## Accepting Drops

- **Auto-scroll** destination containers when people drag items within scrolling content.
- **Pick the richest version** of dropped content your app can accept.
- **Extract only relevant portions** of dropped content (e.g., Mail extracts only name and email from a contact).
- **Check for Option key** at drop time (physical keyboard): Option held = force copy within same container; Option released = move.
- **Show transfer progress** (progress indicator, placeholder at drop location) when content needs time to transfer.
- **Provide task feedback** when a drop initiates an action (e.g., printing).
- **Apply appropriate text styling**: Maintain original styles when both source and destination support them; otherwise apply destination styles.
- **Maintain selection state** in the destination after drop. Deselect content in the source when moving to a different container; remove selection from original location when copying within the same container.

## Platform-Specific Guidance

### iOS / iPadOS

- Support **multiple simultaneous drag activities**. Let people add items during a drag with visual flocking feedback and accept multiple simultaneous drops.

### macOS

- **Support dragging content to Finder** in a format your app can reopen (e.g., Calendar exports `.ics` files). Support **clippings** for text content.
- **Let people drag from inactive windows** without activating the window (background selection).
- Let people **drag individual items from inactive windows** without affecting existing background selection.
- **Display a badge** (filled oval with count) during multi-item drags. Update the badge if the destination accepts only a subset.
- **Change pointer appearance** to indicate outcome: copy pointer, drag link, disappearing item, operation not allowed. See Pointers guidelines.
- **Allow single-motion select-and-drag** unless people are selecting multiple items.

### visionOS

- People pinch and hold virtual objects while dragging in any direction, including along the z-axis.
- **Launch your app to handle content dropped into empty space** by associating a `NSUserActivity` with draggable content (e.g., dropping a URL launches Safari, dropping Quick Look content launches Quick Look).