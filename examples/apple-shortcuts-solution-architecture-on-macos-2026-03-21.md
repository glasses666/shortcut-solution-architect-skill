| Dimension | Expected Content (Preview) | Remarks |
| :--- | :--- | :--- |
| **Capability Matrix** | Native actions, share sheet, CLI, URL scheme, AppleScript/JXA, GUI automation fallback | Apple-native evidence first |
| **Delivery Path** | Plan only vs `.shortcut` file vs download link vs optional iCloud link | Default to portable macOS flow |
| **Quality Gate** | Preflight, Run 1, Run 2 fallback, Run 3 fallback for `Buzz` | Target 3 attempts or fewer |
| **Example Pattern** | `send a recording into a watched transcription folder` mapped to share-sheet bridge, CLI/URL bridge, or unsupported verdict | Avoid invented integrations |

```markdown
---
date: 2026-03-21
tags: [software-development, shortcuts, macos, automation, apple-shortcuts]
model_version: v2.0
---

# DeepResearch Prompt: Apple Shortcuts solution architecture on macOS

## 🧩 Context & Background
We want a production-usable research pack for building a reusable Apple Shortcuts skill that helps an agent research, design, generate, validate, and distribute macOS shortcuts. The immediate target app is `Buzz` and the immediate task is `send a recording into a watched transcription folder`. The desired deliverable level is `plan + file + link`.

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
5. Concrete examples, including `Buzz` for `send a recording into a watched transcription folder`
6. Recommended artifacts for a reusable skill targeted at ordinary agents and OpenClaw-style agents

## 🧠 Strategy
If evidence is incomplete for a path, list the missing evidence and downgrade confidence instead of assuming success.
```
