# Siri Integration Guidelines

Design guidelines for integrating apps with Siri via SiriKit, including system intents, custom intents, shortcuts, suggestions, voice experiences, and editorial rules.

## Integrating Your App with Siri

SiriKit uses **intents** to represent tasks an app supports. Communication between your app and Siri is based on these intents.

- **System intents**: Common tasks (messaging, calling, workouts) grouped into domains
- **Custom intents**: For tasks not covered by system intents (ordering meals, grocery shopping)

### Intent Processing Phases

1. **Resolve**: Agree on what the request means. Ask for required parameters, clarify ambiguity (e.g., "Which Amy?")
2. **Confirm**: Verify the person wants to complete the task. Present errors if something prevents completion (e.g., pickup location closed). Required for financial-impact tasks.
3. **Handle**: Perform the task, provide visual and textual results (e.g., show a receipt)

### Providing Information & Supporting Suggestions

- Share information about frequent actions so Siri can suggest shortcuts at the right time
- Tell Siri about actions people haven't performed yet but might want to
- Siri uses signals like location, time of day, and motion type to predict when to suggest actions
- Suggestions appear on lock screen, in search results, or on the Siri watch face

## System Intents

| Domain | Intents |
| --- | --- |
| VoIP Calling | Initiate calls |
| Workouts | Start, pause, resume, end, cancel workouts |
| Lists and Notes | Create notes; search notes; create reminders |
| Media | Search/play media; like/dislike items; add to library/playlist |
| Messaging | Send, search, read messages |
| Payments | Send/request payments |
| Car Commands | Hazard lights, horn, lock/unlock doors, check fuel/power |

### Design Responses to System Intents

- **Complete requests without leaving Siri.** If the app must open, go directly to the expected destination — no intermediary screens.
- **Default to the safest, least expensive option** for financial-impact requests. Never misrepresent pricing or add hidden fees.
- **Provide alternative results** for ambiguous media playback requests.
- **On Apple Watch**, design streamlined workflows with minimal interaction. Use intelligent defaults; offer a small number of relevant choices.

### Enhance Voice Experience for System Intents

- **Create example requests** for the Help button in the Siri interface
- **Define custom vocabulary** — specific, nongeneric terms people use with your app (account names, workout names, etc.). Never include other app names, inappropriate language, or reserved phrases like "Hey Siri"
- **Define alternative app names** if people might refer to your app differently (e.g., "Unicorn" for UnicornChat). Never use other apps' names.

### Custom Interface for System Intents

- Avoid extraneous or redundant information; don't duplicate system-displayed info
- Ensure the action works without viewing the custom interface (voice-only fallback)
- Use **ample margins and padding** — generally 20pt from each edge
- Align content with the app icon displayed above your interface
- **Height**: No taller than half the screen height
- Don't display your app name or icon (system shows this automatically)
- watchOS apps cannot provide custom Siri UI

## Custom Intents

### Custom Intent Categories and Verbs

| Category | Default verb | Additional verbs |
| --- | --- | --- |
| Generic | Do | Run, go |
| Information | View | Open |
| Order | Order | Book, buy |
| Start | Start | Navigate |
| Share | Share | Post, send |
| Create | Create | Add |
| Search | Search | Find, filter |
| Download | Download | Get |
| Other | Set | Request, toggle, check in |

### Response Types

- **Confirmation**: Confirms people want to perform the action
- **Success**: Indicates action initiated
- **Error**: Action can't be completed

Customize responses with templates combining your dialogue with placeholders for app-supplied data. Confirmation responses show default dialogue *after* custom dialogue.

### Designing Custom Intents

- Use a system intent if one matches your action's purpose
- **Pick the category that most closely matches the action** — affects dialogue and controls
- Use the **information category** for actions that retrieve/display information (avoids extra taps)
- Design intents that **accelerate common, useful tasks**
- Ensure intents **work in every scenario** — voice with/without screen, lock screen, Siri watch face, search, multistep shortcuts
- Design for **tasks that aren't overly complex** — reduce required actions, avoid lengthy conversations
- Design **long-lived intents** — avoid date-specific or temporary-data intents
- **Don't request Siri permission** for custom-intent-only apps
- **Support background operation** — run quickly without bringing app to front

### Follow-Up Questions & Parameters

- **Minimize follow-up questions** — one or two at most
- **List the smallest number of options possible**; sort meaningfully (recency, frequency, popularity)
- **Each question should be meaningful** — avoid overly granular or similar options
- **Design simple, understandable parameters** with straightforward names
- **Ask for confirmation only when necessary** — required for financial impact; avoid asking more than once
- **Prioritize options based on context** (e.g., nearby locations for pickup)
- Consider **dynamic parameter options** during shortcut setup — contextually relevant lists or comprehensive lists

### Voice Experience for Custom Intents

- **Create conversational interactions** — write scripts and act them out to test naturalness
- **Provide specific error descriptions** (e.g., "Sorry, we're out of chicken noodle soup" instead of generic errors)
- **Voice responses must convey the same info as visual elements** for voice-only scenarios (HomePod, AirPods, CarPlay)
- **Keep responses concise and descriptive** — customize default dialogue for clarity ("Which soup?" > "Which one?")
- **Avoid repetition** — people run shortcuts frequently; minimize unnecessary words and humor
- **Provide app-specific synonyms** (e.g., "bowl" = "large") and alternative spoken dialogue
- **Exclude your app name** from responses — system handles attribution
- **Never impersonate Siri** or reproduce Siri functionality
- **Respect parental controls**; avoid offensive content
- **Avoid personal pronouns** — be inclusive
- **Consider offering "See more in App Name"** for incomplete option lists
- **Keep responses device-independent**
- **Don't advertise** in intent content

## Shortcuts and Suggestions

### Making Actions Available (Donations)

- **Donate every time** people perform the action — helps predict best suggestion timing
- **Only donate actions people actually perform** — not browsing or unrelated actions
- **Remove donations** when required data no longer exists (e.g., deleted contact)
- **Donate reservations** (ticketed events, travel, restaurants) for Calendar/Maps suggestions

### Shortcut Titles and Subtitles

- **Be concise but descriptive** — title conveys what happens when shortcut runs
- **Start titles with a verb**, use sentence-style capitalization, no punctuation
- Lead with important information (truncation varies by device)
- Exclude app name
- Localize titles and subtitles

| ✅ | ❌ |
| --- | --- |
| *Order my favorite coffee* | *Large latte* |
| *Show today's forecast* | *Weather forecast* |

### Custom Images for Suggestions

- iOS: 60×60 pt (180×180 px @3x)
- Siri watch face (44mm): 34×34 pt (68×68 px @2x); watchOS scales down for smaller watches

### Default Phrases for Shortcuts

- Keep phrases **short and memorable** — 2-3 words work best
- Make phrases **accurate and specific** (*Watch baseball* > *Watch sports*)
- Don't imply variable invocation (*Order a large clam chowder* suggests substitutions work)
- Never commandeer core Siri commands (e.g., *Call 911*) or include *Hey Siri*

### Making Shortcuts Customizable

- **Provide a parameter summary** for each custom intent — a sentence beginning with a verb using editable parameters (e.g., "Order *quantity* *coffee*")
- Include all required parameters and those receiving values from other apps
- Summary should be **clearly related to intent title** — use the same verb
- Use **sentence-style capitalization**, no ending punctuation; minimize internal punctuation
- Provide **multiple summaries** for parent-child parameter relationships
- Provide **output parameters** for multistep shortcut use
- Consider defining an **input parameter** for automatic chaining from preceding actions
- Use a **key parameter** with an image to help distinguish action variations
- **Avoid multiple actions for the same basic task** — combine into one flexible action

## Editorial Guidelines

### Referring to Siri

- Don't use pronouns (she/him/her) for Siri — use "Siri"
- **Hey Siri**: Two words, italicized or quoted, uppercase H and S, no ellipsis

| ✅ | ❌ |
| --- | --- |
| *Say Hey Siri to activate Siri.* | *Say Hey Siri… to activate Siri.* |
| *Say "Hey Siri" to activate Siri.* | *Say "hey Siri" to activate Siri.* |

### Hey Siri Localization

Only translate "Hey" — *Siri* is never translated.

| Locale | Translation | Locale | Translation |
| --- | --- | --- | --- |
| ar_AE/ar_SA | يا Siri | fr_CA/fr_CH/fr_FR/fr_BE | Dis Siri |
| da_DK | Hej Siri | it_CH/it_IT | Ehi Siri |
| de_AT/de_CH/de_DE | Hey Siri | ja_JP | Hey Siri |
| en_* | Hey Siri | ko_KR | Siri야 |
| es_CL/es_ES/es_MX/es_US | Oye Siri | ms_MY | Hai Siri |
| fi_FI | Hei Siri | nb_NO/no_NO | Hei Siri |
| nl_BE | Hé, Siri | nl_NL | Hé Siri |
| pt_BR | E aí Siri | ru_RU | привет Siri |
| sv_SE | Hej Siri | th_TH | หวัดดี Siri |
| tr_TR | Hey Siri | zh_CN | 嘿Siri |
| zh_HK | 喂 Siri | zh_TW | 嘿 Siri |

### Referring to Shortcuts

- **Shortcuts** (feature/app): Always capitalized, always plural
- **shortcuts** (individual): Lowercase
- Use phrases like *Run a shortcut by asking Siri* — avoid "voice shortcuts," "voice command," "voice prompt"
- For non-voice encouragement: *For quick access, add to Shortcuts*
- Translate app name and "Shortcuts" but never "Siri" in localized contexts

### Referring to Apple Products

- Use Apple product names exactly as on the Apple Trademark List, in singular form only
- Don't make Apple product names possessive
- Don't translate Apple, Siri, or any Apple trademark
- Don't use category descriptors (say "iPad" not "tablet")
- Don't imply Apple sponsorship or endorsement
- Attribute trademarks with correct credit lines in legal sections