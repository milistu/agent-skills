# Notifications

Guidelines for designing notifications across Apple platforms — including content, actions, badging, and watchOS-specific considerations.

## Best Practices

- **Provide concise, informative notifications.** People turn on notifications for quick updates; provide valuable information succinctly.
- **Avoid sending multiple notifications for the same thing**, even if someone hasn't responded. This fills Notification Center and people may disable all notifications from your app.
- **Avoid telling people to perform specific tasks within your app.** Instructions are hard to remember after dismissal. Use notification actions for simple tasks instead.
- **Use alerts — not notifications — for error messages.** See Alerts guidelines.
- **Handle notifications gracefully when your app is in the foreground.** Present info in a discoverable but non-distracting way (e.g., incrementing a badge, inserting new data into the current view).
- **Avoid including sensitive, personal, or confidential information** — notifications may be visible to others.

## Content

The system displays the sender's name for communication notifications; for noncommunication notifications, it shows your app name if no title is provided.

- **Create a short title if it provides context.** Use brief, glanceable titles. Use title-style capitalization, no ending punctuation.
- **Write succinct, easy-to-read body content.** Use complete sentences, sentence case, proper punctuation. Don't truncate — the system handles this.
- **Provide generic placeholder text for hidden previews.** When previews are hidden, the system shows only your app icon and "Notification" as the title. Write body text that gives context without revealing details (e.g., "Friend request," "New comment," "Reminder"). Use sentence-style capitalization. See `hiddenPreviewsBodyPlaceholder`.
- **Avoid including your app name or icon.** The system displays these automatically.
- **Consider providing a sound.** Custom sounds should be short, distinctive, and professionally produced. Don't rely on sound alone for important information.

## Notification Actions

Notifications can present a detail view with up to four action buttons.

- **Provide beneficial actions that eliminate the need to open your app.** Use short, title-case labels that clearly describe the result.
- **Don't include your app name or extraneous info in button labels.** Keep text brief; account for localization.
- **Avoid providing an action that merely opens your app.** Tapping the notification already does this.
- **Prefer nondestructive actions.** If destructive actions are necessary, ensure people have enough context. The system gives destructive actions a distinct appearance.
- **Provide a recognizable interface icon for each action.** Use SF Symbols — choose an existing symbol or edit one for a custom icon. Displayed on the trailing side of the action title.

## Badging

A badge is a small filled oval with a number on an app icon indicating unread notifications.

- **Use badges only for unread notification counts.** Don't use for unrelated numeric info (weather, dates, scores).
- **Don't rely solely on badging for essential information.** People can disable badges.
- **Keep badges up to date.** Update as people open corresponding notifications. Reducing count to zero removes all related notifications from Notification Center.
- **Don't create custom images mimicking badge appearance.** People who disable badges will be frustrated by fake badges.

## watchOS Considerations

Notifications occur in two stages: **short look** and **long look**. People can also view notifications in Notification Center and respond via double tap on supported devices.

### Short Looks

Appears when the wearer's wrist is raised; disappears when lowered.

- **Don't use short looks as the only way to communicate important information.** They appear only briefly.
- **Keep privacy in mind.** Provide only basic information; avoid sensitive content in the title.

### Long Looks

Provide more detail; scrollable via swipe or Digital Crown. Can be **static** or **dynamic**.

- **Static interface:** Displays notification message with additional static text and images.
- **Dynamic interface:** Full access to notification content with more appearance options.

Structure includes a **sash** (top, showing app icon/name) and a **Dismiss button** (bottom, below custom buttons).

- **Use rich, custom long-look notifications** to let people get info without launching your app. Use SwiftUI Animations, SpriteKit, or SceneKit.
- **At minimum, provide a static interface; prefer providing dynamic too.** The system falls back to static when dynamic is unavailable.
- **Customize the sash:** Choose a background color or blurred appearance. Use blurred sash when displaying a photo at the top.
- **Content area background:** Default is transparent. For system-matching appearance, use white with 18% opacity; or use a custom/brand color.
- **Provide up to four custom action buttons** below the content area. The system determines which to display based on notification type.

### Double Tap

On supported devices, double tap selects the **first nondestructive action** as the response.

- **Place the most frequently used action first** in the list of custom actions, since double tap triggers it automatically.