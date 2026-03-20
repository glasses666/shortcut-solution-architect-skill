# Examples

Use these examples to keep recommendations concrete and realistic.

## Example 1: Buzz classroom workflow

Request:
- send a Voice Memos recording to Buzz
- keep the original recording safe
- make it easy for a normal Mac user

Recommended result:
- classification: `Share-sheet bridge`
- path: `录音 -> 编码为 M4A -> 保存到 Buzz 监听目录 -> 打开 Buzz`
- why:
  - avoids `buzz add` database-lock issues while the app is open
  - works with share-sheet temp exports
  - stays Apple-native

Artifacts:
- full shortcut design
- optional exported `.shortcut`
- optional local download path

## Example 2: CLI/URL bridge

Request:
- app has a documented CLI or URL scheme
- user wants a reusable agent workflow

Recommended result:
- classification: `CLI/URL bridge`
- path: shortcut gathers input, then calls the CLI or URL scheme

Why:
- more stable than UI automation
- more portable than machine-specific click scripts

## Example 3: Unsupported app

Request:
- desktop app with no share sheet, no scriptability, no documented CLI, and no import/export hook

Recommended result:
- classification: `Unsupported` or `UI automation only`
- answer explains the absence of stable automation surfaces
- no fake `.shortcut` or share-link claim

## Example 4: File vs link decision

Request:
- user wants “a link I can click to import”

Recommended result:
- if the environment can produce a signed `.shortcut`, provide a download path/link
- if Apple-backed sharing is really available, optionally provide an iCloud share link
- otherwise explain that the skill can produce the file but not publish the cloud link from the current environment

## Example 5: Cherri-worthy request

Request:
- generate many similar shortcuts from code
- keep the shortcut definition in version control
- produce a reusable file artifact

Recommended result:
- classification: usually `Native Shortcut-capable` or `Share-sheet bridge` at runtime, but `Cherri` is chosen as the build path
- path: `spec/DSL -> Cherri compile/generate -> optional Apple signing -> downloadable artifact`

Why:
- the user cares about repeatable generation more than one-off manual editing
- a code-first pipeline is part of the deliverable

Guardrails:
- still provide a native fallback
- do not claim iCloud sharing unless it is actually available

## Example 6: Delivery priority

Request:
- runtime path is already known
- user wants a working shortcut quickly
- manual assembly would require many repetitive UI actions

Recommended result:
- keep the runtime classification based on the real app surfaces
- prefer a generated `.shortcut` or shortcut spec/DSL as the first delivery fallback after the primary native runtime path is selected
- only drop to manual build instructions if generation is unavailable

Why:
- this reduces user effort without changing the runtime architecture
- it keeps Apple-native behavior while improving delivery quality
