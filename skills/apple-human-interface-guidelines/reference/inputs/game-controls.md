# Game Controls

Guidelines for designing touch controls, physical game controller support, and keyboard bindings for games on Apple platforms.

## Touch Controls (iOS/iPadOS)

**Virtual controls vs. direct interaction:** Reduce virtual control overlays by associating actions with in-game gestures (e.g., tap objects to select instead of adding a virtual selection button).

### Placement
- Respect device boundaries and safe areas; avoid overlapping Home indicator or Dynamic Island
- Place frequently used buttons near thumbs
- Avoid circular regions where players expect movement/camera input
- Place secondary controls (menus) at the top of the screen
- Movement control: left side of screen
- Camera control: right side of screen

### Sizing
- Frequently used controls: minimum **44×44 pt**
- Less important controls (menus): minimum **28×28 pt**

### Press States
- Always include visible and tactile press states
- Add visual effects (e.g., glow) visible even when finger covers the control
- Combine with sound and haptics for feedback

### Button Design
- Use symbols that communicate actions (e.g., weapon graphic for attack)
- Avoid abstract shapes or controller-based labels (A, X, R1)

### Dynamic Controls
- Show/hide virtual controls based on gameplay context to reduce clutter
- Fade controls when not in use; show highlight when active
- Show virtual thumbstick wherever the player lands their thumb (not static position)
- For camera, prefer direct touch panning over a virtual thumbstick

### Combining Actions
- Redesign mechanics requiring simultaneous multi-button presses
- Use double-tap and touch-and-hold for action variations (e.g., hold for powered-up attack)
- Combine related actions (walk/sprint) into a single control

## Physical Controllers

- Always support the platform's default interaction method as fallback (touch on iOS/iPadOS, keyboard+mouse on Mac, remote on tvOS, eyes+hands on visionOS)
- Auto-detect paired controllers instead of requiring manual setup
- Customize onscreen content to match the connected controller's labeling scheme (colors, symbols)
- On tvOS and visionOS, you can require a controller; App Store shows "Game Controller Required" badge. Check for controller presence and gracefully prompt connection.

### Standard UI Button Mapping

| Button | Expected UI Behavior |
| --- | --- |
| A | Activates a control |
| B | Cancels action / returns to previous screen |
| X | — |
| Y | — |
| Left shoulder | Navigate left to different screen/section |
| Right shoulder | Navigate right to different screen/section |
| Left/Right thumbstick | Moves selection |
| Directional pad | Moves selection |
| Home/logo | Reserved for system |
| Menu | Opens settings / pauses gameplay |

### Multiple Controllers
- Use labels/glyphs matching the actively-used controller
- In multiplayer, use appropriate labels per player's controller
- When referencing multiple controllers, list them together

### Symbols
- Prefer SF Symbols (Gaming category) over text to refer to controller elements
- Especially helpful for inexperienced controller users

## Keyboards

- **Prioritize single-key commands** — easier/faster, especially when using mouse/trackpad simultaneously
- Use first letter of menu items as shortcuts (I for Inventory, M for Map)
- Map main action to Space bar (large, easy target)
- **Apple keyboard ergonomics:** Remap Control (^) bindings to Command (⌘), which sits next to Space bar near WASD
- **Key proximity:** Place high-value commands near WASD if that's the navigation scheme; group related actions on physically close keys (e.g., number keys for inventory)
- **Let players customize key bindings**

## visionOS

- Match spatial game controller behavior to hand input
- Support look + trigger for indirect interaction
- Support reach + trigger for direct interaction
- Supports wireless game controllers and spatial controllers (e.g., PlayStation VR2 Sense)