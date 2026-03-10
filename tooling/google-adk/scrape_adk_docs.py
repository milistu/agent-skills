"""
Scrape Google ADK documentation for Python skill creation.

Fetches all relevant ADK docs pages, converts HTML -> Markdown using markdownify,
and saves them to tooling/data/google-adk/python/ organized by category.

Usage:
    cd tooling/google-adk/
    uv run python scrape_adk_docs.py
"""

import asyncio
import json
from pathlib import Path
from datetime import date

from markdownify import markdownify as md
from playwright.async_api import async_playwright
from tqdm.auto import tqdm


# ─── Output paths ────────────────────────────────────────────────────────────

DATA_DIR = Path("../data/google-adk/docs")
DATA_DIR.mkdir(parents=True, exist_ok=True)

TODAY = date.today().isoformat()

# ─── Pages to scrape ─────────────────────────────────────────────────────────
# Format: (url, output_relative_path)
# output_relative_path is relative to DATA_DIR

PAGES = [
    # Getting Started
    ("https://google.github.io/adk-docs/", "home.md"),
    ("https://google.github.io/adk-docs/get-started/python/", "getting-started/python-quickstart.md"),
    ("https://google.github.io/adk-docs/get-started/typescript/", "getting-started/typescript-quickstart.md"),
    ("https://google.github.io/adk-docs/get-started/go/", "getting-started/go-quickstart.md"),
    ("https://google.github.io/adk-docs/get-started/java/", "getting-started/java-quickstart.md"),
    ("https://google.github.io/adk-docs/get-started/installation/", "getting-started/advanced-setup.md"),
    ("https://google.github.io/adk-docs/get-started/about/", "getting-started/technical-overview.md"),
    ("https://google.github.io/adk-docs/get-started/quickstart/", "getting-started/quickstart-multi-tool-agent.md"),
    ("https://google.github.io/adk-docs/tutorials/agent-team/", "getting-started/tutorial-agent-team.md"),
    ("https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/", "getting-started/quickstart-streaming-python.md"),
    ("https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming-java/", "getting-started/quickstart-streaming-java.md"),
    ("https://google.github.io/adk-docs/tutorials/coding-with-ai/", "getting-started/coding-with-ai.md"),

    # Agents
    ("https://google.github.io/adk-docs/agents/", "agents/agents-overview.md"),
    ("https://google.github.io/adk-docs/agents/llm-agents/", "agents/llm-agents.md"),
    ("https://google.github.io/adk-docs/agents/workflow-agents/", "agents/workflow-agents.md"),
    ("https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/", "agents/workflow/sequential-agents.md"),
    ("https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/", "agents/workflow/loop-agents.md"),
    ("https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/", "agents/workflow/parallel-agents.md"),
    ("https://google.github.io/adk-docs/agents/custom-agents/", "agents/custom-agents.md"),
    ("https://google.github.io/adk-docs/agents/multi-agents/", "agents/multi-agent-systems.md"),
    ("https://google.github.io/adk-docs/agents/config/", "agents/agent-config.md"),

    # Models
    ("https://google.github.io/adk-docs/agents/models/", "models/models-overview.md"),
    ("https://google.github.io/adk-docs/agents/models/google-gemini/", "models/gemini.md"),
    ("https://google.github.io/adk-docs/agents/models/anthropic/", "models/claude.md"),
    ("https://google.github.io/adk-docs/agents/models/vertex/", "models/vertex-ai.md"),
    ("https://google.github.io/adk-docs/agents/models/apigee/", "models/apigee.md"),
    ("https://google.github.io/adk-docs/agents/models/ollama/", "models/ollama.md"),
    ("https://google.github.io/adk-docs/agents/models/vllm/", "models/vllm.md"),
    ("https://google.github.io/adk-docs/agents/models/litellm/", "models/litellm.md"),
    ("https://google.github.io/adk-docs/agents/models/litert-lm/", "models/litert-lm.md"),

    # Tools
    ("https://google.github.io/adk-docs/integrations/", "tools/tools-and-integrations.md"),
    ("https://google.github.io/adk-docs/tools-custom/function-tools/", "tools/function-tools-overview.md"),
    ("https://google.github.io/adk-docs/tools-custom/performance/", "tools/tool-performance.md"),
    ("https://google.github.io/adk-docs/tools-custom/confirmation/", "tools/action-confirmations.md"),
    ("https://google.github.io/adk-docs/tools-custom/mcp-tools/", "tools/mcp-tools.md"),
    ("https://google.github.io/adk-docs/tools-custom/openapi-tools/", "tools/openapi-tools.md"),
    ("https://google.github.io/adk-docs/tools-custom/authentication/", "tools/tool-authentication.md"),
    ("https://google.github.io/adk-docs/tools/limitations/", "tools/tool-limitations.md"),
    ("https://google.github.io/adk-docs/skills/", "tools/skills-for-agents.md"),

    # Runtime
    ("https://google.github.io/adk-docs/runtime/", "runtime/runtime-overview.md"),
    ("https://google.github.io/adk-docs/runtime/web-interface/", "runtime/web-interface.md"),
    ("https://google.github.io/adk-docs/runtime/command-line/", "runtime/command-line.md"),
    ("https://google.github.io/adk-docs/runtime/api-server/", "runtime/api-server.md"),
    ("https://google.github.io/adk-docs/runtime/resume/", "runtime/resume-agents.md"),
    ("https://google.github.io/adk-docs/runtime/runconfig/", "runtime/runtime-config.md"),
    ("https://google.github.io/adk-docs/runtime/event-loop/", "runtime/event-loop.md"),

    # Sessions & Memory
    ("https://google.github.io/adk-docs/sessions/", "sessions/sessions-overview.md"),
    ("https://google.github.io/adk-docs/sessions/session/", "sessions/sessions.md"),
    ("https://google.github.io/adk-docs/sessions/session/rewind/", "sessions/rewind-sessions.md"),
    ("https://google.github.io/adk-docs/sessions/session/migrate/", "sessions/migrate-sessions.md"),
    ("https://google.github.io/adk-docs/sessions/state/", "sessions/state.md"),
    ("https://google.github.io/adk-docs/sessions/memory/", "sessions/memory.md"),

    # Context
    ("https://google.github.io/adk-docs/context/", "context/context-overview.md"),
    ("https://google.github.io/adk-docs/context/caching/", "context/context-caching.md"),
    ("https://google.github.io/adk-docs/context/compaction/", "context/context-compression.md"),

    # Callbacks
    ("https://google.github.io/adk-docs/callbacks/", "callbacks/callbacks-overview.md"),
    ("https://google.github.io/adk-docs/callbacks/types-of-callbacks/", "callbacks/types-of-callbacks.md"),
    ("https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/", "callbacks/callback-patterns.md"),

    # Components
    ("https://google.github.io/adk-docs/artifacts/", "components/artifacts.md"),
    ("https://google.github.io/adk-docs/events/", "components/events.md"),
    ("https://google.github.io/adk-docs/apps/", "components/apps.md"),
    ("https://google.github.io/adk-docs/plugins/", "components/plugins.md"),
    ("https://google.github.io/adk-docs/mcp/", "components/mcp.md"),

    # A2A Protocol
    ("https://google.github.io/adk-docs/a2a/intro/", "a2a/a2a-introduction.md"),
    ("https://google.github.io/adk-docs/a2a/quickstart-exposing/", "a2a/quickstart-exposing-python.md"),
    ("https://google.github.io/adk-docs/a2a/quickstart-exposing-go/", "a2a/quickstart-exposing-go.md"),
    ("https://google.github.io/adk-docs/a2a/quickstart-consuming/", "a2a/quickstart-consuming-python.md"),
    ("https://google.github.io/adk-docs/a2a/quickstart-consuming-go/", "a2a/quickstart-consuming-go.md"),

    # Streaming
    ("https://google.github.io/adk-docs/streaming/", "streaming/streaming-overview.md"),
    ("https://google.github.io/adk-docs/streaming/dev-guide/part1/", "streaming/part1-intro-to-streaming.md"),
    ("https://google.github.io/adk-docs/streaming/dev-guide/part2/", "streaming/part2-sending-messages.md"),
    ("https://google.github.io/adk-docs/streaming/dev-guide/part3/", "streaming/part3-event-handling.md"),
    ("https://google.github.io/adk-docs/streaming/dev-guide/part4/", "streaming/part4-run-configuration.md"),
    ("https://google.github.io/adk-docs/streaming/dev-guide/part5/", "streaming/part5-audio-images-video.md"),
    ("https://google.github.io/adk-docs/streaming/streaming-tools/", "streaming/streaming-tools.md"),
    ("https://google.github.io/adk-docs/streaming/configuration/", "streaming/streaming-configuration.md"),

    # Grounding
    ("https://google.github.io/adk-docs/grounding/google_search_grounding/", "grounding/google-search-grounding.md"),
    ("https://google.github.io/adk-docs/grounding/vertex_ai_search_grounding/", "grounding/vertex-ai-search-grounding.md"),

    # Deployment
    ("https://google.github.io/adk-docs/deploy/", "deployment/deployment-overview.md"),
    ("https://google.github.io/adk-docs/deploy/agent-engine/", "deployment/agent-engine.md"),
    ("https://google.github.io/adk-docs/deploy/agent-engine/deploy/", "deployment/agent-engine-standard-deployment.md"),
    ("https://google.github.io/adk-docs/deploy/cloud-run/", "deployment/cloud-run.md"),
    ("https://google.github.io/adk-docs/deploy/gke/", "deployment/gke.md"),

    # Observability
    ("https://google.github.io/adk-docs/observability/", "observability/observability-overview.md"),
    ("https://google.github.io/adk-docs/observability/logging/", "observability/logging.md"),

    # Evaluation
    ("https://google.github.io/adk-docs/evaluate/", "evaluation/evaluation-overview.md"),
    ("https://google.github.io/adk-docs/evaluate/criteria/", "evaluation/evaluation-criteria.md"),
    ("https://google.github.io/adk-docs/evaluate/user-sim/", "evaluation/user-simulation.md"),

    # Safety
    ("https://google.github.io/adk-docs/safety/", "safety.md"),

    # Reference
    ("https://google.github.io/adk-docs/api-reference/cli/", "reference/cli-reference.md"),
    ("https://google.github.io/adk-docs/api-reference/agentconfig/", "reference/agent-config-reference.md"),
]

# ─── Pages to skip (with reasons, for the summary) ───────────────────────────

SKIPPED_PAGES = [
    ("https://google.github.io/adk-docs/visual-builder/", "GUI tool, not code-based development"),
    ("https://google.github.io/adk-docs/deploy/agent-engine/asp/", "Template scaffold, not core ADK dev"),
    ("https://google.github.io/adk-docs/deploy/agent-engine/test/", "Deployment testing, not development"),
    ("https://google.github.io/adk-docs/api-reference/python/", "External redirect to pkg.dev, not inline docs"),
    ("https://google.github.io/adk-docs/api-reference/typescript/", "External redirect to pkg.dev, not inline docs"),
    ("https://google.github.io/adk-docs/api-reference/rest/", "HTTP layer reference, low value for dev skill"),
    ("https://google.github.io/adk-docs/release-notes/", "Changelog, not developer guidance"),
    ("https://google.github.io/adk-docs/community/", "External links, not core content"),
    ("https://google.github.io/adk-docs/contributing-guide/", "Contributing to ADK itself, not using it"),
    ("https://google.github.io/adk-docs/api-reference/agentconfig/", "Interactive JSON schema viewer, not convertible to markdown"),
]


# ─── Scraper ─────────────────────────────────────────────────────────────────

ARTICLE_SELECTORS = ["article", "[role='main']", "main"]


async def scrape_page(page, url: str) -> str | None:
    """Navigate to URL and return article content as Markdown."""
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Try selectors in order
        selector_used = None
        for sel in ARTICLE_SELECTORS:
            try:
                await page.wait_for_selector(sel, timeout=5000)
                selector_used = sel
                break
            except Exception:
                continue

        if not selector_used:
            raise Exception("No content selector found on page")

        content_html = await page.locator(selector_used).first.inner_html()
        markdown_content = md(
            content_html,
            heading_style="ATX",
            strip=["button", "svg", "script", "style"],
            newline_style="backslash",
        )
        return markdown_content
    except Exception as e:
        print(f"\n  ERROR scraping {url}: {e}")
        return None


async def run_scraper():
    fetched = []
    errors = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        for url, rel_path in tqdm(PAGES, desc="Scraping ADK docs", unit="page"):
            content = await scrape_page(page, url)

            if content is None:
                errors.append({"url": url, "path": rel_path, "reason": "scrape_error"})
                continue

            # Create parent dirs and write file
            out_path = DATA_DIR / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)

            header = f"> Source: {url}\n> Fetched: {TODAY}\n\n"
            out_path.write_text(header + content.strip())
            fetched.append({"url": url, "path": rel_path})

        await browser.close()

    return fetched, errors


# ─── Summary ─────────────────────────────────────────────────────────────────

def write_summary(fetched: list[dict], errors: list[dict]):
    lines = [
        "# ADK Python Docs Scraping Summary",
        "",
        f"**Date:** {TODAY}",
        f"**Total pages fetched:** {len(fetched)}",
        f"**Total pages skipped (intentional):** {len(SKIPPED_PAGES)}",
        f"**Errors:** {len(errors)}",
        "",
        "## Fetched Pages",
        "",
    ]
    for item in fetched:
        lines.append(f"- `{item['path']}` — {item['url']}")

    lines += [
        "",
        "## Skipped Pages (Intentional)",
        "",
    ]
    for url, reason in SKIPPED_PAGES:
        lines.append(f"- {url} — *{reason}*")

    if errors:
        lines += [
            "",
            "## Errors",
            "",
        ]
        for item in errors:
            lines.append(f"- {item['url']} — {item.get('reason', 'unknown')}")

    summary_path = DATA_DIR / "SCRAPING_SUMMARY.md"
    summary_path.write_text("\n".join(lines))
    print(f"\nSummary written to {summary_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

async def main():
    print(f"Scraping {len(PAGES)} ADK docs pages to {DATA_DIR}/\n")
    fetched, errors = await run_scraper()
    write_summary(fetched, errors)
    print(f"\nDone! {len(fetched)} pages saved, {len(errors)} errors.")
    if errors:
        print("Errors:")
        for e in errors:
            print(f"  {e['url']}: {e['reason']}")


if __name__ == "__main__":
    asyncio.run(main())
