# Apple Shortcuts Capabilities On macOS

Use this reference when deciding what is officially supported and what is merely possible.

## Apple-native capabilities to prefer

- `Shortcuts.app` can receive share-sheet input and file/media input.
- `shortcuts` CLI supports:
  - `run`
  - `list`
  - `view`
  - `sign`
- `.shortcut` files can be imported through the Shortcuts app.
- Shortcut URL schemes can:
  - create a blank shortcut UI
  - open a shortcut
  - run a shortcut
  - use x-callback-url flows

## What Apple does not officially expose

- No official CLI for `create`, `edit`, or `import`.
- No official API for editing a shortcut action graph as structured data.
- No official stable interface for bulk mutation of the local shortcut database.

## Practical implications

- Running and orchestrating shortcuts is officially supported.
- Signing an already-generated shortcut payload is officially supported.
- Creating shortcut internals is not officially modeled as a public API.
- A solution that depends only on the Shortcuts app, share sheet, file bridges, URL schemes, and `shortcuts` CLI is more portable across Macs.

## Default recommendation

Prefer these build routes in order:

1. Native shortcut actions
2. Share-sheet bridge
3. File bridge
4. CLI/URL bridge
5. Cherri or other code-generation tooling
6. GUI automation fallback

Use route 5 or 6 only when the requested deliverable cannot be met by routes 1-4.
