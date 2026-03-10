"""
Clean scraped ADK documentation and copy to skills/google-adk/reference/.

Removes scraping artifacts and content bloat:
- Source/Fetched metadata headers
- [¶](url) heading anchor links
- Supported in ADK / version badge blocks
- Language tab nav links and selector strings (PythonTypeScriptGoJava, etc.)
- Google CDN image references
- Floating admonition labels (Note, Warning, Tip, Experimental as lone lines)
- Adjacent nav-link chains ([text](#anchor)[text2](#anchor2)...)
- Related Concepts / Next Steps footer sections
- Copyright headers in code blocks (Apache 2.0 boilerplate)
- 3-of-4 duplicate language code blocks (keep Python, strip TypeScript/Go/Java)
- Excessive blank lines

Usage:
    cd tooling/google-adk/
    uv run python clean_adk_docs.py
"""

import re
from pathlib import Path

SRC_DIR = Path("../data/google-adk/docs")
DST_DIR = Path("../../skills/google-adk/reference")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def is_code_fence(line: str) -> bool:
    return line.startswith("```")


def strip_consecutive_code_blocks(lines: list[str]) -> list[str]:
    """Keep only the first code block in any sequence of consecutive unlabeled
    code blocks (i.e. blocks separated only by blank lines).

    ADK docs show every concept in Python, TypeScript, Go, Java as 4 separate
    unlabeled fenced code blocks in a row. We keep the first (Python) and drop
    the rest, since Python is the primary language and the others are redundant
    for most users.

    A block is "unlabeled" if the opening fence is exactly ``` (no language tag).
    We preserve labeled blocks (```python, ```bash, etc.) always.
    """
    result = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # Check if this starts an unlabeled code block
        if line.rstrip() == "```":
            # Find the closing fence
            block_lines = [line]
            i += 1
            while i < n and lines[i].rstrip() != "```":
                block_lines.append(lines[i])
                i += 1
            if i < n:
                block_lines.append(lines[i])  # closing ```
                i += 1

            result.extend(block_lines)

            # Now look ahead: skip any subsequent unlabeled code blocks that
            # follow with only blank lines in between
            while i < n:
                # Skip blank lines
                j = i
                while j < n and lines[j].strip() == "":
                    j += 1

                # If next non-blank line is an unlabeled code fence, skip it
                if j < n and lines[j].rstrip() == "```":
                    # Skip blank lines before
                    i = j + 1
                    # Skip until closing fence
                    while i < n and lines[i].rstrip() != "```":
                        i += 1
                    if i < n:
                        i += 1  # skip closing fence
                    # Also skip trailing blank after removed block (keep 1)
                else:
                    break
        else:
            result.append(line)
            i += 1

    return result


def strip_copyright_in_code_blocks(lines: list[str]) -> list[str]:
    """Remove Apache 2.0 copyright headers that appear inside code blocks."""
    result = []
    i = 0
    n = len(lines)
    in_code = False

    while i < n:
        line = lines[i]

        if is_code_fence(line):
            in_code = not in_code
            result.append(line)
            i += 1
            continue

        if in_code and re.match(r'^//\s*Copyright \d{4} Google', line):
            # Skip until end of license block (look for "limitations under the License")
            while i < n and not re.match(r'^//\s*limitations under the License', lines[i]):
                i += 1
            if i < n:
                i += 1  # skip the "limitations" line too
            # Skip one more blank line inside code if present
            if i < n and lines[i].strip() == "":
                i += 1
            continue

        result.append(line)
        i += 1

    return result


def strip_footer_sections(lines: list[str]) -> list[str]:
    """Remove trailing navigation/footer sections like Related Concepts, Next Steps."""
    footer_headings = re.compile(
        r'^#{1,3}\s*(Related Concepts|Next Steps?|Next:|What\'s Next|See Also|Continue Learning)',
        re.IGNORECASE
    )
    # Find last occurrence of a footer heading and truncate there
    last_footer_idx = None
    for idx, line in enumerate(lines):
        if footer_headings.match(line):
            last_footer_idx = idx

    if last_footer_idx is not None:
        return lines[:last_footer_idx]
    return lines


# ─── Main cleaner ─────────────────────────────────────────────────────────────

def clean_content(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # 1. Remove source/fetched metadata header lines
        if line.startswith("> Source: ") or line.startswith("> Fetched: "):
            i += 1
            continue

        # 2. Remove heading anchor links: [¶](url "Permanent link")
        line = re.sub(r'\[¶\]\([^)]+\)', '', line)

        # 3. Remove Google CDN image lines
        if re.match(r'^\s*!\[.*?\]\(https?://(lh\d+\.googleusercontent\.com|fonts\.gstatic\.com|[^)]*google[^)]*)\)', line):
            i += 1
            continue

        # 4. Remove markdown link-chain tab navigation
        # Matches lines like [Python](#python)[TypeScript](#typescript)[Go](#go)...
        if re.match(r'^\s*(\[(?:Python|TypeScript|Typescript|Go|Java|Kotlin|Windows CMD|Windows Powershell|MacOS[^)]*)\]\(#[^)]*\)){2,}\s*$', line, re.IGNORECASE):
            i += 1
            continue

        # 5. Remove concatenated language selector strings (PythonTypeScriptGoJava, etc.)
        # These appear at the start of files as raw text from tab UI elements
        if re.match(r'^(Python|TypeScript|Typescript|Go|Java|Kotlin|Experimental){1,5}$', line.strip()):
            i += 1
            continue
        if re.match(r'^(Python|Go|Java)(Experimental)$', line.strip()):
            i += 1
            continue

        # 6. Remove "Supported in ADK" version badge blocks
        if line.strip() == "Supported in ADK":
            i += 1
            while i < n and re.match(r'^\s*(Python|Typescript|TypeScript|Go|Java|Kotlin)\s+v\d+', lines[i].strip()):
                i += 1
            continue

        # Also handle inline badge format
        line = re.sub(r'Supported in ADK\s*(?:(?:Python|Typescript|TypeScript|Go|Java|Kotlin)\s+v[\d.]+\s*)*', '', line)

        # 7. Remove floating admonition labels (lone lines that are just "Note", "Warning", etc.)
        if re.match(r'^(Note|Warning|Caution|Tip|Info|Experimental)\s*$', line.strip()):
            i += 1
            continue

        # 8. Strip full google.github.io URLs from inline links, keeping link text
        # [text](https://google.github.io/adk-docs/...) -> text
        line = re.sub(r'\[([^\]]+)\]\(https://google\.github\.io/adk-docs/[^)]*\)', r'\1', line)

        cleaned.append(line)
        i += 1

    # 9. Strip copyright headers inside code blocks
    cleaned = strip_copyright_in_code_blocks(cleaned)

    # 10. Strip duplicate language code blocks (keep only first/Python)
    cleaned = strip_consecutive_code_blocks(cleaned)

    # 11. Strip footer nav sections
    cleaned = strip_footer_sections(cleaned)

    result = "\n".join(cleaned)

    # 12. Collapse 3+ consecutive blank lines to 2
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    # 13. Strip leading/trailing whitespace
    result = result.strip()

    return result


# ─── Runner ───────────────────────────────────────────────────────────────────

def process_all():
    docs_dir = SRC_DIR
    skill_ref_dir = DST_DIR

    md_files = list(docs_dir.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "SCRAPING_SUMMARY.md"]

    print(f"Processing {len(md_files)} files...")
    processed = 0
    errors = []
    total_before = 0
    total_after = 0

    for src_path in md_files:
        rel_path = src_path.relative_to(docs_dir)
        dst_path = skill_ref_dir / rel_path

        try:
            content = src_path.read_text(encoding="utf-8")
            cleaned = clean_content(content)

            before = len(content.splitlines())
            after = len(cleaned.splitlines())
            total_before += before
            total_after += after

            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(cleaned, encoding="utf-8")
            processed += 1

            reduction = (before - after) / before * 100 if before > 0 else 0
            if reduction > 20:
                print(f"  {rel_path}: {before} -> {after} lines ({reduction:.0f}% reduction)")
        except Exception as e:
            errors.append((str(rel_path), str(e)))
            print(f"  ERROR {rel_path}: {e}")

    overall = (total_before - total_after) / total_before * 100 if total_before > 0 else 0
    print(f"\nDone! {processed} files written to {skill_ref_dir}")
    print(f"Total: {total_before} -> {total_after} lines ({overall:.0f}% reduction)")
    if errors:
        print(f"{len(errors)} errors:")
        for path, err in errors:
            print(f"  {path}: {err}")


if __name__ == "__main__":
    process_all()
