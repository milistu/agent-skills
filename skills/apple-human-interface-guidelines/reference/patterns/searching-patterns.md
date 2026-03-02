# Searching Pattern

Guidelines for implementing search experiences across Apple platforms.

## Best Practices

- **If search is important, make it a primary action.** Give it a distinct tab in the tab bar or place the search field in the toolbar for clear visibility.
- **Aim for a single search location.** People expect one clearly identified place to find anything in your app. For apps with distinct sections, offer local search that filters the current view.
- **Use placeholder text to indicate searchable content.** E.g., the Apple TV app uses "Shows, Movies, and More".
- **Clearly display the current search scope.** Use descriptive placeholder text, a scope control, or a title to reinforce what's being searched.
- **Provide suggestions to make searching easier.** Display recent searches and offer search suggestions before and while typing. See `searchSuggestions(_:)` in SwiftUI.
- **Consider privacy before displaying search history.** People may not want search history visible to others. Provide alternatives to narrow searches, and if you show history, let people clear it.

## Systemwide Search (Spotlight)

- **Make your app's content searchable in Spotlight.** Share content by making it indexable with descriptive metadata attributes. Spotlight extracts, stores, and organizes this for fast searches.
- **Define metadata for custom file types.** Supply a Spotlight File Importer plug-in (`CSImportExtension`) describing the metadata your file format contains.
- **Use Spotlight for advanced file-search within your app.** E.g., a button that initiates a Spotlight search based on the current selection, displaying results in a custom view.
- **Prefer system-provided open and save views.** They include built-in search fields for searching and filtering the entire system.
- **Implement a Quick Look generator for custom file types.** Helps Spotlight and other apps show previews of your documents.

## Platform Considerations

No additional platform-specific considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.

## Related Components

- [Search fields](/design/human-interface-guidelines/search-fields) — scope controls and tokens
- [Tab bars](/design/human-interface-guidelines/tab-bars)
- [Toolbars](/design/human-interface-guidelines/toolbars)