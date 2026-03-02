# Buttons

Guidelines for designing buttons across Apple platforms. A button initiates an instantaneous action, combining style, content, and role to communicate its function.

## Best Practices

- **Hit region**: Minimum 44×44 pt (60×60 pt in visionOS) for easy selection regardless of input method.
- **Always include a press state** for custom buttons to provide responsive feedback.
- Use **prominent visual style** (accent color background) for the most likely action — limit to 1–2 prominent buttons per view.
- Use **style — not size** — to distinguish the preferred choice among multiple options. Keep buttons in a set the same size.
- Avoid applying a similar color to button labels and content layer backgrounds. If content is colorful, prefer monochromatic button labels.

## Content

- Each button should clearly communicate its purpose via a symbol/icon, text label, or both.
- Use **familiar icons for familiar actions** (e.g., `square.and.arrow.up` for share).
- Use **text** when a short label communicates more clearly than an icon. Use title-style capitalization, starting with a verb (e.g., "Add to Cart").
- In macOS and visionOS, the system displays a **tooltip** on hover for icon-only buttons.

## Roles

| Role | Meaning | Appearance |
|---|---|---|
| Normal | No specific meaning | Default |
| Primary | Default/most likely choice | Uses accent color |
| Cancel | Cancels current action | Standard |
| Destructive | May result in data destruction | System red color |

- Assign **primary role** to the button people are most likely to choose (responds to Return key, auto-closes temporary views).
- **Never assign primary role to destructive actions**, even if most likely — people may click without reading.

## iOS / iPadOS

- Use an **activity indicator** within a button for actions that don't complete instantly. Can display an alternative label (e.g., "Checkout" → "Checking out…").

## macOS

### Push Buttons
- Standard button type; can display text, symbol, icon, image, or combinations.
- Use **flexible-height push buttons** only for tall or variable-height content.
- **Append trailing ellipsis (…)** to title when button opens another window, view, or app.
- Consider supporting **spring loading** (Magic Trackpad force click to activate without dropping dragged items).

### Square Buttons (Gradient Buttons)
- Used for view-related actions (e.g., adding/removing table rows).
- Contain symbols or icons only — no text.
- Place in close proximity to associated view, not in window frame/toolbars.
- Prefer SF Symbols.

### Help Buttons
- Circular button with question mark; opens app-specific help documentation.
- Use the system-provided help button.
- Open context-specific help topic when possible.
- Maximum one help button per window.

| View Style | Help Button Location |
|---|---|
| Dialog with dismissal buttons | Lower corner, opposite dismissal buttons, vertically aligned |
| Dialog without dismissal buttons | Lower-left or lower-right corner |
| Settings window or pane | Lower-left or lower-right corner |

- Don't place in toolbars or status bars.

### Image Buttons
- Displays an image, symbol, or icon in a view (not window frame).
- Include ~10 px padding between image edges and button edges.
- Position labels below the image button if needed.

## visionOS

Buttons include a visible background and play sound for feedback.

### Shapes
- **Circular**: icon-only buttons
- **Capsule**: text-only or text+icon buttons
- **Rounded rectangle**: text-only buttons

### Sizes

| Shape | Mini (28 pt) | Small (32 pt) | Regular (44 pt) | Large (52 pt) | Extra Large (64 pt) |
|---|---|---|---|---|---|
| Circular | ✓ | ✓ | ✓ | ✓ | ✓ |
| Capsule (text only) | | ✓ | ✓ | ✓ | |
| Capsule (text+icon) | | | ✓ | ✓ | |
| Rounded rectangle | | ✓ | ✓ | ✓ | |

### Interaction States
Idle, Hover, Selected (white background/black content — reserved style), Unavailable.

### Key Guidelines
- Prefer buttons with **discernible background shape and fill**.
  - On glass windows: use `thin` material as background.
  - Floating in space: use glass material.
- **Don't use white background with black text/icons** for custom buttons (reserved for toggled state).
- Prefer **circular or capsule shapes** (easier to look at steadily than rectangles).
- Space button centers **at least 60 pt apart**. For buttons ≥60 pt, add 4 pt padding to prevent hover overlap.
- Avoid small/mini buttons in vertical stacks or horizontal rows.
- Use **rounded rectangle** in vertical stacks; **capsule** in horizontal rows.
- Buttons don't support custom hover effects.
- Use standard controls for built-in audible feedback (no haptics in visionOS).

## watchOS

- All inline buttons use **capsule** shape with material effect for legibility.
- Use **toolbar** to place buttons in corners (system applies Liquid Glass appearance).
- Prefer **full-width buttons** for primary actions (easier to tap).
- If two buttons share horizontal space, use same height and short text/images.
- Use **same height** for vertical stacks of text buttons.