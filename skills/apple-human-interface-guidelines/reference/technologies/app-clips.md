# App Clips Design Guidelines

Guidance for designing App Clips — lightweight app experiences that are instantly available without full app installation. Covers UI design, App Clip cards, App Clip Codes, privacy, notifications, and printing specifications.

## When to Create an App Clip

**On-the-go experiences:** Rental bikes, coffee shops, food trucks, restaurants, museums — tasks performed over a finite time.

**Demo experiences:** Games (demo/tutorial), fitness apps (free workout), productivity apps (create a document) — let people try before buying.

## Designing Your App Clip

- Allow people to complete a task or demo entirely within the App Clip — don't require the full app install
- Focus on essential features only; reserve advanced features for the full app
- Don't use App Clips solely for marketing or to display ads
- Avoid web views — use native components; offer a website link instead if only web components are available
- Design a linear, focused UI — no tab bars, complex navigation, or settings; minimize screens and forms
- On launch, show the most relevant content immediately — skip unnecessary steps
- Include all required assets; omit splash screens; never make people wait on launch
- Keep the App Clip as small as possible; reduce unnecessary code and unused assets; avoid downloading additional data
- Make the App Clip shareable via Messages links
- Support Apple Pay for express checkout
- Avoid requiring account creation before providing value; if needed, use Sign in with Apple
- When the full app replaces the App Clip, provide a familiar experience — don't require re-login

## Preserving Privacy

- App Clips can't perform background operations
- Limit stored data; store login info securely off-device (system may delete App Clip data between launches)
- Offer Sign in with Apple and Apple Pay for privacy-preserving authentication and payment

## Showcasing Your App

App Clips don't appear on the Home Screen; the system removes them after inactivity.

- The App Clip card and system app banner already let people visit the App Store
- Don't compromise the UX by aggressively asking to install the full app
- Display `SKOverlay` at natural pauses (task completion) to recommend your full app
- Don't ask repeatedly or interrupt tasks; don't use push notifications to push app installs

## Notifications

App Clips can schedule/receive notifications for up to 8 hours after launch.

- Only request extended notification permission if functionality spans more than a day
- Keep notifications focused on the task — no promotional notifications
- Only send notifications in response to explicit user actions

## Creating App Clips for Businesses (Platform Providers)

- Use consistent branding — the business's brand should be front and center, not yours
- Handle multiple businesses/locations simultaneously; provide switching between recent businesses; verify location on launch

## App Clip Card Content

| Element | Specification |
|---------|---------------|
| Header image | 1800×1200 px PNG or JPEG, no transparency |
| Title | Max 30 characters |
| Subtitle | Max 56 characters |
| Action button verbs | **View** (media/informational), **Play** (games), **Open** (all others) |

- Use photography/graphics, not UI screenshots
- Avoid text in the header image (not localizable, hard to read)
- Clearly communicate the App Clip's purpose

## App Clip Codes

Two variants:
- **Scan-only** — camera icon in center; scan with Camera app or Code Scanner
- **NFC-integrated** — iPhone icon in center; hold device near or scan

### Display Guidelines

**Use NFC-integrated** when physically accessible (tabletops, registers, storefronts, signage, gift cards).

**Use scan-only** when inaccessible or digital (posters, printed ads, behind-counter signage, digital displays, emails, social media).

- Include the App Clip logo (badge design) when space allows; omit on disposable items or gambling/drinking items
- Place on flat or cylindrical surfaces only; on cylinders, width must not exceed 1/6 of circumference
- Avoid deformable materials (paper, plastic, fabric) — use rigid surfaces
- Ensure adequate lighting for scan-only codes; avoid wide-angle scanning requirements
- Don't overlay with text, logos, or images; never animate or dim
- Display in upright position — don't rotate

### Minimum Sizes

| Type | Minimum Size |
|------|-------------|
| Printed | 3/4 inch (1.9 cm) diameter |
| Digital | 256×256 px (PNG or SVG) |
| NFC-integrated | NFC tag ≥35 mm diameter; printed code ≥1.37 inches (3.48 cm) diameter |

- Distance-to-code-size ratio: max 20:1, prefer 10:1 (e.g., 40" distance → ≥4" diameter)
- If near a QR code, make the App Clip Code at least the same size
- Minimum clear space = distance between center glyph and circular code

### Call-to-Action Messaging

**Scan-only:**
- "Scan to [action]."
- "Scan using the camera on your iPhone or iPad to [action]."

**NFC-integrated:**
- "Scan to [action]."
- "Hold your iPhone near the [object] to launch an App Clip that [action]."

### Customization Rules

- Always use generated App Clip Codes — never create custom designs
- Don't apply filters, color augmentation, glows, shadows, gradients, or reflections
- Don't change aspect ratio when scaling; scale all attributes proportionally
- Choose foreground/background colors with sufficient contrast; tools will reject inadequate contrast

## Printing Guidelines

- Use high-quality, non-textured, matte finish materials
- Avoid gloss, reflective, holographic overlays, or thin laminate; use matte laminate if needed
- For outdoor use: UV-resistant materials/coatings
- Use flexographic printing (professional) or inkjet (desktop)
- Rasterize SVG at ≥600 ppi; print at ≥300 dpi
- Convert sRGB SVG to CMYK using relative colorimetric intent
- Use "Generic CMYK ICC profile" (CMYK printers) or "Gracol 2013 ICC profile" (CMYKOV printers)
- Color tolerance: CIELab Delta E of 2.5
- Grayscale printers: only generate grayscale codes (color codes printed in grayscale may not scan reliably)
- NFC tags: use Type 5 NFC tags, ≥35 mm diameter
- For large batches: conduct small test runs; use print templates showing encoded URL and SVG filename for validation
- Use Apple's [printer calibration test sheets](https://developer.apple.com/app-clips/resources/printer-calibration-test-sheets.zip) to verify settings

## Legal Requirements

- Only Apple-provided App Clip Codes (from App Store Connect or App Clip Code Generator) are approved
- Stop displaying codes when your App Clip is no longer active
- Don't use App Clip Code elements (Apple Logo, App Clip mark) in company/product names
- Don't seek copyright/trademark registration for App Clip Codes
- Don't translate Apple trademarks — keep in English
- Always use title case for "App Clips" and "App Clip Code"

## Platform Support

iOS and iPadOS only. Not supported on macOS, tvOS, visionOS, or watchOS.