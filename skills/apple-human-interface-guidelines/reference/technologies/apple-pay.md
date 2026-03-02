# Apple Pay Design Guidelines

Guidelines for integrating Apple Pay as a payment option in apps (iOS, iPadOS, macOS, watchOS, visionOS) and websites.

## Offering Apple Pay

- **Offer Apple Pay on all devices and browsers that support it.** Use Apple Pay APIs to evaluate device support. Don't present it where unsupported.
- **If using APIs to detect an active card in Wallet, make Apple Pay the primary (but not sole) payment option** everywhere those APIs are used (e.g., pre-select it).
- **Feature Apple Pay at least as prominently as other payment options** on every page/screen that offers payment methods.
- **Use the Apple-provided API to display Apple Pay buttons** — never create custom button designs. API buttons are correctly styled and auto-localized.
- **If using a custom button to start payment, it must NOT display "Apple Pay" or the Apple Pay logo.** Instead, show the Apple Pay mark or reference Apple Pay in text on the same page.
- **Use Apple Pay buttons only to start payment or (when appropriate) the set-up process.** Don't repurpose them.
- **Don't hide or disable an Apple Pay button.** If prerequisites aren't met (e.g., no size selected), show the error after tap/click.
- **Use the Apple Pay mark only to communicate acceptance**, never as a payment button.
- **Inform search engines** that Apple Pay is accepted using semantic markup.

## Streamlining Checkout

- **Provide a cohesive checkout experience** — use your branding throughout; avoid opening new windows (especially on web).
- **If Apple Pay is available, assume the person wants to use it.** Display Apple Pay as the first/most prominent option.
- **Accelerate single-item purchases** with Apple Pay buttons on product detail pages (individual item only, exclude cart items).
- **Accelerate multi-item purchases** with express checkout that immediately shows the payment sheet.
- **Collect required info (color, size) before reaching the Apple Pay button.** Highlight missing fields with warning text.
- **Collect optional info (gift messages, delivery instructions) before or after checkout** — not on the payment sheet.
- **Gather multiple shipping methods/destinations before the payment sheet** (it only supports one method/destination per order).
- **For in-store pickup**, let people choose a location before displaying the payment sheet; show address as read-only.
- **Prefer information from Apple Pay** over stored info — assume it's current and complete.
- **Avoid requiring account creation before purchase.** Ask on the order confirmation page; prepopulate fields from the payment sheet.
- **Report transaction results** so people can see them in the payment sheet, including error details.
- **Display an order confirmation page** with shipping info and status tracking. If mentioning Apple Pay, format as "1234 (Apple Pay)" or "Paid with Apple Pay."

### Customizing the Payment Sheet

- **Only present and request essential information.** Don't show shipping address for electronically-delivered items.
- **Display active coupon/promo codes or allow entry on the sheet** (especially useful for express checkout).
- **Show shipping methods with description, cost, and optionally estimated delivery dates.** Use `PKDateComponentsRange` for accurate dates.
- **For in-store pickup**, let people choose a pickup window via shipping method date/time ranges.
- **Use line items for charges, discounts, pending costs, donations, recurring/future payments.** Don't itemize individual products.
- **Keep line items short** — fit on a single line when possible.
- **Use business name after "Pay" in the total line** — match the name on bank/credit card statements.
- **If acting as intermediary**, name both businesses: "Pay [End_Merchant (via Your_Business)]".
- **Disclose additional post-authorization costs** clearly, using "Amount Pending" when appropriate.

### Website Icon

For websites supporting Apple Pay, provide an icon for the payment sheet summary view:

| @2x | @3x |
| --- | --- |
| 120×120 px | 180×180 px |

## Handling Errors

### Data Validation

- Validate data when the payment sheet appears, when field values change, and after authentication.
- System error messaging highlights problematic fields; provide **custom error messages for the detail view**.
- **Privacy note:** Before authorization, only card type and redacted shipping address are accessible.
- **Avoid forcing strict business logic** — ignore irrelevant data, infer missing data (e.g., accept Zip+4 when only 5 digits needed; accept phone numbers in any format).
- **Provide accurate status codes** with custom error messages (`PKPaymentError` for iOS/watchOS, Apple Pay Status Codes for web).
- **Error messages should be specific:** "Zip code doesn't match city" not "Address is invalid." Use noun phrases, sentence-style capitalization, no ending punctuation. Keep ≤128 characters.

### Payment Processing

- **Handle interruptions (cancellation, timeout)** — cancel in-progress payment when the sheet dismisses. People can restart via the Apple Pay button.

## Supporting Subscriptions

- Recurring fees can be fixed or variable (where regulations allow).
- **Clarify subscription details before the payment sheet** — billing frequency, terms of service.
- **Include line items for billing frequency, discounts, and upfront fees.** If no payment at authorization, disclose when billing occurs.
- **Show current payment amount in the total line** at time of authorization.
- **Only show the payment sheet for subscription changes that increase cost.**

### Supporting Donations

For [approved nonprofits](https://developer.apple.com/support/apple-pay-nonprofits/):

- **Use a line item to denote a donation** (e.g., "Donation $50.00").
- **Offer predefined donation amounts** ($25, $50, $100) plus an "Other Amount" option.

## Apple Pay Button Types

Use Apple-provided APIs — never create custom button designs. API buttons are correctly styled, proportioned, localized, and VoiceOver-accessible.

| Button Type | Use Case |
| --- | --- |
| Buy with Apple Pay | Product detail/shopping cart pages |
| Pay with Apple Pay | Bills/invoices (utility, services) |
| Check out with Apple Pay | Cart with other "Check out" buttons |
| Continue with Apple Pay | Cart with other "Continue with" buttons |
| Book with Apple Pay | Booking flights, trips, experiences |
| Donate with Apple Pay | Approved nonprofit donations |
| Subscribe with Apple Pay | Subscriptions (gym, meal kit) |
| Reload with Apple Pay | Adding money using term "reload" |
| Add Money with Apple Pay | Adding money using term "add money" |
| Top Up with Apple Pay | Adding money using term "top up" |
| Order with Apple Pay | Placing orders (meals, flowers) |
| Rent with Apple Pay | Renting items (cars, scooters) |
| Support with Apple Pay | Giving money using term "support" |
| Contribute with Apple Pay | Giving money using term "contribute" |
| Tip with Apple Pay | Tipping for goods/services |
| Apple Pay (plain) | Smaller minimum width; no specific call to action; fallback for unsupported types |
| Set up Apple Pay | When device supports but hasn't set up Apple Pay; on Settings/profile/interstitial pages |

## Button Styles

- **Automatic:** Let system appearance determine style (`PKPaymentButtonStyle.automatic`).
- **Black:** Use on white/light backgrounds with sufficient contrast.
- **White with outline:** Use on white/light backgrounds without sufficient contrast.
- **White:** Use on dark backgrounds with sufficient contrast.

## Button Size and Position

- **Make Apple Pay button no smaller than other payment buttons.** Don't make people scroll to see it.
- **Side-by-side layout:** Apple Pay button to the **right** of Add to Cart.
- **Stacked layout:** Apple Pay button **above** Add to Cart.
- **Corner radius** can be adjusted to match other buttons (square, default rounded, or capsule) via `cornerRadius`.

### Minimum Dimensions

| Button | Min Width | Min Height | Min Margins |
| --- | --- | --- | --- |
| Apple Pay (plain) | 100pt | 30pt | 1/10 button height |
| All other types (Buy, Check out, Donate, etc.) | 140pt | 30pt | 1/10 button height |

If the specified size can't fit the translated title, the system auto-replaces with the plain Apple Pay button (no replacement for Set up Apple Pay).

## Apple Pay Mark

Use the mark graphic to show Apple Pay as an available payment option alongside other payment brand logos. It is **not a button**.

- Use only Apple-provided artwork; only adjust height (must be ≥ other payment marks).
- Don't adjust width, corner radius, aspect ratio, or add trademark symbols, visual effects, rotation, or animation.
- Maintain minimum clear space of **1/10 mark height**.
- Download from [Apple Pay Marketing](https://developer.apple.com/apple-pay/marketing/).

## Referring to Apple Pay in Text

| Rule | Detail |
| --- | --- |
| Capitalization | "Apple Pay" — uppercase A, uppercase P, lowercase rest |
| All-caps | Only when conforming to an established all-caps typographic style |
| Trademark | Use ® first time in body text (US); omit in checkout selection context |
| Translation | Never translate "Apple Pay" — always English |
| Apple logo | Never use  to represent "Apple" in text |
| Font | Match your app's typography; don't mimic Apple typography |
| Text-only descriptions | Only when ALL payment options are text-only; otherwise use Apple Pay mark |

**Correct:** "Purchase with Apple Pay" or "Purchase with Apple Pay®"
**Incorrect:** "Purchase with ApplePay", "Purchase with  Pay", "Purchase with APPLE PAY"

## Platform Support

Supported: iOS, iPadOS, macOS, visionOS, watchOS, web browsers. **Not supported on tvOS.**