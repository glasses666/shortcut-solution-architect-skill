# Cherri Advanced Path

Use this reference only when a code-first generation route is materially helpful.

## What Cherri is

Cherri is a code-first shortcut generation path. Treat it as a compiler/DSL workflow for Apple Shortcuts, not as the default way to build ordinary macOS automations.

## When to choose Cherri

Choose Cherri when at least one of these is true:

- the user explicitly wants shortcut generation from code
- the user wants repeatable shortcut artifacts, not just one manual build
- the deliverable requires a `.shortcut` file and a manual step-by-step build is too expensive
- the shortcut needs to be regenerated across machines or projects from a stable spec

## When not to choose Cherri

Do not choose Cherri when:

- Apple-native Shortcuts actions already solve the problem cleanly
- a share-sheet bridge or file bridge is simpler and more portable
- the user only needs one working shortcut and does not need a generator pipeline
- the current environment cannot support the extra tooling

## How to position Cherri in the answer

If Cherri is recommended:

- say it is an advanced, code-driven route
- explain why it beats manual editing for this case
- list the extra dependency cost
- keep Apple-native runtime behavior as the primary target
- include a native fallback plan

## Artifact policy with Cherri

Typical Cherri output stack:

- shortcut spec/DSL
- generated shortcut payload
- optional signed `.shortcut` file
- optional download link

Do not promise an iCloud share link just because Cherri is available.

## Confidence guidance

- `High`: Cherri is available, the request explicitly wants code generation, and file artifacts are required
- `Medium`: Cherri would help, but the environment does not yet prove it is installed
- `Low`: the task is simple and Apple-native approaches are already enough
