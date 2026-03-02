# Gestures

Guidelines for designing gesture interactions across Apple platforms.

## Best Practices

- **Provide multiple interaction methods.** Don't assume people can use a specific gesture. Support voice, keyboard, Switch Control, etc.
- **Respond consistently with expectations.** Don't repurpose familiar gestures (tap, swipe) for unique app-specific actions, and don't create custom gestures for standard actions.
- **Handle gestures responsively.** Provide immediate feedback helping people predict results and understand required movement.
- **Indicate when a gesture isn't available.** Clearly communicate locked states, unavailable buttons, etc. to avoid confusion.

## Custom Gestures

- Add custom gestures only for specialized, frequent tasks not covered by existing gestures (e.g., games, drawing apps)
- Custom gestures must be: discoverable, straightforward to perform, distinct from other gestures, and not the only way to perform an important action
- Use simple language and graphics to teach custom gestures; if hard to describe, it's hard to learn
- Use shortcut gestures to supplement (not replace) standard gestures — always provide a standard fallback
- Avoid conflicting with system gestures (edge swiping in watchOS, hand-rolling in visionOS)

## Standard Gestures (All Platforms)

| Gesture | Supported in | Common action |
| --- | --- | --- |
| Tap | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Activate a control; select an item |
| Swipe | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Reveal actions/controls; dismiss views; scroll |
| Drag | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Move a UI element |
| Touch (or pinch) and hold | iOS, iPadOS, tvOS, visionOS, watchOS | Reveal additional controls or functionality |
| Double tap | iOS, iPadOS, macOS, tvOS, visionOS, watchOS | Zoom in/out; primary action on Apple Watch Series 9/Ultra 2 |
| Zoom | iOS, iPadOS, macOS, tvOS, visionOS | Zoom a view; magnify content |
| Rotate | iOS, iPadOS, macOS, tvOS, visionOS | Rotate a selected item |

## Platform-Specific Guidance

### iOS, iPadOS

Additional gestures:

| Gesture | Common action |
| --- | --- |
| Three-finger swipe | Undo (left swipe); redo (right swipe) |
| Three-finger pinch | Copy selected text (pinch in); paste (pinch out) |
| Four-finger swipe (iPadOS only) | Switch between apps |
| Shake | Undo; redo |

- Consider allowing simultaneous gesture recognition in games (e.g., joystick + firing buttons)

### macOS

Primary input is keyboard and mouse. Standard gestures supported on Magic Trackpad, Magic Mouse, or game controllers with touch surfaces.

### tvOS

Standard gestures work with compatible remote, Siri Remote, or game controllers with touch surfaces.

### visionOS

visionOS supports two gesture categories:

**Indirect gestures:** Look at an object to target it, then manipulate from a distance (e.g., look at button → tap finger and thumb together to select). Comfortable at any distance, minimal movement.

**Direct gestures:** Physically touch interactive objects. Best for objects within reach; can be tiring for extended use.

| Direct gesture | Common use |
| --- | --- |
| Touch | Select or activate an object |
| Touch and hold | Open contextual menu |
| Touch and drag | Move an object |
| Double touch | Preview object/file; select word in editing |
| Swipe | Reveal actions; dismiss views; scroll |
| Two hands, pinch and drag together/apart | Zoom in/out |
| Two hands, pinch and drag circular | Rotate an object |

**Key visionOS guidelines:**
- Support standard gestures everywhere; tap is the first gesture people try
- Offer both indirect and direct interactions; prefer indirect for UI/buttons; reserve direct for close-up interaction
- Avoid requiring specific body movements or positions; support alternative inputs

#### Custom Gestures in visionOS

- App must run in a Full Space; requires hand-tracking permission via ARKit
- Prioritize comfort — avoid requiring raised arms for extended periods
- Avoid requiring specific hands; consider one-handed alternatives
- Complex multi-finger/two-hand gestures should have simpler alternatives

#### System Overlays in visionOS

People look at their palm and gesture to access Home/Control Center overlays.

- **Reserve the area around a person's hand** for system overlays — don't anchor content to hands/wrists
- **Consider deferring system overlay behavior** in immersive Full Space experiences (e.g., games with virtual gloves). Use `persistentSystemOverlays(_:)` to require a tap to reveal the Home indicator
- **Avoid custom gestures with hand/wrist rolling motion** — reserved for system overlays
- visionOS 1 apps defer system overlay by default in Full Space

### watchOS — Double Tap

In watchOS 11+, double tap scrolls lists/scroll views and advances vertical tab views. Can also trigger a primary action in your app, widget, or Live Activity in the Smart Stack.

- **Don't set a primary action** in views with lists, scroll views, or vertical tabs (conflicts with expected navigation)
- **Choose the most commonly used button** as the primary action (e.g., play/pause in media controls)
- Use `handGestureShortcut(_:isEnabled:)` and `primaryAction` for developer implementation
- In notifications, double tap acts on the first nondestructive action