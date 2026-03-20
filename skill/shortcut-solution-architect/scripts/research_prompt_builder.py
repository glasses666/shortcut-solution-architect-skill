#!/usr/bin/env python3
"""Generate a DeepResearch prompt for Apple Shortcuts solution work."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re


DEFAULT_TOPIC = "Apple Shortcuts solution architecture on macOS"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "apple-shortcuts-research"


def build_reference_table(app: str, task: str) -> str:
    return f"""| Dimension | Expected Content (Preview) | Remarks |
| :--- | :--- | :--- |
| **Capability Matrix** | Native actions, share sheet, CLI, URL scheme, AppleScript/JXA, GUI automation fallback | Apple-native evidence first |
| **Delivery Path** | Plan only vs `.shortcut` file vs download link vs optional iCloud link | Default to portable macOS flow |
| **Quality Gate** | Preflight, Run 1, Run 2 fallback, Run 3 fallback for `{app}` | Target 3 attempts or fewer |
| **Example Pattern** | `{task}` mapped to share-sheet bridge, CLI/URL bridge, or unsupported verdict | Avoid invented integrations |"""


def build_prompt(topic: str, app: str, task: str, deliverable: str) -> str:
    today = date.today().isoformat()
    return f"""---
date: {today}
tags: [software-development, shortcuts, macos, automation, apple-shortcuts]
model_version: v2.0
---

# DeepResearch Prompt: {topic}

## 🧩 Context & Background
We want a production-usable research pack for building a reusable Apple Shortcuts skill that helps an agent research, design, generate, validate, and distribute macOS shortcuts. The immediate target app is `{app}` and the immediate task is `{task}`. The desired deliverable level is `{deliverable}`.

## 🎯 Objectives
- Determine the real automation surfaces available on macOS for Apple Shortcuts work.
- Identify how to classify third-party apps into Native Shortcut-capable, Share-sheet bridge, CLI/URL bridge, UI automation only, or Unsupported.
- Establish a reliable default build path with Apple-native preference.
- Determine when `.shortcut` file generation, downloadable artifacts, and iCloud share links are truly feasible.
- Define a quality gate that helps users reach a working shortcut within 3 attempts.

## 📋 Scope
In scope:
- Apple Shortcuts on macOS
- share-sheet workflows
- `shortcuts` CLI and URL schemes
- import/export/sign behavior for shortcut files
- app capability discovery methods
- portable guidance for ordinary macOS users
- optional advanced routes such as Cherri or Apple signing wrappers

Out of scope:
- iOS-only assumptions unless they directly affect macOS
- undocumented claims without strong evidence
- brittle GUI automation as the default solution

## 🔍 Key Questions
- What are the best practical methods to detect whether a macOS app can be integrated through Shortcuts?
- Which signals most strongly indicate native action support, share-sheet compatibility, CLI/URL viability, or effective non-support?
- How should a skill decide whether to return only a plan, a shortcut spec, a `.shortcut` file, a download link, or an iCloud share link?
- What are the safest workflows for generating importable shortcut files on current macOS versions?
- What failure modes most often prevent a shortcut from working on the first attempt, and how should a 3-attempt quality gate be designed?

## 💻 Constraints (Domain Adapted)
- Must be compatible with current macOS Shortcuts behavior.
- Prefer Apple-supported capabilities first.
- Prefer production-usable, repeatable workflows over clever reverse engineering.
- Treat Cherri and reverse-engineered signing as optional advanced paths, not default answers.

## 🚫 Anti-Goals
- No deprecated or abandoned tooling as the primary path.
- No “just script the GUI” recommendation unless no better route exists.
- No fabricated promises that a cloud share link can always be produced.
- No vague compatibility language without concrete criteria.

## 📚 Sources & Citations
- Prefer Apple Support and Apple developer documentation for official capability boundaries.
- Use reputable GitHub repos only for advanced generation/signing routes.
- Clearly separate official support from community or reverse-engineered behavior.

## 📊 Expected Output & Format
Return:
1. A capability-detection framework for macOS apps
2. A build-path decision tree
3. A file/link feasibility matrix
4. A quality-gate checklist
5. Concrete examples, including `{app}` for `{task}`
6. Recommended artifacts for a reusable skill targeted at ordinary agents and OpenClaw-style agents

## 🧠 Strategy
If evidence is incomplete for a path, list the missing evidence and downgrade confidence instead of assuming success.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", default=DEFAULT_TOPIC)
    parser.add_argument("--app", default="Buzz")
    parser.add_argument("--task", default="share a recording into a watched transcription folder")
    parser.add_argument("--deliverable", default="plan + file + link")
    parser.add_argument("--output-dir", default="deepresearch-prompts")
    parser.add_argument("--stdout-only", action="store_true")
    args = parser.parse_args()

    table = build_reference_table(args.app, args.task)
    prompt = build_prompt(args.topic, args.app, args.task, args.deliverable)
    content = f"{table}\n\n```markdown\n{prompt}```\n"

    if args.stdout_only:
        print(content)
        return 0

    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slugify(args.topic)}-{date.today().isoformat()}.md"
    out_path.write_text(content, encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
