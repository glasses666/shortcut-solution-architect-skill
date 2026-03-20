# shortcut-solution-architect

A Codex skill for researching, designing, generating, validating, and distributing Apple Shortcuts solutions on macOS.

## What is included

- `skill/shortcut-solution-architect/`
  The installable skill source, including references, helper scripts, and templates.
- `dist/shortcut-solution-architect.skill`
  A packaged `.skill` artifact ready for distribution.
- `examples/`
  Example DeepResearch prompt output used while shaping the skill.

## Design principles

- Apple-native first
- local app inspection before web research
- transparent capability reporting
- quality gate aimed at a working result within three attempts
- Cherri supported as an advanced, optional generation route

## Typical use cases

- Decide whether a macOS app can be automated through Shortcuts
- Design a share-sheet bridge or file-bridge workflow
- Plan whether to return a shortcut spec, a `.shortcut` file, a download link, or an iCloud share link
- Produce a decision-complete shortcut implementation plan for ordinary agents and OpenClaw-style agents
