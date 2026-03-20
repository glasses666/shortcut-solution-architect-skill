# System App Textbook

Use this file for built-in macOS apps before doing web research. Treat these as default assumptions, then confirm with local inspection when the exact behavior matters.

## Shortcuts

- Default assumption: native Shortcuts actions obviously exist because this is the host app.
- Likely useful surfaces:
  - `shortcuts` CLI
  - URL schemes
  - AppleScript/JXA listing and running metadata
- Verify locally:
  - `which shortcuts`
  - `shortcuts --help`
  - `sdef /System/Applications/Shortcuts.app`

## Finder

- Default assumption: strong file-oriented integration and common Quick Action relevance.
- Likely useful surfaces:
  - file input/output
  - services / Quick Actions
  - AppleScript support
- Verify locally:
  - `sdef /System/Library/CoreServices/Finder.app`
  - app bundle metadata

## Safari

- Default assumption: URL-centric workflows are likely; AppleScript support is common.
- Likely useful surfaces:
  - URL handling
  - AppleScript/JXA
  - share sheet for webpages
- Verify locally:
  - `sdef /Applications/Safari.app`
  - URL schemes and bundle metadata

## Notes

- Default assumption: share-sheet and content-capture workflows are plausible.
- Likely useful surfaces:
  - share extension behavior
  - content input
  - possible AppleScript limitations compared with classic scriptable apps
- Verify locally:
  - bundle metadata
  - `sdef` presence or absence

## Reminders

- Default assumption: built-in task capture is likely straightforward through native actions.
- Prefer native Shortcuts actions over custom bridges.
- Verify locally only when a specific edge case matters.

## Calendar

- Default assumption: built-in event creation/update actions likely exist.
- Prefer native Shortcuts actions over file or GUI bridges.
- Verify locally only when a specific edge case matters.

## Photos

- Default assumption: media-centric flows and native actions are likely.
- Likely useful surfaces:
  - media input
  - save/export patterns
  - share sheet
- Verify locally if file export behavior is critical.

## Mail

- Default assumption: native composition and content handoff are likely.
- Prefer native Shortcuts actions or standard share flows.
- Verify locally if attachment handling is central.

## Music

- Default assumption: playback and media library actions are likely, but exact library mutation behavior may vary.
- Verify locally if the workflow depends on playlists or library writes.

## Voice Memos

- Default assumption: source app for recordings, not a deeply scriptable automation target.
- Most reliable pattern:
  - share sheet export
  - optional media encode
  - file bridge into the destination app
- Verify locally:
  - share sheet input/output behavior
  - exported file format from current macOS

## General rule for system apps

- Prefer textbook defaults plus local inspection.
- Do not spend tokens on web research unless a system app behaves unexpectedly on the current Mac.
- Safe mental model:
  - strongest native support: `Shortcuts`, `Reminders`, `Calendar`
  - strongest file-centric support: `Finder`
  - strongest URL/content handoff: `Safari`, `Notes`, `Mail`
  - strongest media-source/media-target patterns: `Photos`, `Music`, `Voice Memos`
