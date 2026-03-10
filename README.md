# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions that extend agent capabilities, from commit hygiene to full design system references.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Skills at a Glance

| Skill | What it does | Trigger phrases |
|-------|-------------|-----------------|
| [conventional-commits](#conventional-commits) | Commit messages following the Conventional Commits spec | "Write a commit message", "Commit my changes" |
| [conventional-comments](#conventional-comments) | Structured code review comments | "Write review comments", "Give PR feedback" |
| [pr-message](#pr-message) | Concise, high-signal PR descriptions | "Write a PR description" |
| [pr-review](#pr-review) | Analyze a PR for effective review | "Review this PR", "Explain this pull request" |
| [challenge-me](#challenge-me) | Blunt technical advisor mode | "Challenge my design", "Pressure-test this" |
| [humanizer](#humanizer) | Remove signs of AI writing from text | "Humanize this text", "Make it sound less AI" |
| [apple-human-interface-guidelines](#apple-human-interface-guidelines) | Apple HIG reference across all platforms | "Review my UI for HIG compliance" |
| [google-adk](#google-adk) | Google Agent Development Kit reference for building AI agents | "Build an ADK agent", "Deploy my ADK agent to GCP" |

---

## Developer Workflow

### conventional-commits

Generate commit messages following the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification with Angular convention types.

**Use when:** creating git commits, writing commit messages, or enforcing consistent commit conventions.

**Types:** `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`

### conventional-comments

Format review comments following the [Conventional Comments](https://conventionalcomments.org/) standard. Provides labels, decorations, and communication best practices for clear, actionable feedback.

**Use when:** writing code review comments, giving PR feedback, or any written review process.

**Labels:** `praise`, `nitpick`, `suggestion`, `issue`, `todo`, `question`, `thought`, `chore`, `note` (plus optional `typo`, `polish`, `quibble`)

**Decorations:** `(non-blocking)`, `(blocking)`, `(if-minor)`, and custom (e.g., `security`, `ux`)

### pr-message

Write concise, high-signal GitHub pull request descriptions that explain intent, impact, and risk without duplicating information already visible in GitHub.

**Use when:** opening a pull request and you need a well-structured summary.

**Sections:** Summary, What Changed, Testing, Screenshots (UI only), Risk / Rollout, Notes for Reviewers

### pr-review

Analyze and explain a pull request to help review it effectively. Summarizes what changed, why, how the pieces fit together, and what risks deserve attention.

**Use when:** preparing to review someone else's code or trying to understand a PR quickly.

**Analysis areas:** Understanding, Risk & Correctness, Architecture & Consistency, Review Guidance, UI / Functional Changes

### challenge-me

Direct, no-comfort technical advisor mode. Challenges ideas, questions assumptions, and surfaces blind spots.

**Use when:** evaluating tradeoffs, scoping work, or pressure-testing an architecture decision.

**Focus areas:**
- **Architecture & Design** — pressure-test boundaries, ask what can fail, call out unnecessary 
- **Counting & Estimation** — break "quick/easy" into concrete tasks, surface hidden work
complexity

---

## Writing

### humanizer

Detect and remove signs of AI-generated writing from text. Based on documented, research-backed patterns from [Wikipedia's Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

**Use when:** writing, editing, or rewriting text to sound more natural and avoid AI detection patterns.

**What it catches:**

| Category | Examples |
|----------|----------|
| AI vocabulary | "delve", "tapestry", "vibrant", "pivotal", "foster", "underscore" |
| Inflated significance | "serves as a testament to", "marking a pivotal moment" |
| Promotional puffery | "nestled in the heart of", "boasts a diverse array" |
| Structural tells | "not just X, but also Y", rule-of-three, "despite challenges" |
| Grammar quirks | "serves as" instead of "is", synonym cycling, dangling "-ing" phrases |
| Style artifacts | title case headings, bold-colon lists, em dash overuse |

---

## Design & UI

### apple-human-interface-guidelines

Comprehensive [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) reference covering all Apple platforms. Contains 150+ reference documents organized by category.

**Use when:** designing or reviewing UI for iOS, iPadOS, macOS, tvOS, watchOS, or visionOS — or applying Apple's design principles to any app.

**Platforms:** iOS, iPadOS, macOS, tvOS, watchOS, visionOS

**Coverage:**

| Category | What's included |
|----------|----------------|
| Getting Started | Platform-specific design fundamentals and constraints |
| Foundations | Accessibility, color, dark mode, typography, layout, motion, privacy, branding |
| Patterns | Data entry, search, feedback, loading, onboarding, modality, navigation, media |
| Components | Buttons, menus, lists, tabs, sheets, alerts, pickers, toggles, charts, and more |
| Inputs | Touch, Apple Pencil, keyboard, game controllers, Digital Crown, gaze (visionOS) |
| Technologies | Apple Pay, Sign in with Apple, HealthKit, ARKit, CarPlay, SharePlay, Generative AI |

**Common tasks quick reference:**

| Task | References loaded |
|------|-------------------|
| Building a login screen | Privacy, Sign in with Apple, Managing Accounts |
| Designing a settings screen | Settings patterns, Toggles |
| Choosing colors / dark mode | Color guidelines, Dark Mode |
| Implementing navigation | Tab bars, Sidebars, Split views |
| Accessibility audit | Accessibility foundations, VoiceOver |
| Designing a form | Entering data, Text fields, Pickers |
| Building for visionOS | visionOS fundamentals, Spatial layout, Immersive experiences |

Many foundations (accessibility, color, typography, motion, privacy, writing) are applicable beyond Apple platforms to web and cross-platform development.

---

## AI Agent Development

### google-adk

[Google Agent Development Kit](https://google.github.io/adk-docs/) reference for building AI agents in Python, TypeScript, Go, and Java. Contains 90+ reference files organized by topic. The 10 most code-heavy files are split into per-language sidecars so you load only what you need.

**Use when:** building or configuring ADK agents, wiring tools, managing sessions and state, setting up multi-agent pipelines, streaming with the Gemini Live API, deploying to GCP, or evaluating agent behavior.

**Languages:** Python (primary), TypeScript, Go, Java

**Coverage:**

| Category | What's included |
|----------|----------------|
| Agents | LlmAgent, SequentialAgent, LoopAgent, ParallelAgent, custom BaseAgent, multi-agent routing |
| Tools | Function tools, MCP, OpenAPI, tool authentication, action confirmations |
| Sessions & Memory | Session service, state prefixes, MemoryService, cross-session recall |
| Callbacks | Before/after model, tool, and agent callbacks |
| Streaming | Gemini Live API, LiveRequestQueue, run_live(), audio/video/images |
| Deployment | Vertex AI Agent Engine, Cloud Run, GKE |
| Context | Context caching, context compression (EventsCompactionConfig) |
| Evaluation | Criteria, test writing, user simulation |
| A2A Protocol | Agent-to-Agent communication |
| Observability | Logging, Cloud Trace |

---

## Installation

```bash
npx skills add milistu/agent-skills
```

## Usage

Skills are automatically available once installed. The agent uses them when relevant tasks are detected.

```
Write a commit message for my changes
```
```
Write review comments for this PR
```
```
Write the PR description
```
```
Review this pull request
```
```
Challenge my design for this feature
```
```
Humanize this text — it sounds too AI-generated
```
```
Review my UI against Apple HIG
```
```
How do I add OAuth2 authentication to my ADK tool?
```

## Skill Structure

Each skill contains:
- `SKILL.md` — Instructions for the agent
- `reference/` — Supporting documentation (optional)

## License

MIT
