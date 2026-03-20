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

## Recommended build discipline

1. Compile a minimal smoke test.
2. Add the real actions incrementally.
3. After each compile, inspect the actual generated file name.
4. Prefer stable variable shapes over clever interpolation.
5. Keep a manual fallback plan, but only after trying the generator path seriously.
