# Mac Catalyst Design Guidelines

Guidance for creating a Mac version of an iPad app using Mac Catalyst, covering idiom selection, navigation adaptation, input mapping, layout, and menu integration.

## Suitability Assessment

Good candidates already support:
- **Drag and drop** — transfers directly to Mac
- **Keyboard navigation and shortcuts** — expected on Mac
- **Multitasking** (Split View, Slide Over, PiP) — groundwork for Mac window resizability
- **Multiple scenes** — maps to multiple windows on macOS

**Not suitable** if the app relies on gyroscope, accelerometer, rear camera, HealthKit, ARKit, or primary functions like marking, handwriting, or navigation.

## Automatic macOS Features

Mac Catalyst automatically provides:
- Pointer interactions, keyboard-based focus/navigation
- Window management
- Toolbars
- Rich text interaction (copy/paste, contextual menus)
- File management
- Menu bar menus
- App-specific settings in system Settings app

System UI elements that adopt Mac-like appearance: split view, file browser, activity view, form sheet, contextual actions, color picker.

## Choosing an Idiom

### iPad Idiom (Default)
- iPadOS views and text scale down to **77%** in macOS
- 17pt iPadOS baseline font → 13pt in macOS
- Consistent layout without significant changes
- Text and graphics may appear slightly less detailed

### Mac Idiom
- Text and artwork render at **100%** (more detail)
- More Mac-like appearance for interface elements
- Better performance for graphics-intensive apps, lower power consumption
- **Requires additional layout work**

### Mac Idiom Adoption Checklist
- Thoroughly audit and update layout
- Consider a **separate asset catalog** for Mac assets
- Adjust font sizes (100% rendering can appear too large); use **text styles** instead of fixed sizes
- Verify views and images look correct at full resolution
- Limit appearance customizations to those available in macOS
- Avoid fixed font, view, or layout sizes to reduce work

## Navigation Adaptation

### iPad → Mac Navigation Mapping

| iPad Component | Mac Equivalent |
|---|---|
| Tab bar | Split view with sidebar OR segmented control |
| Split view | Split view (sidebar drives content) |
| Page controls | Next/Previous buttons + gestures |

### Choosing Between Sidebar and Segmented Control
- **Sidebar**: Best for hierarchical navigation; each tab's contents available within sidebar; creates consistent layout between iPad and Mac
- **Segmented control**: Works for flat navigation hierarchies; accommodates mutually exclusive selection like a tab bar

### Key Navigation Guidelines
- Ensure all important tab-bar items remain accessible; list top-level items in the macOS **View menu**
- Provide **multiple navigation methods**: Next/Previous buttons alongside trackpad/gesture-based swiping

## Input Mapping

### iPadOS → Mouse

| iPadOS Gesture | Mouse Interaction |
|---|---|
| Tap | Left or right click |
| Touch and hold | Click and hold |
| Pan | Left click and drag |

### iPadOS → Trackpad

| iPadOS Gesture | Trackpad Gesture |
|---|---|
| Tap | Click |
| Touch and hold | Click and hold |
| Pan | Click and drag |
| Pinch | Pinch |
| Rotate | Rotate |

Note: Pinch and rotate gestures send both touches to the view under the pointer, not the view under each touch.

## App Icons

Create a **dedicated macOS app icon** using the lifelike rendering style expected in macOS while maintaining cross-platform harmony.

## Layout Adaptation

- Divide single-column content into **multiple columns** for wider Mac screens
- Use **regular-width and regular-height size classes**; reflow elements side-by-side as windows resize
- Replace **popovers with inspector UI** next to main content
- Move controls from iPad main UI to the Mac **toolbar**; list associated commands in the menu bar
- Adopt a **top-down flow** — important actions/content near window top
- Relocate buttons from **side/bottom screen edges** to other areas or the toolbar (ergonomic iPad placement doesn't apply on Mac)

## Menus

- Mac users expect **all commands in the menu bar**
- Pop-up and pull-down button menus automatically adopt macOS appearance
- iPadOS context menus automatically convert to macOS context menus
- Add context menus to **every object** — Mac users expect them everywhere
- Use `UIKeyCommand` for keyboard shortcuts on menu commands
- Use `UIMenuBuilder` to add/remove custom app menus; use `UICommand` for menu items