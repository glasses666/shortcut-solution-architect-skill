# Popular App Textbook

Use this file for covered third-party apps before doing web research. Treat these as starting assumptions and confirm with local inspection when the exact path matters.

## Buzz

- Default assumption: more reliable as a destination app through file bridges than through a concurrently-running CLI queue mutation path.
- Best-known pattern:
  - share/export source audio
  - optionally encode to M4A
  - save into a watched folder
  - open Buzz
- Local verification points:
  - app installed path
  - bundle executable
  - whether watch-folder mode is configured
  - whether CLI use collides with a running app state
- Local evidence from this Mac:
  - installed at `/Applications/Buzz.app`
  - bundle identifier `com.chidiwilliams.buzz`
  - version `1.4.4`
  - no detected URL scheme
  - no detected AppleScript dictionary
  - no detected share extension or document-type hints
- Practical consequence:
  - default to the watched-folder/file-bridge route
  - treat direct CLI queue mutation while the GUI app is open as suspect unless freshly verified

## Obsidian

- Default assumption: file-based integration is usually the strongest route.
- Likely useful surfaces:
  - vault file creation/update
  - URL schemes
  - share sheet or file handoff
- Prefer file or URL bridges over GUI automation.
- Verify locally:
  - bundle metadata
  - URL schemes
  - vault location assumptions

## Notion

- Default assumption: often better treated as URL/web/API-oriented than as a native share-sheet destination.
- Likely useful surfaces:
  - URLs
  - browser or web capture flows
  - app link/open flows
- Be careful not to assume rich local native automation without local proof.

## Raycast

- Default assumption: launcher/workflow integration is plausible, but exact command surfaces depend on installed extensions and settings.
- Likely useful surfaces:
  - URL schemes
  - scripts/commands
  - possible extension-driven workflows
- Verify locally before promising exact behavior.

## General rule for covered third-party apps

- Prefer local inspection over internet docs for what this specific Mac can do.
- Use the textbook only to reduce token cost and to form a first hypothesis.
- If local evidence contradicts the textbook, trust local evidence.
- Safe defaults:
  - `Buzz`: file bridge
  - `Obsidian`: file bridge or URL bridge
  - `Notion`: web/URL bridge
  - `Raycast`: URL/script-command bridge
