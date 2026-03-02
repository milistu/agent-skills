# Tap to Pay on iPhone - HIG Guidelines

Design guidelines for integrating Tap to Pay on iPhone into iOS payment apps, covering enabling, merchant education, checkout flows, result display, and additional interactions.

## Enabling Tap to Pay on iPhone

Merchants must accept terms and conditions before initial device configuration.

- **Present T&C before customer-facing flows** — let merchants accept during onboarding or in-app messaging, not during checkout.
- **Present T&C only to administrative users** — if a non-admin tries to activate, explain that admin access is required. Admins can accept via web interface or different app (even non-iPhone devices).
- **Ensure device is up to date** — if your PSP requires specific iOS versions, present T&C only after the merchant updates.

## Educating Merchants

Provide a tutorial covering supported payment types and how to accept each. Offer it via:
- Learn More option in in-app messaging
- Auto-present after T&C acceptance
- Auto-present to new users
- Persistent location (help content or settings)

Use Apple-approved assets from [Tap to Pay marketing guidelines](https://developer.apple.com/tap-to-pay/marketing-guidelines/) or the `ProximityReaderDiscovery` API for a pre-built, localized merchant education experience.

Custom tutorials should show how to:
- Launch checkout for each payment type
- Help customers position contactless card/digital wallet on the device
- Handle PIN entry, including accessibility mode

Offer T&C acceptance at the end of the tutorial for merchants who haven't accepted yet.

## Checkout Flow

### Availability
- **Show Tap to Pay on iPhone as a checkout option whether enabled or not** — let merchants enable it inline without leaving checkout.
- **Always make the option selectable even during configuration** — show a progress indicator while configuring rather than hiding the option.

### Performance
- **Minimize wait times** — call `prepare(using:)` as soon as the app starts and after each foreground transition.
- **During configuration**, show an indeterminate progress indicator by default; show a determinate indicator if the ProximityReader API reports ongoing configuration progress via `PaymentCardReader.Event.updateProgress(_:)`.

### Multiple Payment Methods
- **Make Tap to Pay button easy to find** — don't require scrolling. If it's the only payment method, open it automatically at checkout.
- **Let merchants switch between Tap to Pay and hardware accessories** seamlessly during checkout without visiting settings.

### Button Labeling Rules

| Scenario | Label |
|---|---|
| Standard button | "Tap to Pay on iPhone" |
| Space-constrained | "Tap to Pay" |
| Only payment method | Reuse existing "Charge" or "Checkout" button |
| With icons (multiple methods) | Use `wave.3.right.circle` or `wave.3.right.circle.fill` SF Symbols |

**Never include the Apple logo in Tap to Pay buttons.**

- "Tap to Pay on iPhone" / "Tap to Pay" labels are **only for payment actions** (see Additional Interactions for non-payment).
- Style the button to match your app's other buttons (color, shape are flexible).

### Pre-Payment
- **Determine final amount before initiating the Tap to Pay screen** — handle tipping and other adjustments first.
- **Display pre-payment options** (e.g., payment type selection) after the merchant taps the button but before opening the Tap to Pay screen.

## Displaying Results

After a successful tap, the system shows a checkmark and returns encrypted payment data. After failure, an error screen appears.

### Success Flow
- **Start processing immediately** — use `returnReadResultImmediately` to get results before the checkmark animation finishes.
- **Show an authorization progress indicator** after the Tap to Pay screen animation finishes (use `PaymentCardReader.Event.readyForTap` to time this).
- **Clearly display transaction result** (approved or declined) with the reason if possible.
- **Offer digital receipt options** — QR code, text message, etc.

### Failure Handling
When payment fails (unreadable card, unsupported network, amount limit, no online PIN):
- Let merchants accept alternate payment (cash, external hardware, payment link)
- Allow relaunching Tap to Pay for a different card

### Special Scenarios
- **SCA (Strong Customer Authentication)** — in some regions, banks may request PIN after processing even if the card didn't require one during tap. App may need to display PIN entry instead of result.
- **Offline PIN markets** — some PSPs support PIN fallback to collect partial data and continue via another method.

### Error Handling
- Display clear error descriptions with recommended resolutions (e.g., suggest iOS update if version unsupported).
- Provide easy access to help content and support contact.

## Additional Interactions

### Non-Payment Card Reads
For reading cards without a transaction amount (lookups, storing cards, refunds, verification):
- **Use generic button labels** like "Look Up," "Store Card," "Verify," or "Refund"
- **Do NOT use** "Tap to Pay on iPhone" or "Tap to Pay" for these actions

### Loyalty Cards
For independent loyalty card transactions:
- Provide a **separate, clearly labeled button** (e.g., "Loyalty Card")
- **Do NOT include** "Tap to Pay on iPhone," "Tap to Pay," or payment-related terms in loyalty button labels

## Platform Support

iOS only. Not supported on iPadOS, macOS, tvOS, visionOS, or watchOS.