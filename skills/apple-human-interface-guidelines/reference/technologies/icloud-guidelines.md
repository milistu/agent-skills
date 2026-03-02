# iCloud Design Guidelines

Guidelines for integrating iCloud into apps so users can seamlessly access content across devices.

## Best Practices

- **Make iCloud usage automatic.** People expect apps to work with iCloud once enabled in Settings. If needed, show a simple first-launch option: use iCloud for all data or not at all.

- **Avoid asking which documents to keep in iCloud.** Users expect all content available in iCloud. Perform file-management tasks automatically rather than exposing per-document choices.

- **Keep content up to date.** Balance freshness with storage/bandwidth constraints. For very large documents, let users control when updates download. Indicate when a newer version is available and provide subtle feedback if downloads take more than a few seconds.

- **Respect iCloud storage space.** Store only user-created content — not app resources or regenerable data. iCloud backups include the Documents folder, so be selective about what goes there.

- **Handle iCloud unavailability gracefully.** Don't alert when someone manually disables iCloud or enables Airplane Mode. Unobtrusively note that changes won't sync to other devices until iCloud access is restored.

- **Store app state in iCloud.** Save settings and state (e.g., last page viewed) so users can continue across devices. Only sync settings that make sense across all devices (some may be location/context-specific).

- **Warn before deleting documents.** Deletion removes the document from iCloud and all devices. Show a warning and require confirmation.

- **Resolve conflicts promptly.** Detect and resolve version conflicts automatically when possible. If not, show an unobtrusive notification to differentiate and choose between conflicting versions. Resolve conflicts early to avoid wasted time.

- **Include iCloud content in search results.** Users expect search to surface content from iCloud.

- **For games, save player progress in iCloud.** Use the GameSave framework for efficient cross-device save data synchronization with built-in alerts for offline play and conflict handling.