# Menus - Apple HIG

Guidelines for designing menus that reveal options when people interact with them, covering labels, icons, organization, submenus, toggled items, and platform-specific considerations.

## Labels

- **Write clear, succinct labels** — Use a verb or verb phrase for action items (e.g., View, Close, Select)
- **Use title-style capitalization** — Capitalize every word except articles, coordinating conjunctions, and short prepositions; always capitalize the last word
- **Remove articles** (*a*, *an*, *the*) from labels to save space
- **Dim unavailable items** — Show them as unavailable but keep the menu itself openable so people can discover available commands
- **Append an ellipsis (…)** when the action requires additional input before completing

## Icons

- **Use familiar icons** for common actions (Copy, Share, Delete) — match system-provided icons
- **Don't add icons** if no clear representation exists; avoid decorative-only icons
- **For a group of similar items**, use a single icon on the first item only, then rely on text labels for the rest (e.g., a Copy icon on the first copy action, no icons on subsequent copy variants)

## Organization

- **List important/frequently used items first** — people scan from the top
- **Group logically related items** with separators (horizontal line or gap)
- **Keep related commands together** even if they differ in frequency of use (e.g., Paste and Paste and Match Style belong in the same group)
- **Avoid excessively long menus** — consider splitting into separate menus or using submenus. Exception: user-defined/dynamic content (e.g., History, Bookmarks) where long lists and scrolling are acceptable

## Submenus

- **Use sparingly** — each submenu adds complexity and hides items
- Consider a submenu when a term appears in more than two menu items in the same group (e.g., "Sort by" → Date, Score, Time)
- **Limit to a single level** of nesting; keep submenus to ~5 items max
- **Keep submenus available** even when all nested items are unavailable
- **Prefer submenus over indented menu items** — indentation is non-standard

## Toggled Items

- **Use a changeable label** to describe current state (e.g., Show Map ↔ Hide Map)
- **Add a verb** if the toggled label is ambiguous (e.g., "Turn HDR On" instead of "HDR On")
- **Show both items** when viewing both states simultaneously helps (e.g., Take Account Online / Take Account Offline with one dimmed)
- **Use checkmarks** to indicate currently active attributes in a list
- **Offer a "clear all" item** (e.g., Plain) to remove multiple toggled attributes at once

## In-Game Menus

- **Use platform-default interaction methods** for menu navigation (touch on iOS/iPadOS, gestures on visionOS)
- **Ensure menus are legible and tappable on all supported platforms** — scale tap targets appropriately for smaller screens

## Platform-Specific

### iOS / iPadOS

Three menu layout sizes (via `UIMenu.preferredElementSize`):

| Layout | Top Row Items | Labels | Use Case |
|--------|--------------|--------|----------|
| **Small** | 4 items | Icons/symbols only | Closely related actions (Bold, Italic, Underline, Strikethrough) |
| **Medium** | 3 items | Symbol + short label | Important frequent actions (e.g., Scan, Lock, Pin) |
| **Large** (default) | N/A | Full list | General use |

Remaining items appear in a list below the top row for small/medium layouts.

### visionOS

- Supports small and large layout styles (same as iOS/iPadOS)
- **Display menus near the content they control** — people look at items before tapping
- Menus can appear outside window boundaries
- **Breakthrough effects** for menus overlapping 3D content:
  - `subtle` (default/recommended) — blends with surroundings, maintains legibility
  - `prominent` — displays prominently over entire scene; can cause discomfort
  - `none` — fully occluded by 3D content; use only for specific game mechanics

### macOS, tvOS, watchOS

No additional considerations.