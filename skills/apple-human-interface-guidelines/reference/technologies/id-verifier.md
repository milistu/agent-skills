# ID Verifier

Design guidelines for integrating ID Verifier into iPhone apps to read ISO18013-5 compliant mobile IDs in person.

## Request Types

- **Display Only request**: Displays data (name, age, portrait photo) in system-provided UI on the requester's iPhone for visual confirmation. Customer data stays within system UI and is not transmitted to your app.
- **Data Transfer request**: For legal verification requirements where you need to store or process information (address, date of birth). Requires an additional entitlement.

## Best Practices

- **Ask only for the data you need.** People lose trust if you ask for more data than necessary. For age verification, use an age threshold request rather than requesting actual age or birth date.

- **Register with Apple Business Register** if your app qualifies, so customers see your official organization name and logo during the ID verification UI on their devices.

- **Provide a button that initiates the verification process:**
  - Use **"Verify Age"** for simple age checks
  - Use **"Verify Identity"** for more detailed identity data requests
  - **Do not** include symbols suggesting a particular communication type (NFC, QR codes)
  - **Never** include the Apple logo in any button label

| Button Label | Use Case |
| --- | --- |
| Verify Age | Checking whether people are old enough to attend an event or access a venue |
| Verify Identity | Verifying specific identity information like name and birth date (e.g., rental car pickup) |

- **In Display Only requests, provide feedback UI for visual confirmation.** When the reader displays the customer's portrait, provide buttons like "Matches Person" and "Doesn't Match Person" so your app can receive an approved or rejected value in the response.

## Platform Support

iOS only. Not supported in iPadOS, macOS, tvOS, visionOS, or watchOS.