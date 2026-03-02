# In-App Purchase Design Guidelines

Guidelines for designing in-app purchase experiences across Apple platforms, including subscriptions, offer codes, refunds, and Family Sharing.

## Content Types

- **Consumable**: Depletes with use (e.g., game lives/gems), can be repurchased
- **Non-consumable**: Permanent premium features, doesn't expire
- **Auto-renewable subscriptions**: Ongoing access, auto-renews until canceled
- **Non-renewing subscriptions**: Limited-time access (e.g., battle pass), must be manually repurchased

> **In-app purchase vs Apple Pay**: Use in-app purchase for virtual goods (premium content, subscriptions). Use Apple Pay for physical goods, services (hotel reservations, event tickets), and donations.

## Best Practices

- **Let people experience your app before purchasing.** People invest more after discovering value.
- **Design an integrated shopping experience.** Products and transactions should mirror your app's style — don't make it feel like a different app.
- **Use simple, succinct product names and descriptions.** Titles shouldn't truncate or wrap; use plain, direct language.
- **Display the total billing price** for every in-app purchase, regardless of type.
- **Hide the store when payments aren't available** (e.g., parental restrictions). Use `canMakePayments` to check.
- **Use the default confirmation sheet.** Don't modify or replicate the system purchase confirmation sheet.

## Family Sharing

People can share auto-renewable subscriptions and non-consumable purchases with up to 5 family members.

- **Prominently mention Family Sharing** where people learn about your content — include "Family" or "Shareable" in subscription names; reference it on sign-up screens.
- **Help people understand benefits and how to participate.** Existing subscribers receive Apple notifications about sharing; family members get notified about shared content.
- **Customize messaging for both purchasers and family members.** E.g., welcome family members with "Your family subscription includes…".

## Providing Help with Purchases

Present custom UI within your app for purchase assistance and the system-provided refund flow (`beginRefundRequest(for:in:)`).

- **Provide help before the refund request** — include missing purchase resolution, FAQ, feedback/contact options alongside the refund link.
- **Use simple refund action titles** like "Refund" or "Request a Refund." The system clarifies it's through Apple.
- **Help identify the problematic purchase** — show product image, name, description, and original purchase date.
- **Consider offering alternative solutions** (e.g., immediate fulfillment), but always make the refund option clear and accessible.
- **Don't create barriers to refund requests** — avoid requiring scrolling or extra screens to find the refund button.
- **Don't characterize Apple's refund policies** — don't speculate on outcomes. Link to Apple's support page if needed.

## Auto-Renewable Subscriptions

- **Call attention to subscription benefits during onboarding** with a strong call to action and clear terms summary.
- **Offer a range of content choices, service levels, and durations.**
- **Let people try content for free before signing up** via:
  - Freemium app (limited free features)
  - Metered paywall (limited free articles per month)
  - Free trial
- **Prompt to subscribe at relevant times** (e.g., nearing monthly free content limit). Include prompts throughout the app.
- **Only encourage new subscriptions when someone isn't already subscribed.** Provide sign-in for cross-app/website subscribers.

### Making Signup Effortless

- **Provide clear, distinguishable subscription options** with short names, price, and duration. For introductory pricing, show the intro price, offer duration, and standard price after.
- **Simplify initial signup** — ask only for necessary info; defer the rest.
- **On tvOS, help people sign up using another device** — send a code rather than requiring input on TV.
- **Sign-up screen must include:**
  - Subscription name, duration, and content/services provided
  - Billing amount, correctly localized for territories and currencies
  - Way for existing subscribers to sign in or restore purchases
  - Links to Terms of Service and Privacy Policy
- **Clearly describe how a free trial works** — explicitly state the trial duration and what's billed when it ends.
- **Include a sign-up opportunity in app settings.**

### Supporting Offer Codes (iOS/iPadOS)

Two types:
- **One-time use code**: Unique, generated in App Store Connect. Redeemable via URL, in-app, or App Store. Best for small/restricted distribution.
- **Custom code**: You create (e.g., NEWYEAR). Redeemable via URL or in-app only. Best for large campaigns.

Guidelines:
- **Clearly explain offer details** in marketing materials.
- **Custom codes**: Alphanumeric ASCII only, no special characters (no Chinese/Arabic).
- **Tell people how to redeem custom codes** — they can't enter them in App Store account settings.
- **Support in-app redemption** — add a "Redeem Code" button to your paywall, onboarding, or settings. Use `presentOfferCodeRedeemSheet(in:)` or `offerCodeRedemption(isPresented:onCompletion:)`.
- **Supply an engaging promotional image** for the redemption flow (defaults to app icon).
- **Align post-redemption experience** with subscriber status — welcome new subscribers, tour new features for upgraders. Handle subscribers who haven't opened the app yet.

### Helping People Manage Subscriptions

- **Provide subscription summaries** — show renewal date in settings/account screen. Use `Product.SubscriptionInfo`.
- **Use system-provided subscription management UI** via `showManageSubscriptions(in:)` for consistent upgrade/downgrade/cancel experience.
- **Encourage retention** — when notified of cancellation, offer a personalized deal or exit survey.
- **Always make cancellation easy** — don't bury the manage subscription action or make it hard to find.
- **Create branded complementary UI** — offer premium tiers, personalized plan suggestions, promotional/discounted offers, or offer codes for win-back.

## watchOS Considerations

Display the same required subscription information as other platforms, adapted for the small screen.

- **Clarify differences from other platforms** — if the watchOS app has different functionality or a content subset, be straightforward about what's available on Apple Watch vs other devices.
- **Use a modal sheet** for required sign-up info — keeps UI streamlined with a default Close button.
- **Make options easy to compare on small screens** using either:
  - **One button per option**: Each button includes price/duration; one tap starts signup. Lock up button with its description.
  - **List + single button**: One option per row, button title updates to reflect the selected option. Minimizes scrolling.