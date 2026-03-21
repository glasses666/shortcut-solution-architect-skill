# Cherri Pitfalls From Real Builds

Use this file when you are actually generating `.shortcut` artifacts with Cherri, especially on macOS.

## Practical lessons

### 1. Treat Cherri as a real compiler, not just a serializer

- Expect parser and type-system edge cases.
- Validate the pipeline with a tiny smoke-test shortcut first.
- A minimal "show notification" shortcut is a good first compile before building the real workflow.

### 2. Output filename behavior can surprise you

- Cherri may honor the shortcut title for the produced file name instead of the source file stem.
- Do not assume `-o some-name.shortcut` means the final artifact will always use that exact base name.
- After compilation, inspect the output directory and report the actual generated file path.

### 3. Action results and conditions can be type-fragile

- Some action outputs do not behave like plain text or numbers in conditionals until explicitly normalized.
- A safer pattern is:
  - capture the action result
  - convert it with a dedicated action such as `getText(...)`
  - if needed, seed a variable with an empty literal of the target shape before assigning the action result
- Do not assume action outputs can always be used directly in `if ... contains` or numeric comparisons.

### 4. Inline variable interpolation is not equally stable for all value sources

- Inline references that look reasonable may still fail when the underlying value comes from an action result or transformed object.
- Prefer simple constants for path fragments and filenames when possible.
- If interpolation fails, reduce complexity:
  - use fewer nested conversions
  - avoid inline property access inside string interpolation
  - materialize values first

### 5. Reuse of constants across sibling branches can fail

- Cherri may reject redefinition of the same `const` name in separate branches.
- For branch-local temporary values that repeat, prefer mutable variables.

### 6. Warnings about default arguments are usually harmless

- Cherri warns when you pass a default value explicitly, such as `/bin/zsh` or `"Normal"`.
- These warnings do not necessarily indicate a broken shortcut.
- Distinguish "warning noise" from real compile blockers.

### 7. When the DSL fights you, simplify the user-visible behavior first

- If dynamic notifications or branch-specific counts trigger compiler instability, prefer a simpler, stable notification over a clever but fragile one.
- The first goal is a working importable `.shortcut`, not maximal elegance in the source.

### 8. Artifact handoff matters as much as compilation

- A technically correct `.shortcut` hidden in a deep build directory still feels broken to the user.
- After generation, copy the final `.shortcut` and any required helper files to an easy-open location or provide a real download link.
- Report the final user-facing handoff path, not only the compiler working directory.

### 9. Failure UX should favor alerts over notifications

- Notifications are easy to miss or can collapse in Notification Center.
- For conversion, import, or bridge tasks where the user needs the exact reason something failed, prefer a blocking `display alert` style message with a short summary and the first useful error details.
- Keep notifications for success or background progress hints, not for critical failure diagnosis.

### 10. Hierarchical menus reduce wrong-format mistakes

- When a shortcut offers many output formats, do not flatten everything into a single long menu.
- Prefer a two-step structure such as:
  - conversion type
  - target format
- This reduces misclicks and makes the workflow easier to scan, especially in share sheet or Quick Action contexts.

### 11. Preserve output naming expectations

- For file conversion shortcuts, users usually expect the original base filename to survive.
- Change the extension, not the stem, unless the user explicitly asked for timestamps, suffixes, or collision labels.
- If collisions are possible, append a minimal numeric suffix instead of overwriting silently.

### 12. External shell scripts are a deployment surface, not just an implementation detail

- A generated shortcut that calls a sidecar shell script can fail even when the script works perfectly in Terminal.
- Do not assume a script living in `Documents` or another user folder will be readable from `Run Shell Script` in the same way it is from an interactive shell.
- Prefer one of these in order:
  - inline shell for small logic
  - a controlled handoff location that Shortcuts can read reliably
  - a clearly documented sidecar deployment step
- If you ship a sidecar script, verify the runtime path from inside the actual shortcut, not only from Terminal.

### 13. Shortcuts shell environments are narrower than Terminal environments

- Do not assume Homebrew tools are on `PATH` when a shortcut runs.
- Resolve critical binaries explicitly, for example with absolute paths or a small lookup table.
- Validate behavior under a reduced environment, not only in your interactive shell.

### 14. Shortcut input shape can differ from the Finder item the user thinks they clicked

- Share sheet and Quick Action inputs may arrive as temporary files, renamed files, or file wrappers.
- Do not rely on the visible filename alone for type detection or error messaging.
- Prefer layered detection:
  - media stream inspection when possible
  - Spotlight metadata
  - extension fallback
- When diagnosing failures, include the received path and detected type in the error detail.

### 15. Detection order matters for media conversion shortcuts

- `ffprobe` can report a still image as a `video` stream.
- For image conversion shortcuts, do not let stream inspection override a clear `public.image` classification from Spotlight metadata.
- A safer order is:
  - `mdls` image classification first
  - then stream inspection for audio/video separation
  - then extension fallback
- Verify at least one real image input and one real video input before shipping.

### 16. AppleScript alert bodies do not interpret literal `\\n` automatically

- If you concatenate shell strings with literal backslash-n sequences, the alert may show `\\n` instead of line breaks.
- Build multiline strings with real newline characters before passing them to AppleScript.
- Verify one real failure path so the user-facing error dialog is readable, not just technically present.

### 17. Success feedback matters too

- A shortcut that silently opens Finder can still feel unfinished or ambiguous to the user.
- For longer conversions, add a clear success notification or another lightweight completion signal.
- Prefer:
  - blocking alerts for failure
  - lightweight notifications for success

### 18. Default transcoding presets should match the user's likely intent

- A technically valid transcode can still feel broken if the output is dramatically larger than the input.
- Do not use heavy mezzanine codecs such as ProRes as the default for everyday "convert to MOV" unless the user explicitly asked for edit-grade output.
- For casual or mixed-use conversion shortcuts, default to balanced presets first and expose heavier delivery presets as explicit options.

## Recommended build discipline

1. Compile a minimal smoke test.
2. Add the real actions incrementally.
3. After each compile, inspect the actual generated file name.
4. Prefer stable variable shapes over clever interpolation.
5. Keep a manual fallback plan, but only after trying the generator path seriously.
6. Make the final handoff easy to open and easy to debug for the user, not only for the generator author.
7. Verify the real runtime environment of shortcut-invoked shell code, not just the code path in Terminal.
8. Test one real image case, one real audio case, and one real video case before calling a media shortcut ready.
