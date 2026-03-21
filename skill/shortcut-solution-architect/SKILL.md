---
name: shortcut-solution-architect
description: Design, research, generate, validate, and distribute Apple Shortcuts solutions for macOS. Use when a user wants to build a shortcut, wire an app into Shortcuts or the share sheet, judge whether an app is automatable, produce a shortcut file or import/share link, or create a reusable shortcut workflow for ordinary agents and OpenClaw-style agents.
---

# Shortcut Solution Architect

Turn a shortcut request into a decision-complete solution with four fixed outputs:

1. `Capability Report`
2. `Recommended Build Path`
3. `Artifacts`
4. `Quality Gate`

Default to Apple-native macOS runtime routes first. Treat local inspection as the primary source of truth for app capabilities on the current Mac. Treat third-party compilers and reverse-engineered signing as optional escalations for artifact generation, not the default runtime answer.

## Workflow

1. Collect the minimum input set.
   Required:
   - target task
   - target app
   - platform, default `macOS`
   - desired deliverable: plan, file, link, or all
   - user language or dominant language of the current conversation, so the plan and operator-facing instructions can be written in the user's language by default

2. Run a capability pass.
   - Start with local inspection, not web search.
   - Run [scripts/local_app_inspector.py](scripts/local_app_inspector.py) against the target app when local access is possible.
   - Inspect what is actually available on this Mac: install state, bundle path, bundle identifier, URL schemes, document types, extensions, AppleScript/JXA support, executable path, likely CLI entrypoints, and other observable metadata.
   - Read [references/local-inspection-playbook.md](references/local-inspection-playbook.md) when you need a fuller local probe checklist or supporting commands.
   - Read [references/system-app-textbook.md](references/system-app-textbook.md) and [references/popular-app-textbook.md](references/popular-app-textbook.md) when the app is a built-in macOS app or a covered popular app.
   - Use [scripts/capability_matrix_builder.py](scripts/capability_matrix_builder.py) to produce a structured compatibility judgment before proposing implementation details.
   - Only if the app surface is still unclear or the user explicitly wants broader research, run [scripts/research_prompt_builder.py](scripts/research_prompt_builder.py) and save the prompt under `./deepresearch-prompts/`.

3. Classify the integration path.
   Prefer this order:
   - `Native Shortcut-capable`
   - `Share-sheet bridge`
   - `CLI/URL bridge`
   - `UI automation only`
   - `Unsupported`

   If evidence is incomplete, report the unknowns explicitly instead of pretending the app is supported.

4. Choose the build path.
   - Read [references/official-capabilities.md](references/official-capabilities.md) for Apple-native constraints.
   - Read [references/bridge-patterns.md](references/bridge-patterns.md) for pattern selection.
   - Read [references/cherri-advanced-path.md](references/cherri-advanced-path.md) when a code-driven shortcut generator is relevant.
   - Use Apple-native actions, share sheet flows, file bridges, `shortcuts` CLI, and URL schemes first.
   - If the runtime path is clear but a manual build would be expensive, fragile, or hard for the user to reproduce, prefer generated shortcut artifacts before falling back to a hand-built-only answer.
   - Only fall back to asking the user to assemble the shortcut manually after native runtime routes and advanced generation routes have both been judged unavailable or too risky.
   - Do not default to brittle GUI automation. Use it only as a last-resort fallback and say that clearly.

5. Plan artifacts.
   - Use [scripts/shortcut_artifact_planner.py](scripts/shortcut_artifact_planner.py) to convert the compatibility result into an artifact plan.
   - Default artifact policy:
     - always provide a complete implementation plan
     - when the user wants a working shortcut and ordinary runtime architecture is known, prefer producing a generated shortcut artifact or shortcut spec before telling the user to build it manually
     - provide shortcut spec/AST/DSL when a file is requested but generation is not yet guaranteed
     - provide `.shortcut` files only when the generation path is supported
     - provide download links by default when the environment can expose a file
     - when a download link is not available, place generated local files in a shallow, easy-to-open location instead of a deeply nested build directory
     - provide iCloud share links only when a real Apple-account-backed publish step is available
   - Read [references/distribution-playbook.md](references/distribution-playbook.md) before promising any link.

6. Produce the final report in this exact section order.
Use [assets/report_template.md](assets/report_template.md) as the output skeleton.
Write the implementation plan, operator guidance, and user-facing action labels in the user's language by default unless the user explicitly asks for a different language.

### Capability Report

Include:
- app name
- task
- whether the judgment is based on local inspection, textbook knowledge, network research, or a mix
- detected integration surfaces:
  - native shortcut action support
  - share sheet/file input support
  - CLI support
  - URL scheme support
  - AppleScript/JXA support
  - GUI automation fallback only
- evidence
- unknowns
- classification

### Recommended Build Path

State one primary route and one fallback route.

For the primary route, specify:
- why it wins
- what macOS capability it relies on
- whether it is portable across Macs or tied to the current machine
- what the user must already have installed

### Artifacts

State exactly what will be produced:
- plan doc
- shortcut spec/AST/DSL
- `.shortcut` file
- local downloadable file path
- optional iCloud link

If an artifact cannot be produced safely, say so and give the blocker.

If a `.shortcut` file is part of the answer:
- prefer old-format plus Apple signing on macOS
- use [scripts/sign_shortcut_wrapper.py](scripts/sign_shortcut_wrapper.py) only when the input file already exists
- do not imply that signing alone creates the shortcut structure
- when possible, give the user an easy-open path or downloadable link instead of only reporting a deep filesystem path

### Quality Gate

Read [references/quality-gate.md](references/quality-gate.md).

Always include:
- `Preflight`
- `Run 1`
- `Run 2 fallback`
- `Run 3 fallback`

The answer must be good enough that a user can get to a working result in three attempts or fewer without making architecture decisions themselves.
When a generated shortcut includes user-visible error handling, prefer modal alerts with detailed reasons over notification-only failure reporting.

## Decision Rules

### Apple-native first

Use Apple-native routes whenever the task can be solved with:
- Shortcuts app actions
- share sheet input
- file bridge patterns
- `shortcuts run/view/sign`
- URL schemes

This rule applies to the runtime architecture, not necessarily to the delivery method. A shortcut may still be best delivered as a generated artifact even when the runtime architecture is Apple-native.

### Local evidence first

Prefer this evidence order:
- current-Mac local inspection
- bundled textbook references for system or common apps
- network research only as supplemental evidence

Do not let generic web documentation override concrete local evidence from the user's machine.

### Cherri is optional

Mention Cherri only when:
- the user explicitly wants code-driven shortcut generation, or
- a file artifact is required and a native manual build path is too costly
- a reusable generator pipeline is more valuable than a one-off manually built shortcut
- the ordinary route is understood, but generating the shortcut is better than asking the user to click through a long manual build

Do not make Cherri the default recommendation for simple share sheet or file-bridge tasks.

When Cherri is chosen:
- describe it as a code-first shortcut generator/compiler path
- keep Apple-native Shortcuts behavior as the runtime target
- be explicit that Cherri is an advanced route with extra tooling requirements
- still include a native fallback if the Cherri pipeline is unavailable
- prefer Cherri or another supported generator before falling back to "the user must build it manually"

### Download link vs iCloud link

Default to a downloadable file path or downloadable artifact link.

Only promise an iCloud share link when:
- the environment can publish through a real Apple account, and
- the shortcut has actually been exported/shared

### Unsupported software

If the app lacks native actions, share sheet integration, scriptable entrypoints, and stable bridge options:
- classify it as `Unsupported` or `UI automation only`
- explain why
- do not invent a file or link workflow

### Language alignment

- Default the plan, build steps, fallback instructions, and shortcut labels to the user's language.
- If the conversation is multilingual, prefer the language used for the task request itself.
- Only switch to English-first documentation when the user explicitly asks for it or the target ecosystem is clearly English-only.

### UX defaults for generated shortcuts

- When a shortcut exposes many target formats or many actions, prefer a hierarchical menu such as `type -> format` over one long flat list.
- When a shortcut can fail in ways the user must understand, prefer a modal alert with actionable detail instead of a notification that can collapse away.
- For long-running or file-centric shortcuts, failure should be explicit and success should still be visible; do not make users infer success only from a side effect such as Finder opening.
- Preserve user expectations about outputs when possible:
  - keep the original base filename
  - avoid silent overwrite unless the user explicitly wants it
  - reveal the output in Finder when the task is file-centric
  - choose default transcode presets that match likely user intent instead of technically correct but unexpectedly huge outputs
- Generated artifacts should be easy for the user to access:
  - prefer download links when available
  - otherwise copy the final `.shortcut` and any required sidecar scripts to a shallow path such as the workspace root or another clearly named handoff folder
- If a generated shortcut invokes shell code:
  - assume the runtime shell environment is more restricted than Terminal
  - do not assume Homebrew binaries are on `PATH`
  - prefer inline shell for small logic, or explicitly managed sidecar deployment for larger logic
  - verify at least one real runtime failure path from inside the shortcut, not only from Terminal
  - when the shortcut handles media, verify at least one real image, one real audio, and one real video input
  - do not assume stream inspection alone is enough for type detection; still images can be misclassified as video by media tooling

## References

Read only what you need:

- [references/official-capabilities.md](references/official-capabilities.md)
  Use for Apple-supported boundaries: `shortcuts` CLI, import, share, URL schemes.
- [references/bridge-patterns.md](references/bridge-patterns.md)
  Use for pattern selection and common integration shapes.
- [references/cherri-advanced-path.md](references/cherri-advanced-path.md)
  Use when evaluating code-first shortcut generation, file artifacts, or repeatable generator pipelines.
- [references/cherri-pitfalls.md](references/cherri-pitfalls.md)
  Use during real `.shortcut` generation to avoid common Cherri parser, typing, interpolation, artifact-path, shell-runtime, and user-facing error-message pitfalls.
- [references/local-inspection-playbook.md](references/local-inspection-playbook.md)
  Use for local, non-destructive app inspection before falling back to research.
- [references/system-app-textbook.md](references/system-app-textbook.md)
  Use for built-in macOS app defaults before spending tokens on research.
- [references/popular-app-textbook.md](references/popular-app-textbook.md)
  Use for covered third-party app defaults before spending tokens on research.
- [references/distribution-playbook.md](references/distribution-playbook.md)
  Use for download link vs iCloud share decisions.
- [references/quality-gate.md](references/quality-gate.md)
  Use for the three-attempt success bar.
- [references/examples.md](references/examples.md)
  Use for concrete cases such as Buzz file-bridge, CLI/URL bridge, and unsupported apps.

## Scripts

- [scripts/research_prompt_builder.py](scripts/research_prompt_builder.py)
  Generate a DeepResearch prompt and optional file.
- [scripts/local_app_inspector.py](scripts/local_app_inspector.py)
  Inspect a locally installed app and gather capability evidence from the current Mac.
- [scripts/capability_matrix_builder.py](scripts/capability_matrix_builder.py)
  Build a structured compatibility judgment.
- [scripts/shortcut_artifact_planner.py](scripts/shortcut_artifact_planner.py)
  Turn compatibility and deliverable goals into an artifact plan.
- [scripts/sign_shortcut_wrapper.py](scripts/sign_shortcut_wrapper.py)
  Wrap `shortcuts sign` for already-generated shortcut payloads.

## Output Standards

- Be transparent about unsupported assumptions.
- Prefer local evidence over generic internet claims.
- Separate what is verified on the current Mac from what is only generally likely.
- Prefer one strong route over multiple weak routes.
- Never leave the implementer to choose the architecture.
- Prefer a generated shortcut artifact or structured shortcut spec over a long manual click-by-click build when both are feasible.
- If manual assembly is still required, explain that it is a fallback, not the first choice.
- Match the user's language for plan voice and operator guidance by default.
