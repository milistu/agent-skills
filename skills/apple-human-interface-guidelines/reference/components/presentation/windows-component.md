# Windows

Guidelines for presenting UI views and components in windows across iPadOS, macOS, and visionOS.

**Not supported in iOS, tvOS, or watchOS.**

## Window Types

- **Primary window**: Presents the main navigation and content of an app, and actions associated with them.
- **Auxiliary window**: Presents a specific task or area in an app. Dedicated to one experience, doesn't allow navigation to other app areas, and typically includes a close button.

## Best Practices

- **Adapt fluidly to different sizes** to support multitasking and multiwindow workflows.
- **Choose the right moment to open a new window.** Opening content in a separate window helps people multitask or preserve context (e.g., Mail opens a new window for Compose). Avoid opening new windows as default behavior unless it clearly benefits UX.
- **Offer the option to view content in a new window** via context menus or the File menu, even if it's not the default.
- **Don't create custom window UI.** Use system-provided window frames and controls. Custom frames/controls that don't perfectly match the system feel broken.
- **Use the term "window"** in user-facing content, not "scene" (which is an implementation term).

## iPadOS

Windows present in two modes based on user settings:
- **Full screen**: Windows fill the entire screen; switch via app switcher.
- **Windowed**: Freely resizable, multiple onscreen, repositionable. System remembers size and placement.

### iPadOS Guidelines

- **Ensure window controls don't overlap toolbar items.** In windowed mode, window controls appear at the leading edge of the toolbar. Move leading toolbar buttons inward when window controls appear.
- **Consider gestures to open content in a new window** (e.g., pinch to expand a Notes item).

## macOS

People run several apps simultaneously, viewing and switching between windows from multiple apps.

### Window Anatomy

- **Frame**: Above the body area; contains window controls and toolbar. Rare: a bottom bar below body content.
- **Body**: Main content area.
- People move windows by dragging the frame and resize by dragging edges.

### Window States

| State | Description |
|---|---|
| **Main** | Frontmost window of an app. One per app. |
| **Key** (active) | Accepts user input. One key window onscreen at a time. Usually the main window, but could be a panel. |
| **Inactive** | Not in foreground. Subdued appearance, no vibrancy. |

- Key window: colored title bar controls. Inactive/main-not-key: gray controls.
- Some windows (e.g., Colors, Fonts panels) only become key when clicking the title bar or a text field.

### macOS Guidelines

- **Ensure custom windows use system-defined appearances** for main/key/inactive states. System components update automatically; custom ones need manual handling.
- **Avoid putting critical info in a bottom bar** — people often hide the bottom edge. Use it only for small, directly related info (like Finder's status bar). For more info, consider an inspector in a split view.

## visionOS

Two main window styles: **default** (window) and **volumetric** (volume). Both display 2D and 3D content; multiple can be viewed simultaneously in Shared Space or Full Space.

Additional style: **plain** — like default but without the glass background (`PlainWindowStyle`).

The system defines the initial position of the first window/volume. People can move them afterward.

### visionOS Windows (Default Style)

An upright plane with glass background material (unmodifiable), close button, window bar, resize controls. Can include Share button, tab bar, toolbar, and ornaments. Uses dynamic scale by default.

#### Window Guidelines

- **Use windows for familiar interfaces and tasks.** Reserve immersive experiences for meaningful content.
- **Retain the glass background.** It adapts to lighting, provides reflections/shadows, and keeps text legible. Removing it hurts legibility; opaque backgrounds feel constricting.
- **Default size: 1280×720 pt.** Placed ~2 meters from the wearer (~3m apparent width). Minimize empty areas — excessive empty space makes the window unnecessarily large.
- **Choose an initial shape that suits content.** Wide for Keynote (slides), tall for Safari (webpages), game-appropriate shapes.
- **Set minimum and maximum sizes** so content looks great at all sizes. Prevent overlap at small sizes or unusability at large sizes.
- **Minimize 3D content depth in windows.** The system adds highlights/shadows for apparent depth. Content extending too far from the surface gets clipped. Use volumes for deeper 3D content.

### visionOS Volumes (Volumetric Style)

Display 2D or 3D content viewable from any angle. Includes window-management controls; close button and window bar face the viewer as they move around.

#### Volume Guidelines

- **Use volumes for rich 3D content.** Use windows for UI-centric interfaces.
- **Place 2D content carefully** — perspective changes as people move around, so 2D positioning may appear incorrect. Use attachments to pin 2D content to 3D objects.
- **Use dynamic scaling** (generally) for legibility at distance. Use fixed scaling (the default) when representing real-world objects.
- **Leverage the default baseplate glow** (visionOS 2+) to help people discern volume edges and find the resize control. Disable if content is full bleed or you have a custom baseplate.
- **Offer high-value content in an ornament** (visionOS 2+). Use attachment anchors (e.g., `topBack`, `bottomFront`) to keep ornament position relative to viewer. Don't place on the same edge as toolbar/tab bar. Prefer one additional ornament only.
- **Choose volume alignment based on interaction.** Parallel-to-floor works for passive content; tilt-to-match-gaze works for interactive content (e.g., reclining users).