# Apple Pencil and Scribble

Design guidelines for Apple Pencil interactions on iPad, including hover, double tap, squeeze, barrel roll, Scribble text entry, and custom drawing.

## Best Practices

- **Support intuitive marking instrument behaviors.** Think about how people use real-world pencils and pens, and proactively support natural actions (e.g., writing in margins).
- **Let people use Apple Pencil and finger input interchangeably.** All app controls should respond to Apple Pencil — an unresponsive control feels broken. (Scribble only supports Apple Pencil input.)
- **Let people mark the moment Apple Pencil touches the screen.** Don't require tapping a button or entering a special mode first.
- **Respond to Apple Pencil properties:** tilt (altitude), force (pressure), orientation (azimuth), and barrel roll. Vary stroke thickness and intensity. Keep pressure responses intuitive — affect continuous properties like opacity or brush size.
- **Provide direct visual feedback.** Apple Pencil should appear to directly manipulate content it touches. Avoid disconnected actions or affecting content elsewhere on screen.
- **Design for left- and right-handed use.** Don't place controls where either hand may obscure them. Consider letting people reposition controls.

## Hover

- **Use hover to preview** what will happen when Apple Pencil touches the screen (e.g., tool dimensions and color). Avoid continuously modifying the preview as distance changes — frequent variations are distracting.
- **Never use hover to initiate an action.** Hovering is imprecise; people may inadvertently trigger actions, especially destructive ones.
- **Show mid-range preview values.** For dynamic properties like opacity, preview a middle value — max values may occlude content; min values may be invisible.
- **Use hover for contextual interactions** near the marking area (e.g., show a tool-size menu on squeeze or modifier key press).
- **Prefer showing hover previews for Apple Pencil only**, not pointing devices. See `UIKit` > Adopting hover support for Apple Pencil.

## Double Tap

- **Respect system settings** for double-tap gesture: toggle current tool/eraser, toggle current/previous tool, show/hide color picker, or do nothing. If system behaviors don't apply, you can use double tap to change interaction mode (e.g., toggle between raise/lower in a mesh editor).
- **Provide a control for custom double-tap behavior** so people can discover and choose it. Don't enable custom behavior by default.
- **Never use double tap for destructive or content-modifying actions.** Accidental double taps happen; only trigger easily undoable actions.

## Squeeze (Apple Pencil Pro)

People can squeeze Apple Pencil Pro to perform an action. They may configure squeeze to run an App Shortcut instead of app-specific actions.

- **Treat squeeze as a single, quick, discrete action.** Don't require holding or repeated squeezing — it's tiring.
- **Display squeeze results (e.g., contextual menus) near the Apple Pencil Pro tip** to maintain the connection between gesture and result.
- **Squeeze actions must be nondestructive and easy to undo.** Accidental squeezes happen.

> Note: Squeeze only works when the paired iPad screen is on and Apple Pencil Pro is not touching it. People may not always see the result.

## Barrel Roll (Apple Pencil Pro)

- **Use barrel roll only to modify marking behavior** (e.g., rotating highlight angle in Notes). Do not use it for navigation or displaying controls.

## Scribble

Scribble lets people write with Apple Pencil in any text field using on-device handwriting recognition. Available in all standard text components by default (except password fields).

- **Don't require tap/select before writing** in custom text fields.
- **Make Scribble available everywhere text entry seems natural** — even areas without explicit text fields (e.g., writing a new reminder in blank space). See `UIIndirectScribbleInteraction`.
- **Avoid displaying autocompletion while writing** — suggestions visually interfere with handwriting.
- **Hide placeholder text immediately** when writing begins so input doesn't overlap it.
- **Keep text fields stationary while people write.** If movement is unavoidable, delay until a writing pause.
- **Prevent text autoscrolling during writing/editing** — it causes misselection and disorientation.
- **Give enough space to write.** Increase text field size before or between writing sessions. Avoid resizing during writing. See `UIScribbleInteraction`.

## Custom Drawing (PencilKit)

- **Drawing on existing content (PDF, photo):** Disable dynamic Dark Mode color adjustment so markup stays sharp and visible. Default canvas colors adjust to Dark Mode automatically.
- **Compact environments:** The tool picker omits undo/redo buttons. Display custom undo/redo buttons in a toolbar and consider supporting the 3-finger undo/redo gesture.

## Platform Support

iPadOS only. Not supported in iOS, macOS, tvOS, visionOS, or watchOS.