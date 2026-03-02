# Wallet Design Guidelines

Guidelines for designing Apple Wallet passes, order tracking, identity verification, and related experiences on iPhone and Apple Watch.

## Passes

- **Offer to add new passes to Wallet** when people complete relevant actions (checking into a flight, purchasing tickets, etc.). Use system-provided UI for one-tap adding (`PKPassLibrary/addPasses`) or a custom view with Add to Apple Wallet button (`PKAddPassesViewController`).
- **Help people add passes created outside your app** (e.g., from website). Suggest once; if declined, don't ask again.
- **Add related passes as a group** (e.g., multi-connection boarding passes, event ticket sets). Bundle for single download.
- **Display Add to Apple Wallet button** (`PKAddPassButton`) to let people re-add previously declined or removed passes.
- **Let people jump to their pass in Wallet** with a "View in Wallet" link wherever pass info appears in your app.
- **Tell the system when passes expire** — set expiration date, relevant date, and voided properties correctly so Wallet auto-hides expired passes.
- **Always get permission before deleting a pass** — consider an in-app setting for manual vs. automatic removal.
- **Help the system suggest passes contextually** by supplying when/where info so passes appear on Lock Screen when relevant. iOS 18+/watchOS 11+: system starts Live Activity for poster event ticket passes when relevant.
- **Update passes as needed** to reflect changes (delays, gate changes, etc.).
- **Use change messages only for time-critical updates** (e.g., gate changes). Never for marketing. Available per-field.

## Designing Passes

Design clean, simple passes that look at home in Wallet rather than replicating physical items.

- **Design for all devices** — don't put essential info in elements unavailable on certain devices. Don't add padding to images (watchOS crops white space).
- **Avoid device-specific language** — don't write "slide to view" as it doesn't work on Apple Watch.
- **Make passes instantly identifiable** using brand color. Ensure content is readable against background.
- **Keep front uncluttered** — show essential info (event date, balance) in top-right area (visible when collapsed). Put extras on back (iOS) or details screen (watchOS).
- **Prefer NFC-compatible passes** — barcodes/QR codes appear on back (iOS) or details (watchOS) when NFC is primary.
- **Reduce image sizes** for fast email/webpage downloads.
- **Provide a brand/company icon** for Lock Screen notifications and Mail.
- **Display text only in pass fields** — don't embed text in images (not accessible, not shown on all devices). Avoid custom fonts that hinder readability.

### Pass Layout Areas

All styles use these basic areas:
1. **Top row**: Logo image, logo text, essential/header area
2. **Primary area**: Important information
3. **Secondary and auxiliary area**: Supplemental information
4. **Bottom**: Codes area and optional footer

| Field | Layout Area | Purpose |
|---|---|---|
| Header | Essential | Critical info visible when pass is collapsed |
| Primary | Primary | Important info for using the pass |
| Secondary/Auxiliary | Secondary/Auxiliary | Useful but not always needed info |
| Back | Back of pass | Supplemental details |

General limits: up to 3 header fields, 1 primary field, up to 4 secondary fields, up to 4 auxiliary fields.

### Pass Styles

#### Boarding Passes
For transit (trains, airlines, etc.). Each pass = single trip with start/end point.
- Images: logo, footer
- Fields: up to 2 primary, up to 5 auxiliary

#### Coupons
For coupons, special offers, discounts.
- Images: logo, strip
- Fields: up to 4 secondary/auxiliary on one row

#### Store Cards
For loyalty cards, discount cards, points cards, gift cards. Usually shows current balance.
- Images: logo, strip
- Fields: up to 4 secondary/auxiliary on one row

#### Event Tickets
For concerts, movies, plays, sporting events. Single event or season ticket.
- Images: logo, strip OR background OR thumbnail (strip excludes background/thumbnail)
- Can include extra row of up to 4 auxiliary fields (`row` property)

##### Poster Event Tickets (iOS 18+)
Contactless-only event tickets with rich visual experience. **Not compatible with QR/barcode entry.**
- Displays event logo, background image, optional secondary/issuer logo
- Uses `SemanticTags` metadata (required sets vary by event type: general, sports, live performance)
- System generates Maps shortcut and event guide below ticket
- Event guide: 1–4 quick action buttons (>4 collapses to menu), weather, venue map

**Poster event ticket design guidance:**
- Create vibrant, identifiable background with minimal text
- Position artwork in safe area (header/footer overlap background)
- Ensure sufficient contrast — system applies gradient (header) and blur (footer) by default; adjust if needed
- Use `useAutomaticColors` for system-determined text colors, or customize with sufficient contrast
- Use additional information tile for extra non-essential event details
- **Continue supporting standard event tickets for earlier iOS versions** — provide primary/secondary/auxiliary fields and image assets in `PassFields`

#### Generic Passes
For passes that don't fit other categories (gym cards, coat-check tickets).
- Images: logo, thumbnail
- Fields: up to 4 secondary/auxiliary on one row

### Passes for Apple Watch

Wallet shows passes in a scrolling carousel. People can add passes without a watch-specific app.

Basic watch layout:
1. Logo image + essential field
2. Primary field
3. Secondary/auxiliary fields

Overflow info goes to scrolling details screen. **watchOS crops strip images to card aspect ratio and may crop white space from other images.**

## Order Tracking

Wallet displays order info (active/completed), updating on status changes. Uses [Wallet Orders](/documentation/WalletOrders) schema.

- **Make it easy to add orders to Wallet** — use `PKPaymentOrderDetails` (app) or `ApplePayPaymentOrderDetails` (web) after Apple Pay transactions. iOS 17+: use `AddOrderToWalletButton` for Track with Apple Wallet button.
- **Make order info available immediately** after placement, even if details are pending.
- **Provide fulfillment info ASAP and keep status updated** — system auto-sends notifications on changes. Statuses: Order Placed, Processing, Ready for Pickup, Picked Up, Out for Delivery, Delivered, Issue, Canceled.
- **Logo image**: 300×300px PNG/JPEG, nontransparent background.
- **Product images**: 300×300px PNG/JPEG, nontransparent background, straightforward depiction, solid background.
- **Keep text brief** — system truncates long text.
- **Localize text** and ensure price matches confirmed final price.

### Order & Fulfillment Details

- Provide a universal link to order management area.
- Clearly describe each item using `LineItem` (price, name, image). Attach PDF receipts when appropriate.
- Supply prioritized list of your apps for system links.
- Avoid duplicate notifications (suppress Wallet notifications when associated app is installed).
- Provide multiple contact methods: website, Messages for Business, phone, email, support page.
- For shipping: provide carrier name, tracking link (direct), use specific status values (`onTheWay`, `outForDelivery`, `delivered`) when you have carrier details, or `shipped` if not.
- For pickup: include scannable barcode when required.
- Provide clear instructions for receiving/picking up orders.
- Keep fulfillment screen focused on order tracking (don't prioritize app promotion).
- Write approachable, accurate status descriptions. Be direct about Issue/Canceled statuses.

## Identity Verification

iOS 16+. Apps/App Clips can verify identity from Wallet-stored ID cards.

- **Present Verify with Wallet only when device supports it** — provide fallback verification. Use `VerifyIdentityWithWalletButton`.
- **Ask for identity info only at the precise moment needed** — during the process/transaction requiring it, not during account creation.
- **Write clear purpose strings** explaining why info is needed. Use sentence case, direct language, include period.
- **Ask only for data you need** — e.g., use age threshold check (`age(atLeast:)`) instead of requesting birth date.
- **Specify data retention** using `PKIdentityIntentToStore` — system displays explanatory content.

### Verification Button Types

| Button | Use When |
|---|---|
| Verify Age with Apple Wallet | Transaction completable after age verification (e.g., leasing) |
| Verify Identity with Apple Wallet | Transaction completable after identity verification (e.g., car rental) |
| Continue with Apple Wallet | Verify with Wallet is part of a multi-step process requiring additional info |
| Verify with Apple Wallet | Verification completable without additional steps, but other labels don't fit |

All buttons: white text on black background. Optional light outline style for dark backgrounds (`blackOutline`). Adjust `cornerRadius` to match UI. Multiline variants auto-applied when space is constrained.

## Pass Image Specifications

Create PNG files at these dimensions (in points):

| Image | Supported Pass Styles | Filename | Dimensions (pt) |
|---|---|---|---|
| Logo | Boarding pass, coupon, store card, event ticket, generic | `logo.png` | Up to 160×50 |
| Primary logo | Poster event ticket | `primaryLogo.png` | Up to 126×30 |
| Secondary logo | Poster event ticket | `secondaryLogo.png` | Up to 135×12 |
| Icon | All | `icon.png` | 38×38 |
| Background | Event ticket | `background.png` | 180×220 |
| Background | Poster event ticket | `artwork.png` | 358×448 |
| Strip | Coupon, store card | `strip.png` | 375×144 |
| Strip | Event ticket | `strip.png` | 375×98 |
| Footer | Boarding pass | `footer.png` | Up to 286×15 |
| Thumbnail | Event ticket, generic pass | `thumbnail.png` | 90×90 |

**Note:** Logo, primary logo, and secondary logo dimensions are maximums, not required. Don't add unnecessary padding.