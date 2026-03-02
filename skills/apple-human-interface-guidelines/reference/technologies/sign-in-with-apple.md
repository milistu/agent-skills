# Sign in with Apple

Guidelines for implementing Sign in with Apple across all platforms, including button design, UX flow, data collection, and custom button creation.

## Offering Sign in with Apple

- **Ask people to sign in only in exchange for value.** Display a brief description of sign-in benefits.
- **Delay sign-in as long as possible.** Let people explore before requiring sign-in.
- **If you require an account, ask people to set it up before offering sign-in options.** Explain why an account is required first.
- **Consider letting people link an existing account to Sign in with Apple.** Support linking via matching email or through account settings.
- **In commerce apps, wait until after purchase before asking to create an account.** Support guest checkout; offer account creation on the order confirmation page.
- **Welcome people to their new account immediately** after Sign in with Apple completes. Don't delay with unnecessary information requests.
- **Indicate current sign-in status** — display "Using Sign in with Apple" in settings or account views.

## Collecting Data

- **Clarify whether additional data is required or optional.** Explain legally/contractually required data vs. experience-enhancing data.
- **Don't ask people to supply a password** — unless they've stopped using Sign in with Apple.
- **Avoid asking for a personal email when people supply a private relay address.** Respect the relay choice. Let people view their relay address in your app; use alternative identifiers (order numbers, phone numbers) for customer service.
- **Let people engage with the app before asking for optional data.** Don't block features if optional data isn't provided.
- **Be transparent about collected data.** Welcome people using the name/email they shared to show how data is used.

## Displaying Buttons

**Prominently display a Sign in with Apple button.** Make it no smaller than other sign-in buttons; don't make people scroll to see it.

### System-Provided Buttons

System buttons provide:
- Apple-approved appearance
- Ideal content proportions as style changes
- Automatic locale translation
- Configurable corner radius (iOS, macOS, web)
- VoiceOver alternative text

**Available titles (iOS, macOS, tvOS, web):**
- "Sign in with Apple"
- "Sign up with Apple"
- "Continue with Apple"

**watchOS title:** "Sign in" only.

### Button Appearance Styles

| Style | Platforms | Use On |
|---|---|---|
| **White** | All platforms + web | Dark backgrounds with sufficient contrast |
| **White with outline** | iOS, macOS, web | White/light backgrounds lacking contrast with white fill. Avoid on dark/saturated backgrounds. |
| **Black** | All platforms + web | White/light backgrounds with sufficient contrast. Don't use on dark backgrounds. |

**watchOS exception:** The black button uses system-defined dark gray (not pure black) to contrast with the pure black Apple Watch background.

### Button Size and Corner Radius

- Corner radius is customizable: square corners, default rounded, or capsule shape (iOS, macOS, web).
- Match corner radius to other buttons in your app.

| Minimum width | Minimum height | Minimum margin |
|---|---|---|
| 140pt (140px @1x, 280px @2x) | 30pt (30px @1x, 60px @2x) | 1/10 of button height |

## Creating a Custom Button

Custom buttons are allowed for iOS, macOS, and web. App Review evaluates all custom buttons.

Download Apple logo artwork from [Apple Design Resources](https://developer.apple.com/design/resources/) (PNG, SVG, PDF). Available in black and white, for logo-only and logo+text buttons.

### Logo File Rules

- Use only downloaded Apple logo artwork; never create a custom Apple logo.
- Use the logo file to position the logo in a button; never use the logo as the button itself.
- Match logo file height to button height.
- Don't crop the logo file.
- Don't add vertical padding.

### What You CANNOT Change

- **Titles:** Only "Sign in with Apple", "Sign up with Apple", or "Continue with Apple"
- **General shape:** Logo+text buttons are always rectangular; logo-only buttons can be circular or rectangular
- **Logo and title colors:** Must be either black or white within a button; no custom colors

### What You CAN Change

- Title font (weight and size adjustable)
- Title case (can capitalize all letters)
- Background appearance (must remain black or white overall; subtle texture/gradient OK)
- Button corner radius
- Button bezel and shadow (stroke, drop shadow)

### Custom Logo+Text Button Specs

- **Logo file format:** Use SVG/PDF for any height; use PNG only for 44pt-tall buttons.
- **Title font proportions:** Title font size = 43% of button height (button height = 233% of font size, rounded to nearest integer).
  - 44pt button → 19pt font
  - 56pt button → 24pt font
- **Prefer the system font** for the title.
- **Preserve default capitalization** unless your UI is all uppercase.
- **Vertically center** title and logo in the button.
- **Logo inset:** Adjustable to align with other authentication logos.
- **Minimum right margin for title:** At least 8% of button width.
- **Minimum button size:** 140×30pt. **Minimum margin:** 1/10 of button height.

### Custom Logo-Only Button Specs

- Always 1:1 aspect ratio.
- Use SVG/PDF for any size; PNG only for 44×44pt.
- Don't add horizontal padding (artwork includes correct padding).
- Use a mask (circle, rounded rect) to change shape; never crop the artwork or add extra padding.
- **Minimum margin:** 1/10 of button height.