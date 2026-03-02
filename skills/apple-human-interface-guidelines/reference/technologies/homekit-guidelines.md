# HomeKit Design Guidelines

Guidelines for integrating with HomeKit in iOS, tvOS, and watchOS apps, covering terminology, setup, Siri interactions, custom functionality, icon usage, and branding.

## Terminology and Layout

HomeKit models the home as a hierarchy. Your app must use the correct terminology and object model to reinforce people's understanding.

### Object Hierarchy

| Term | Definition |
|------|------------|
| **Home** | Physical home, office, or location. One person can have multiple homes. Root of the hierarchy. |
| **Room** | Named physical room (e.g., *Bedroom*, *Office*). No size/location attributes. |
| **Zone** | Area containing multiple rooms (e.g., *upstairs*, *downstairs*). Optional but enables multi-room voice commands. |
| **Accessory** | Physical connected device (fan, lamp, lock, camera). Has a **category** (thermostat, fan, light). |
| **Service** | Controllable feature of an accessory (e.g., switch on a light). Don't use the word "service" in UI — use descriptive names like *garage door opener*. People speak the service name to Siri, not the accessory name. |
| **Characteristic** | Controllable attribute of a service (e.g., *speed*, *brightness*). Don't use the word "characteristic" in UI. |
| **Service group** | Group of services controlled as a unit (e.g., *reading lamps* for three lamps in one corner). |
| **Action** | Changing a service's characteristic (e.g., adjusting brightness). |
| **Scene** | Group of actions controlling one or more services/accessories (e.g., *Movie Time* dims lights + lowers shades). API uses "action set" — always use "scene" in UI. |
| **Automation** | Accessories reacting to triggers: location change, time, another accessory, or sensor detection. |

### Key Principles

- **Acknowledge the hierarchical model** — reference rooms/zones so people can use voice commands like "turn on the lights upstairs"
- **Make HomeKit details easily accessible** — don't hide zone/room info in buried settings screens
- **Support multiple homes** — show relevant home info in accessory detail views
- **Don't present duplicate home settings** — defer to settings made in the Home app; never ask people to re-setup their homes

## Setup

- **Use the system-provided setup flow** via `HMAccessorySetupManager.performAccessorySetup(using:completionHandler:)` for naming, pairing, room assignment, and favorites
- **Provide a purpose string** explaining Home data access, e.g., "Lets you control this accessory with the Apple Home app and Siri across your Apple devices."
- **Don't require account creation** — defer to HomeKit for info; make account setup optional and offer it after initial HomeKit setup
- **Honor setup choices** — don't force other platforms during HomeKit setup
- **Custom setup comes after** — present system flow first, then offer custom post-setup for unique accessory features

### Naming Rules

Service names must follow these rules (system flow checks original names; your app must check renames):

- Use only alphanumeric, space, and apostrophe characters
- Start and end with alphabetic or numeric character
- No emojis

| Status | Example |
|--------|---------|
| ✅ | Reading lamp |
| ❌ | 📚 lamp |
| ✅ | 2nd garage door |
| ❌ | #2 garage door |

- **Suggest good service names** — never suggest company names or model numbers
- **Prevent location info in names** — "kitchen light" in the kitchen causes unpredictable voice results. Detect duplicated room/zone names and suggest people assign the accessory to that room/zone instead

## Siri Interactions

- **Show example voice commands** using the chosen service name right after setup
- **Teach complex commands** in context throughout your app (e.g., in scene detail: *You can say "Hey Siri, set 'Movie Time.'"*)
- **Recommend zones and service groups** when they make sense (e.g., "upstairs" zone, "media center" service group)
- **Offer shortcuts only for non-HomeKit functionality** — don't duplicate what HomeKit voice control already supports
- **Clarify shortcuts vs. HomeKit** if your app supports both

### Example Siri Phrases

| Phrase | Siri Understands |
|--------|------------------|
| "Turn on the floor lamp" | Service name |
| "Show me the entryway camera" | Service name |
| "Turn on the light" | Accessory category |
| "Turn off the living room light" | Room + category |
| "Make the living room a little bit brighter" | Room + implied category + brightness characteristic |
| "Turn on the recessed lights" | Service group |
| "Turn off the lights upstairs" | Category + zone |
| "Run Good night" | Scene |
| "Is someone in the living room?" | Implied category + occupancy characteristic |
| "Did I leave the garage door open?" | Category + open characteristic |
| "It's dark in here" | Current home + current room (via HomePod) + implied category |

## Custom Functionality

- **Clarify your app vs. Home app** — guide people to add other accessories to scenes via the Home app
- **Defer to HomeKit database** — automatically reflect changes from Home app; never overwrite without explicit direction
- **Ask permission** before writing to the HomeKit database
- **Show conflicts visually** (e.g., side-by-side name comparison) when databases differ

### Cameras

- **Don't block camera images** — supplementary features (alerts) are fine, but don't cover camera content
- **Show microphone button only if bidirectional audio is supported**

## Icon Usage

Use the HomeKit icon only in setup or instructional communications.

### Styles

| Style | When to Use |
|-------|-------------|
| Black icon | White/light backgrounds, when other tech icons are black |
| White icon | Black/dark backgrounds, when other tech icons are white |
| Custom color | When other tech icons use the same color |

### Icon Rules

- **Use only Apple-provided icons** — download from [Apple Design Resources](https://developer.apple.com/design/resources/)
- **Position consistently** with other technology icons; if others are in shapes, put HomeKit icon in a shape too
- **Use noninteractively** — don't use in buttons or custom interactive elements
- **Don't use within text** or as a replacement for the word "HomeKit"
- **Pair correctly with name** — show name below or beside icon, using same font as layout

## Referring to HomeKit (Branding & Trademark)

- **Emphasize your app over HomeKit** — references to HomeKit/Apple Home should be less prominent than your brand
- **Capitalize correctly**: *HomeKit* (one word, uppercase H and K); *Apple Home* (two words, uppercase A and H)

### Usage Rules

| Rule | ✅ Correct | ❌ Incorrect |
|------|-----------|-------------|
| Use as descriptor | "[Brand] lightbulbs work with HomeKit" / "HomeKit-enabled thermostat" | "HomeKit lightbulbs" |
| Don't personify | "Back door is unlocked with HomeKit" | "HomeKit unlocked the back door" |
| Apple prefix optional | "Compatible with Apple HomeKit" | — |
| App name | "Open the Apple Home app" (first mention), then "the Home app" | "Open Home" |
| Device references | "Use HomeKit to turn on your lights from your iPhone or iPad" | "...from your iOS devices" |

### Trademark Requirements

- Don't use Apple trademarks in app names or images
- Use Apple product names in singular form; don't make them possessive
- Don't translate Apple, Apple Home, HomeKit, or other Apple trademarks
- Don't use category descriptors (say "iPad" not "tablet")
- Don't indicate sponsorship/partnership/endorsement from Apple
- Include correct trademark credit lines in legal sections of your app