# Search Fields

Guidelines for designing search fields across Apple platforms — an editable text field with a Search icon, Clear button, and placeholder text.

## Best Practices

- **Display placeholder text describing what people can search for.** E.g., "Shows, Movies, and More" — avoid generic terms like "Search".
- **Start search immediately as a person types** to feel more responsive with continuously refined results.
- **Show suggested search terms** before or during typing to help people search faster.
- **Simplify search results.** Prioritize the most relevant results first; consider categorizing them.
- **Let people filter search results** — e.g., with a scope control in the results area.

## Scope Controls and Tokens

- **Scope control**: Acts like a segmented control for choosing a search category.
- **Token**: A visual representation of a search term that can be selected/edited, acting as a filter.

### Scope Control Guidelines
- Use to filter among clearly defined search categories.
- Default to a broader scope; let people refine as needed.

### Token Guidelines
- Use tokens to filter by common search terms or items (e.g., filtering by a contact in Mail, or by photos in Messages).
- Consider pairing tokens with search suggestions so people discover available tokens.

## iOS

Three main search entry point positions:
1. **Tab bar** (bottom of screen)
2. **Toolbar** (bottom or top)
3. **Inline** with content

### Search in a Tab Bar

Place as a visually distinct tab on the trailing side. The search field can start **focused** or **unfocused**:

- **Focused**: Keyboard appears immediately; provides a transient experience returning to the previous tab after exiting. Ideal for quick, seamless search.
- **Unfocused**: Search tab expands into an unselected field at bottom; screen space available for discovery content. Good for apps with large content collections (Music, TV).

### Search in a Toolbar

- **Bottom toolbar**: Include as an expanded field or toolbar button. Tapping animates into a search field above keyboard. Use when search is a priority and easy reach matters. Examples: Settings (only item), Mail and Notes (alongside other controls).
- **Top toolbar (navigation bar)**: Appears as a toolbar button; tapping animates into a search field above keyboard or inline at top. Use when content at the bottom shouldn't be covered or there's no bottom toolbar. Example: Wallet app with event passes at bottom.

### Search as Inline Field

- Place inline when positioning alongside the content strengthens the relationship (e.g., filtering within a library view in Music).
- **Prefer placing search at bottom** even for subset searches — easier to reach.
- When at the top, position above the list it searches and pin to the top toolbar when scrolling.

## iPadOS & macOS

Placement and behavior are similar on both platforms. Clearing the field exits search and dismisses keyboard.

- **Trailing side of toolbar** for common uses — especially apps with split views or multiple sources (Mail, Notes, Voice Memos). Start with global scope.
- **Top of sidebar** to filter sidebar content/navigation (e.g., Settings).
- **Sidebar or tab bar item** for a dedicated discovery area with rich suggestions, categories, and content (Music, TV).
- In a dedicated area, consider **immediately focusing the field** when navigated to — except on iPad with virtual keyboard only (leave unfocused to prevent unexpected keyboard appearance).
- **Account for window resizing**: Search field fluidly resizes with the window. For compact views, ensure search is contextually placed (e.g., Notes and Mail place search above the content list column).

## tvOS

Search screen is a specialized keyboard screen with results displayed beneath the keyboard in a customizable view.

- **Provide suggestions** (popular, context-specific, recent searches) to minimize typing.

## watchOS

Tapping the search field displays a full-screen text-input control. The app returns to the search field after tapping Cancel or Search.