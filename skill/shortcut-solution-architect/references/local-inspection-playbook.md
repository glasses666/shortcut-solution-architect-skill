# Local Inspection Playbook

Use this before web research whenever the target app is on the current Mac.

Treat the app bundle as the primary source of truth. Stay read-only.

## Checklist

1. Detect install state and resolve the real bundle path.
2. Read `Contents/Info.plist`.
3. Check `CFBundleURLTypes` for custom URL schemes.
4. Check `CFBundleDocumentTypes` for import/open/export clues.
5. Inspect `Contents/PlugIns` and `Contents/Extensions` for `.appex`.
6. Read each extension's `NSExtensionPointIdentifier`.
7. Check `NSServices` for Services-menu or share-like hooks.
8. Run `sdef` to check AppleScript/JXA terminology.
9. Inspect the main executable and obvious CLI companions.
10. Use LaunchServices metadata only as supporting evidence.
11. Treat `com.apple.share-services` as strong share-sheet evidence.
12. Treat intent-related extensions as hints, then confirm at runtime if exact Shortcuts behavior matters.

## Useful local commands

Set:

```zsh
APP="/Applications/Example.app"
PLIST="$APP/Contents/Info.plist"
```

Bundle identity:

```zsh
test -d "$APP" && echo installed || echo missing
mdls -name kMDItemCFBundleIdentifier -name kMDItemVersion "$APP"
plutil -extract CFBundleIdentifier raw -o - "$PLIST"
plutil -extract CFBundleShortVersionString raw -o - "$PLIST" 2>/dev/null
plutil -extract CFBundleExecutable raw -o - "$PLIST"
```

URL schemes:

```zsh
plutil -extract CFBundleURLTypes json -o - "$PLIST" 2>/dev/null
```

Document types:

```zsh
plutil -extract CFBundleDocumentTypes json -o - "$PLIST" 2>/dev/null
```

Embedded extensions:

```zsh
find "$APP/Contents" \( -path '*/PlugIns/*.appex' -o -path '*/Extensions/*.appex' \) 2>/dev/null
```

Extension identifiers:

```zsh
find "$APP/Contents" -name '*.appex' -print0 2>/dev/null | while IFS= read -r -d '' x; do
  echo "== $x =="
  plutil -extract NSExtension.NSExtensionPointIdentifier raw -o - "$x/Contents/Info.plist" 2>/dev/null
done
```

Services hooks:

```zsh
plutil -extract NSServices json -o - "$PLIST" 2>/dev/null
```

AppleScript/JXA:

```zsh
sdef "$APP" | head -n 40
```

CLI hints:

```zsh
EXE="$(plutil -extract CFBundleExecutable raw -o - "$PLIST" 2>/dev/null)"
ls -l "$APP/Contents/MacOS/$EXE"
find "$APP/Contents/MacOS" -maxdepth 1 -type f 2>/dev/null
```

LaunchServices hints:

```zsh
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -dump | rg -i 'example|com\.example\.app'
```

## Interpretation rules

- `CFBundleURLTypes`: strong URL-bridge hint.
- `CFBundleDocumentTypes`: strong file-open/import/export hint.
- `.appex` with `com.apple.share-services`: strong share-sheet evidence.
- `NSServices`: useful Services-menu integration; sometimes bridgeable.
- `sdef` output: real AppleScript/JXA surface.
- main executable alone: weak CLI hint until arguments are verified.

## Practical reminder

There is no single local key that universally means “this app exposes Shortcuts actions.” Bundle inspection gives strong hints, not a complete runtime guarantee.
