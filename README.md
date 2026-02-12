# Agent Skills

A collection of skills for AI coding agents focused on developer workflow. Skills are packaged instructions that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

### conventional-commits

Generate commit messages following the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification with Angular convention types. Contains structured rules, type definitions, and scope conventions.

**Use when:**
- Creating git commits
- Writing or formatting commit messages
- Enforcing consistent commit conventions across a project

**Types covered:**
- `feat` — New feature (SemVer MINOR)
- `fix` — Bug fix (SemVer PATCH)
- `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`

### pr-message

Write concise, high-signal GitHub pull request descriptions that explain intent, impact, and risk without duplicating information already visible in GitHub.

**Use when:**
- "Write a PR description"
- "Help me write the PR message"
- Opening a pull request and need a well-structured summary

**Sections covered:**
- Summary (what and why)
- What Changed (behavioral/functional changes only)
- Testing (concrete verification steps)
- Screenshots (UI changes only)
- Risk / Rollout (feature flags, migrations, rollback)
- Notes for Reviewers (tricky logic, non-obvious decisions)

### pr-review

Analyze and explain a pull request to help review it effectively. Summarizes what changed, why, how the pieces fit together, and what risks or concerns deserve attention.

**Use when:**
- "Review this PR"
- "Explain this pull request"
- "What should I look for in this PR?"
- Preparing to review someone else's code

**Analysis areas:**
- Understanding (problem, solution, core vs supporting changes)
- Risk & Correctness (bugs, edge cases, missing tests, rollback concerns)
- Architecture & Consistency (boundaries, patterns, coupling)
- Review Guidance (files to inspect closely, dependent changes)
- UI / Functional Changes (local testing needs, manual verification flows)

### conventional-comments

Format review comments following the [Conventional Comments](https://conventionalcomments.org/) standard. Provides labels, decorations, communication best practices, and examples for clear, actionable feedback.

**Use when:**
- Writing code review comments
- Giving PR feedback
- RFC reviews, peer reviews, or any written review process

**Format:**
```
<label> [decorations]: <subject>

[discussion]
```

**Labels:** `praise`, `nitpick`, `suggestion`, `issue`, `todo`, `question`, `thought`, `chore`, `note` (plus optional `typo`, `polish`, `quibble`)

**Decorations:** `(non-blocking)`, `(blocking)`, `(if-minor)`, and custom (e.g., `security`, `ux`)

### challenge-me

Direct, no-comfort technical advisor mode for counting/estimation and architecture/design. Challenges ideas, questions assumptions, and surfaces blind spots.

**Use when:**
- "Challenge my design"
- "Pressure-test this architecture"
- "Is this estimate realistic?"
- Evaluating tradeoffs or scoping work

**Focus areas:**
- Counting & Estimation — break "quick/easy" into concrete tasks, surface hidden work (edge cases, tests, migrations, rollback, security)
- Architecture & Design — pressure-test boundaries, ask what can fail, call out unnecessary complexity

## Installation

```bash
npx skills add milistu/agent-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
```
Write a commit message for my changes
```
```
Write the PR description
```
```
Review this pull request
```
```
Help me write review comments for this PR
```
```
Challenge my design for this feature
```
