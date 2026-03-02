# Generative AI Design Guidelines

Guidelines for designing responsible, effective generative AI features in Apple platform apps and games.

## Best Practices

- **Design responsibly.** Small changes to inputs (or the same input given multiple times) often produce very different outcomes. You can't always anticipate requests or responses. Orient design around experiences that are inclusive, designed with care, and protect privacy.
- **Keep people in control.** Respect agency — ensure people remain in charge of decision-making. Honor in-scope requests, handle sensitive content carefully. Provide ability to dismiss, revert, or retry content. Clearly identify when/where AI is used.
- **Ensure inclusive experiences.** AI models favor common information, leading to unintended biases. Ask people to provide information rather than inferring personal/cultural characteristics. Seek clarity before making assumptions (e.g., gender identities, relationship types). Test across diverse users.
- **Design engaging, useful features.** Offer generative features only when they provide clear value (time savings, improved communication, enhanced creativity).
- **Ensure graceful degradation.** Provide non-AI fallbacks when possible so the app remains useful when AI is unavailable or people opt out. Examples: Genmoji enhances emoji but regular emoji still work; summarization is helpful but notifications are readable without it.

## Transparency

- **Communicate where AI is used.** Never trick users into thinking AI-generated content is human-authored. Align disclosure with regional regulations.
- **Set clear expectations.** Clarify capabilities and limitations. Offer brief tutorials when introducing features. For open-ended features (search bars, generation prompts), offer curated suggestions. Explain known limitations up front and why inferior results occur.

## Privacy

- **Prefer on-device processing.** On-device models keep data on device, respond faster, and work offline. Use server-based models only when larger/more powerful models are needed. If using server processing, minimize what's shared, inform users about server data transmission, and clarify what data may be stored off-device or used for training.
- **Ask permission before using personal data.** Use minimum data needed, offer clear opt-out. Get explicit permission for model improvement or storage. Be aware model outputs can inadvertently contain sensitive information. Apps for kids have stricter data rules.
- **Disclose data usage clearly.** Explain benefits concisely and specifically when asking for permission. Articulate whether your model uses personal information for training.

## Models and Datasets

- **Evaluate model capabilities early.** Understand differences between general-knowledge and task-specific models. Some model types may be unavailable due to device compatibility, network access, or battery level. Foundation Models framework requires a compatible device with Apple Intelligence enabled.
- **Be intentional with datasets.** Choose datasets with diverse representations. Know data provenance. Ensure relevant licenses for data you don't own. Allow time for testing to mitigate bias and misinformation.

## Inputs

- **Guide usage.** Offer diverse, predefined example inputs that hint at what's possible.
- **Minimize hallucinations.** Generative models may produce plausible but fabricated content. Clearly communicate that AI-generated content may contain errors. Scope requests carefully. Avoid requesting factual information unless the model has verified, up-to-date data. Avoid AI-generated content where hallucinations could cause harm.
- **Handle destructive actions carefully.** Avoid automating destructive actions (deleting photos) or hard-to-undo actions (purchases). Ask for confirmation before significant actions. Adhere to model-specific usage policies and regional AI regulations.

## Outputs

- **Coach on blocked/undesirable results.** Minimize frustration by guiding people toward better requests. Offer example requests that might lead to better results.
- **Reduce harmful outcomes.** Test scenarios including: out-of-scope requests, poorly phrased/vague/ambiguous inputs, personal/sensitive/controversial topics, and requests encouraging harmful results. Use findings to improve models and prevention.
- **Avoid replicating copyrighted content.** Build on models with copyright protections. Curate inputs (e.g., pre-approved prompts). Explicitly instruct models to avoid mimicking certain content or styles.
- **Account for latency.** Generative models take longer than non-generative models. Design loading experiences or generate in background. See Loading guidelines.
- **Offer alternate versions.** Present single or multiple meaningfully different results. Offering choice gives people greater control and bridges the gap between model interpretation and user intent.

## Continuous Improvement

- **Improve models over time.** Update to adapt to behavior, respond to feedback, include new data. Some improvements (blocked word lists) can happen independently of app updates. Plan for fine-tuning, retesting, and prompt engineering when updating base models.
- **Let people share feedback.** Offer quick positive/negative feedback (thumbs up/down). Optionally offer detailed feedback for complex issues. Place feedback affordances in clear locations that don't interrupt the experience. Always make feedback voluntary.
- **Design flexible, adaptable features.** Separate model from UX so you can swap models over time. Lay a foundation for future adjustments while maintaining consistent user experience.