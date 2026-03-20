# Distribution Playbook

Use this file when deciding whether to produce a file, a local download path, or a share link.

## Distribution levels

### Plan only

Use when:
- the app is unsupported
- file generation is not yet feasible
- the user only asked for architecture or compatibility

### Downloadable artifact

Use when:
- a `.shortcut` file or equivalent artifact can actually be created
- the current environment can expose the file path or attach the file

Default recommendation:
- downloadable artifact path or download link

### iCloud share link

Use only when:
- the shortcut has actually been shared/exported through Apple-backed sharing
- the current environment has the Apple account and permissions to publish

Do not promise iCloud links as a generic capability.

## What to include in the Artifacts section

- artifact type
- creation status: planned, generated, signed, shared
- path or link
- portability note
- blockers if not available

## Default policy

- prefer download links or local downloadable artifacts
- treat iCloud links as optional enhancement
- if neither is possible, provide a precise manual export/share path
