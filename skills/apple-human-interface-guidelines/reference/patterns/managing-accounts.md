# Managing Accounts

Guidelines for account creation, authentication, deletion, and TV provider accounts across Apple platforms.

## Best Practices

- **Explain benefits of creating an account** and how to sign up. Display a brief, friendly description in your sign-in view.
- **Delay sign-in as long as possible.** Let people experience your app before requiring commitment. E.g., a shopping app lets people browse freely, requiring sign-in only at purchase.
- **If not using Sign in with Apple, prefer passkeys.** Passkeys eliminate passwords — people just provide a username. If passwords are needed, require two-factor authentication.
- **Always identify the authentication method** in buttons. Use "Sign In with Face ID" not generic "Sign In."
- **Reference only available authentication methods.** Don't mention Face ID on devices without it. Check `LABiometryType`.
- **Avoid app-specific biometric auth settings.** Biometric authentication is a system-level setting; an in-app toggle is redundant.
- **Don't use the term "passcode"** for account authentication — people associate it with device unlock/Apple services.

## Account Deletion

If your app helps create accounts, you **must** also help delete them (not just deactivate). Comply with regional legal requirements.

- **Provide a clear way to initiate account deletion within your app.** If deletion must happen on a website, provide a direct, easily discoverable link (not buried in Privacy Policy/ToS).
- **Revoke Sign in with Apple tokens** when deleting accounts that used it.
- **Provide consistent deletion experience** across app and website — don't make one flow harder than the other.
- **Consider scheduled deletion.** Let people schedule future deletion (e.g., after subscription period ends), but always offer immediate deletion too.
- **Communicate deletion timeline.** Tell people when deletion will complete and notify them when finished.
- **Clarify billing for in-app purchases:**
  - Auto-renewable subscription billing continues through Apple until cancelled, regardless of account deletion.
  - People must separately cancel subscriptions or request refunds after account deletion.
  - Support account deletion even if the subscription wasn't purchased through your app.

## TV Provider Accounts

- Use TV Provider Authentication for efficient sign-in.
- **Don't show sign-out** when signed in at system level. If sign-out is needed, direct to Settings > TV Provider.
- **Never instruct sign-out via privacy controls.** Settings > Privacy manages app access to TV provider, not sign-out.

## Platform Considerations

### tvOS

- **Prefer sign-in via another device.** Configure associated domains so Apple TV works with other devices for credential suggestions.
- **Shared accounts:** Avoid asking profile selection every user switch. In tvOS 16+, use `kSecUseUserIndependentKeychain` and User Management Entitlement to share credentials while storing profiles separately.
- **Minimize data entry.** Use another-device websites for extensive info. For email, show the email keyboard with recent addresses.

### watchOS

- Use iCloud synchronization for Keychain access, enabling autofill of usernames/passwords and preserving app settings.