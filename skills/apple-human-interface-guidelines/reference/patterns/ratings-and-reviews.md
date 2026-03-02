# Ratings and Reviews

Guidelines for when and how to ask users for app ratings and reviews across Apple platforms.

## Best Practices

- **Ask only after demonstrated engagement.** Prompt after completing a game level or significant task. Never ask on first launch or during onboarding — users haven't formed an opinion yet and may leave negative feedback.

- **Don't interrupt tasks or gameplay.** Look for natural breaks or stopping points where a request is least disruptive.

- **Don't pester.** Allow at least 1–2 weeks between requests, and only re-prompt after additional engagement.

- **Use the system-provided prompt.** iOS, iPadOS, and macOS provide a standard in-app rating prompt via [`RequestReviewAction`](https://developer.apple.com/documentation/StoreKit/RequestReviewAction) (StoreKit). The system:
  - Checks for previous feedback before displaying
  - Allows rating + optional written review
  - Dismissible with a single tap/click
  - Users can opt out of prompts for all apps
  - **Automatically limits display to 3 times per app per 365-day period**

- **Consider the trade-offs of resetting your summary rating.** Resetting reflects the current version's quality but results in fewer total ratings, which can discourage downloads.

## Platform Considerations

No additional platform-specific considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS.