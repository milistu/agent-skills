# Machine Learning Design Guidelines

Apple HIG guidance for designing apps that incorporate machine learning features, covering input/output patterns, feedback mechanisms, and error handling.

## Role of Machine Learning in Your App

Classify your ML feature along these dimensions to guide design decisions:

### Critical vs Complementary
- **Critical**: Feature won't work without ML (e.g., Face ID). Demands high accuracy and reliability.
- **Complementary**: App works without it (e.g., QuickType suggestions). People are more forgiving of lower quality.

### Private vs Public Data
- More sensitive data → more serious consequences of inaccuracy
- Health data misinterpretation causes anxiety and erodes trust; music recommendations are low-stakes
- All apps must protect user privacy regardless of data sensitivity

### Proactive vs Reactive
- **Proactive**: Provides results without user request (e.g., Siri Suggestions). People have less tolerance for low-quality proactive results.
- **Reactive**: Provides results when people ask or take action (e.g., QuickType). Helps with current tasks.

### Visible vs Invisible
- **Visible**: People see and interact with results (e.g., word suggestions). People form reliability opinions directly.
- **Invisible**: Results aren't obvious (e.g., adaptive tap areas). Harder to communicate reliability or receive feedback.

### Dynamic vs Static
- **Dynamic**: Improves as people interact (e.g., Face ID adapts to facial changes). Often uses calibration and feedback.
- **Static**: Improves only with app updates (e.g., Photos object recognition per iOS release).

## Explicit Feedback

Actionable information people provide in response to a specific app request. Favoriting and social feedback are *implicit* — not explicit.

- Request explicit feedback **only when necessary** — prefer implicit feedback to avoid extra work for users
- Always make providing feedback **voluntary**
- Use **simple, direct language** describing each option and its consequences. Avoid vague terms like "dislike." Examples:
  - "Suggest less pop music"
  - "Suggest more thrillers"
  - "Mute politics for a week"
- Add icons to descriptions only if they aid comprehension; never use an icon alone
- Consider offering **multiple options** with progressively specific choices
- **Act immediately** on feedback and **persist** changes — content should disappear instantly and not reappear elsewhere
- Use feedback to fine-tune **when and where** results appear, not just what appears

## Implicit Feedback

Information gleaned from user actions without explicit requests.

- **Secure people's information** — implicit feedback can gather sensitive data
- **Help people control their information** — explain how data is used across apps; give control over information flow
- **Don't let implicit feedback reduce exploration** — avoid reinforcing only existing behaviors; leave room for discovery
- **Use multiple feedback signals** to mitigate misinterpretation — a single action (viewing a photo) doesn't confirm intent
- **Withhold private/sensitive suggestions** — people share devices; avoid embarrassing recommendations
- **Prioritize recent feedback** — tastes change; fall back to historical only when recent data is unavailable
- **Match update cadence to mental model** — typing suggestions update instantly; song recommendations shouldn't change so fast that people feel rushed
- **Anticipate UI changes affecting feedback** — even small button repositioning can change interaction patterns
- **Beware confirmation bias** — implicit feedback only covers what people can see/do; it doesn't reveal new interests

## Calibration

Process where people provide initial information before a feature can function (e.g., Face ID face scan).

- Use calibration **only when the feature can't function without it**
- **Secure** all information provided
- **Be clear about why** information is needed — emphasize what the feature does, not how it works
- **Collect only essential information** — minimal data increases trust
- **Avoid repeat calibration** — do it once, early; evolve via feedback afterwards. Exception: calibrating with different objects (e.g., new baseball fields)
- **Make it quick and easy**:
  - Prioritize a few key pieces of info; infer the rest
  - Don't ask for info people would need to look up
  - Don't ask for difficult actions
- **Show explicit goals and progress** (e.g., Face ID tick marks)
- **Provide immediate help if progress stalls** — never blame the user; always give a clear next step
- **Confirm success** — reward completion with a clear path to using the feature
- **Let people cancel at any time** without judgment
- **Give people a way to update or remove** calibration information, both within and outside the calibration flow

## Corrections

How people fix mistakes the app makes.

- Provide **familiar, easy** correction methods — show the steps the app took so people know which controls to use
- **Provide immediate value** — instantly display corrected content and persist updates
- **Let people correct their corrections** — respond immediately and persist
- **Balance feature benefits with correction effort** — if correcting is harder than doing the task manually, people will abandon the feature
- **Never rely on corrections to compensate for low-quality results** — this erodes trust
- **Learn from corrections** when they lead to higher quality results (corrections are a form of implicit feedback)
- **Prefer guided corrections** (suggesting specific alternatives) over freeform corrections (requiring manual input) — combine both when appropriate

## Mistakes

Three principles:
1. **Anticipate mistakes** — design avoidance and mitigation strategies
2. **Help people handle mistakes** — tools must match consequence severity
3. **Learn from mistakes** when it improves the app (but beware of causing unpredictability)

Patterns that address mistakes: Limitations, Corrections, Attribution, Confidence, Explicit/Implicit Feedback.

- **Match corrective actions to consequence severity** — wrong keyboard suggestion ≠ missed flight
- **Make frequent/predictable mistakes easy to correct**
- **Continuously update** to reflect evolving interests and preferences
- **Address mistakes without complicating the UI** — corrections and limitations integrate seamlessly; attributions can be harder
- **Be especially careful with proactive features** — people have less patience since they didn't request the result
- **Watch for cascading effects** — optimizing recognition for one category may degrade another

## Multiple Options

Contexts: suggested options (proactive), requested options (reactive), and corrections.

- **Prefer diverse options** — balance accuracy with variety (e.g., Maps shows toll-free, scenic, and highway routes)
- **Avoid too many options** — increased cognitive load; list on one screen when possible
- **List most likely option first** — use confidence values and contextual info (time, location); consider selecting the first option by default
- **Make options easy to distinguish** — provide brief descriptions highlighting differences; group into scannable categories when many options exist
- **Learn from selections** — use implicit feedback to refine future option ordering

## Confidence

Measure of certainty for a result. Verify that confidence values actually correspond to result quality before using them.

- **Know what values mean before presenting them** — low-quality results presented prominently erode trust
- **Translate confidence into understandable concepts** — "Because you listen to pop music" is better than "97% match"
- **Rank/order results to imply confidence** when attributions aren't helpful; use semantic categories ("high chance", "low chance") if displaying directly
- **Show numerical confidence only when people expect statistical info** (weather, sports, polling)
- **Express confidence as actionable suggestions** — "This is a good time to buy" vs. displaying percentages
- **Adapt presentation to confidence thresholds** — high confidence: show results directly; lower confidence: ask for confirmation (e.g., Photos face recognition)
- **Avoid showing results when confidence is low**, especially for proactive/suggestion features — set a minimum confidence threshold

## Attribution

Expresses the rationale for a result without explaining model internals. Example: "Because you've read mysteries."

Use attributions to:
- Encourage behavior changes
- Minimize mistake impact
- Help people build mental models
- Promote trust over time

Guidelines:
- **Use attributions to distinguish among results** in multiple-option scenarios
- **Avoid being too specific or too general** — overly specific feels surveillance-like; overly general feels impersonal
- **Keep attributions factual and objective** — "Because you've read nonfiction" not "Because you love nonfiction"
- **Avoid technical/statistical jargon** unless the result itself is statistical (weather, sports, science)

## Limitations

Two types: things a feature can't do well, and things it can't do at all.

- **Help people establish realistic expectations** — for rare but serious limitations, disclose before use (in marketing or feature context); for minor ones, use attributions
- **Demonstrate how to get best results**:
  - Use placeholder text to suggest valid input (e.g., Photos search bar: "Photos, People, Places…")
  - Provide real-time feedback during interaction (e.g., Animoji suggests better lighting)
  - Suggest alternatives instead of showing no results (e.g., Siri suggests a reminder when timers aren't available on Mac)
- **Explain causes of unsatisfactory results** — help people understand limitations (e.g., Animoji says it doesn't work in the dark)
- **Consider notifying people when limitations are resolved** in updates, so they can adjust their mental model