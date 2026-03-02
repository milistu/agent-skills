# Managing Notifications

Guidelines for sending notifications across Apple platforms, including interruption levels, Focus integration, and marketing notification rules.

## Permission

You must get permission before sending any notification. People can change this in Settings, including silencing all notifications (except government alerts in some locales).

## Integrating with Focus

People can filter notifications using **Focus** (for activities like sleeping, working, reading) and **delivery scheduling** (immediate vs. summary at chosen times).

- People identify contacts and apps that can break through a Focus
- Even when a Focus delays alert delivery, the notification itself is available immediately

### Notification Types

- **Communication notifications**: For direct communications (calls, messages). Adopt SiriKit intents (`INSendMessageIntent`, `UNNotificationContentProviding`). System uses the sender to determine delivery timing.
- **Noncommunication notifications**: All other tasks. Require a system-defined interruption level.

### Interruption Levels

| Level | Description | Overrides Scheduled Delivery | Breaks Through Focus | Overrides Ring/Silent Switch |
|---|---|---|---|---|
| **Passive** | Info people view at leisure (e.g., restaurant recommendation) | No | No | No |
| **Active** (default) | Info people might want to know when it arrives (e.g., sports score) | No | No | No |
| **Time Sensitive** | Directly impacts the person, requires immediate attention (e.g., account security, package delivery) | Yes | Yes | No |
| **Critical** | Urgent health/safety info demanding immediate attention. Requires an entitlement. | Yes | Yes | Yes |

> **Note:** Critical notifications require a special entitlement because they override the Ring/Silent switch.

## Best Practices

- **Accurately represent urgency.** People can turn off notifications entirely if they feel misled about urgency levels.
- **Use Time Sensitive only for time-relevant events** — happening now or within an hour. The system shows people controls to evaluate and potentially turn off your Time Sensitive notifications.

## Marketing Notifications

- Only send marketing/promotional notifications if people **explicitly opt in**.
- **Never use Time Sensitive** for marketing notifications — they must not break through Focus or scheduled delivery.
- **Request permission explicitly** via an alert, modal, or other UI that describes what you'll send and gives a clear opt-in/opt-out.
- **Provide in-app notification settings** so people can change their preferences at any time.

## watchOS

Notification settings from iPhone apps apply by default to the same apps on Apple Watch. People can manage settings in the Apple Watch app on iPhone, or swipe left on a watch notification for per-notification options (Mute 1 Hour, Turn off Time Sensitive).