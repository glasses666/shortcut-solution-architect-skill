# Quality Gate

Every answer must aim for a working result within three attempts.

## Required subsections

### Preflight

State:
- what must already exist
- what app/version/platform assumptions were made
- what permissions may be required

### Run 1

Describe the expected happy path:
- what the user clicks or runs
- what success looks like
- what visible confirmation to check

### Run 2 fallback

Provide the most likely correction for the first failure mode.

Examples:
- wrong share-sheet input type
- file copied to wrong folder
- app path not found
- CLI missing from PATH

### Run 3 fallback

Provide the second-most likely correction and a stop condition.

Examples:
- switch from CLI to file bridge
- disable fragile option and use simpler output
- admit that the app is effectively unsupported

## Quality bar

Good outputs:
- make architecture decisions for the user
- identify the most probable failure points up front
- include specific checks after import and after first run

Bad outputs:
- ask the user to improvise the integration shape
- promise unverified share links
- omit the first-run verification step
