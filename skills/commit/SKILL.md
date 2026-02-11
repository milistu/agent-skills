---
name: commit
description: Analyze git changes, group files into meaningful commits, and create clean git commits
disable-model-invocation: true
---

# Commit Changes

## Overview
Analyze the current git changes, group related files into meaningful commits, and create clean git commits.
Each commit should represent a single logical change and stage only the files that belong to that change.

## Commit Message Standard
Use a short, one-sentence commit message with a conventional prefix.

### Allowed Prefixes
- **Feat:** introducing a new feature or capability
- **Fix:** bug fixes or behavior corrections
- **Refactor:** code restructuring without behavior change
- **Chore:** tooling, config, or maintenance work
- **Docs:** documentation-only changes
- **Test:** adding or updating tests

### Commit Message Rules
- Exactly one sentence
- Short and descriptive
- Describe *what changed* or *what was added*
- Do not include:
  - Ticket IDs
  - Branch names
  - File names or file lists

## How to Group Files
Group files into a single commit **only if they represent one logical change**.

Use the following reasoning (not rigid rules):

### Good Reasons to Group Files
- Files belong to the same conceptual change or feature
- Files are required together to introduce a new behavior
- Changes span multiple files but serve one responsibility
- Application code and its entry point / handler are tightly coupled

### Good Reasons to Split into Separate Commits
- Changes occur in different architectural layers or responsibilities
- A contract or interface is introduced separately from its implementation
- A domain or model change can stand alone before being used
- Implementation details can evolve independently from orchestration

### Avoid
- One large commit covering unrelated changes
- One commit per file when files clearly belong together
- Staging everything together out of convenience

## Staging Rules
- Never use `git add .`, `git add -A`, or similar
- Always stage files explicitly using `git add <file>`
- Stage only the files that belong to the current commit

## Steps
1. Inspect the current git status and diffs.
2. Identify distinct logical changes.
3. Decide which files belong together based on responsibility and behavior.
4. For each group:
   - Stage only the relevant files using explicit `git add` commands.
   - Write a one-sentence commit message using an appropriate prefix.
   - Create the commit.
5. Repeat until all changes are committed.
6. Output a short summary of the commits created.

## Examples (Conceptual)
- Introducing a new domain concept → one commit
- Defining an interface or contract → one commit
- Wiring that contract into application flow → one commit
- Providing a concrete implementation → one commit

These examples illustrate *thinking patterns*, not strict rules.
