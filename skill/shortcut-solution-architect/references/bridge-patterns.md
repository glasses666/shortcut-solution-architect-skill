# Bridge Patterns

Use this file when selecting the recommended build path.

## Pattern 1: Native Shortcut-capable

Use when the target app or system surface already exposes the needed action.

Typical signs:
- native Shortcuts actions
- obvious built-in automation support
- no need to stage files through Finder

Output:
- direct shortcut design
- minimal fallback plan

## Pattern 2: Share-sheet bridge

Use when the source app can share/export a file or media item, but the destination app does not expose a native shortcut action.

Canonical example:
- `录音 -> 编码为 M4A -> 保存到监听目录 -> 打开 Buzz`

Why this is usually best:
- avoids database or process-lock issues
- avoids app-private APIs
- uses Apple-native surfaces

When to prefer over CLI:
- destination app already watches a folder
- source app only provides a temp export path
- the CLI path is known to be fragile or stateful

## Pattern 3: CLI/URL bridge

Use when the target app exposes:
- a stable CLI
- a stable URL scheme
- an AppleScript/JXA entrypoint that is not UI automation

Use this only when the interface is actually documented or repeatably testable.

## Pattern 4: UI automation only

Use only when:
- no native action exists
- no share-sheet/file bridge exists
- no CLI/URL/scriptable interface exists

Requirements:
- be explicit that it is brittle
- describe required permissions
- include stronger fallback guidance

## Pattern 5: Unsupported

Choose this when no reliable automation path exists.

What to say:
- why it is unsupported
- what minimal manual workflow remains possible
- what evidence would change the verdict

## Build-path tie breakers

- Prefer `Share-sheet bridge` over `CLI/URL bridge` when it removes app-state coupling.
- Prefer `CLI/URL bridge` over `UI automation only` when it is even moderately stable.
- Prefer `Unsupported` over inventing an unreliable architecture.
