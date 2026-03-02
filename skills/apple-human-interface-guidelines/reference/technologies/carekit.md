# CareKit Design Guidelines

Design guidance for CareKit apps that manage care plans related to chronic illness, recovery, or health/wellness goals. CareKit 2.0 includes CareKit UI (prebuilt views) and CareKit Store (on-device database for patients, care plans, tasks, contacts).

## Data and Privacy

- **Provide a coherent privacy policy** — required during app submission; must be viewable from App Store listing.
- Receive permission before accessing data through iOS features; protect all data whether user-entered or device/system-sourced.

### HealthKit Integration

- **Request access to health data only when needed** — tie requests to current context (e.g., request weight access when logging weight, not at launch). People can change permissions, so request every time access is needed.
- **Add descriptive messages to the standard permission screen** — write succinct sentences explaining why data is needed and how sharing benefits the user. Don't replicate the permission screen with custom screens.
- **Manage health data sharing solely through system privacy settings** — don't build additional in-app screens affecting health data flow.

### Motion Data

With permission, apps can access motion data (standing, walking, running, cycling, driving, step count, pace, flights of stairs). Motion data can include custom physical therapy data collected via ResearchKit tasks.

### Photos

With permission, apps can access camera and photos for sharing treatment progress with a care team (e.g., periodic injury photos for physician monitoring).

### ResearchKit Integration

CareKit apps can incorporate ResearchKit features for surveys, tasks, charts, and informed consent modules for data collection/sharing permissions.

## CareKit Views

CareKit UI provides customizable views in three categories:

| Category | Purpose |
| --- | --- |
| Tasks | Present tasks (medication, physical therapy). Support logging symptoms and data. |
| Charts | Display graphical data showing treatment progress. |
| Contact views | Display contact info. Support phone, message, email, and map links. |

Each view has a **header** (text, symbol, disclosure indicator, optional separator) and an optional **content stack** (vertical arrangement of subviews). Layout constraints within views are managed automatically.

### Tasks

Task information:

| Information | Required | Description | Example |
| --- | --- | --- | --- |
| Title | Yes | Word or short phrase introducing the task | *Ibuprofen* |
| Schedule | Yes | When a task must be completed | *Four times a day* |
| Instructions | No | Detailed instructions, recommendations, warnings | *Take 1 tablet every 4–6 hours (max 4 daily)* |
| Group ID | No | Identifier for grouping similar tasks | *medication*, *exercise* |

#### Five Task View Styles

- **Simple** — One-step task. Header with title, subtitle, and completion button (checkmark by default). No content stack; use a different style if additional content is needed.
- **Instructions** — Simple task with added informative text (e.g., "Take on an empty stomach", "Take at bedtime").
- **Log** — For logging events (e.g., nausea occurrences). Displays a button to log and auto-generates timestamps.
- **Checklist** — List of actions/steps in a multistep task. Each item has text and a completion button. Can display instructional text below the list.
- **Grid** — Compact grid of buttons for multistep tasks. Supports succinct button titles. Provides access to underlying collection view for custom UI. Can display instructional text below grid.

#### Task Design Best Practices

- **Use color to reinforce meaning** (e.g., one color for medications, another for physical activities). Never use color as the only way to convey information.
- **Combine accuracy with simplicity** — use marketing names instead of chemical descriptions. Minimize redundant words when context clarifies meaning.
- **Supplement complex tasks with videos or images** to help avoid mistakes.

### Charts

Three chart styles: **bar**, **scatter**, and **line**. For each, provide title, subtitle, axis markers (e.g., days of the week), and data set. Charts update automatically with new data.

#### Chart Design Best Practices

- **Highlight narratives and trends** to illustrate progress (e.g., correlation between medication adherence and pain levels).
- **Label elements clearly and succinctly** — keep labels short, avoid repeating information (e.g., use *BPM* in axis label, not on every data point).
- **Use distinct colors** — avoid different shades of same color for different meanings. Ensure sufficient contrast.
- **Provide a legend** if colors aren't immediately clear.
- **Clearly denote units of time** — include in axis labels or elsewhere if not in data value labels.
- **Consolidate large data sets** for readability — group and organize data for clarity.
- **Offset data to keep charts proportional** when there's significant difference between data points.

### Contact Views

Two styles:

- **Simple** — Person glyph, name, practice type, disclosure button.
- **Detailed** — Header with glyph/name/practice, plus subview with info and buttons for calling, messaging, emailing, and navigating to address.

- **Use color to categorize care team members** for at-a-glance identification.

## Notifications

- **Minimize notifications** — care plans vary; use sparingly so people aren't overwhelmed. Coalesce multiple items into a single notification when possible.
- **Consider providing a detail view** — let people take immediate action (e.g., mark pending tasks complete) without opening the app.
- Apple Watch can also display notifications from the app.

## Symbols and Branding

CareKit uses built-in symbols (phone, messaging, envelope, clock). Most view styles work best with default symbols. The grid-style task view is highly customizable and can display custom UI.

- Use **SF Symbols** for custom items — they coordinate with CareKit's visual design language and support custom symbol creation.
- **Design relevant care symbols** — closely related to your app or health/wellness concept. Don't use decorative symbols or corporate logos.
- **Incorporate refined, unobtrusive branding** — subtly use color and communication style. Avoid advertising that distracts from the care plan.

## Platform Support

iOS and iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS.