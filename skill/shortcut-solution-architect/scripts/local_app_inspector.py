#!/usr/bin/env python3
"""Inspect a local macOS app for shortcut-relevant capability evidence."""

from __future__ import annotations

import argparse
import json
import plistlib
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


COMMON_APP_DIRS = [
    Path("/Applications"),
    Path("/System/Applications"),
    Path.home() / "Applications",
]


def run(cmd: List[str]) -> Dict[str, object]:
    completed = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "ok": completed.returncode == 0,
        "code": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def normalize_name(name: str) -> str:
    return name.removesuffix(".app")


def find_app(name_or_path: str) -> Optional[Path]:
    raw = Path(name_or_path).expanduser()
    if raw.exists():
        return raw.resolve()

    candidate_name = name_or_path if name_or_path.endswith(".app") else f"{name_or_path}.app"
    for base in COMMON_APP_DIRS:
        candidate = base / candidate_name
        if candidate.exists():
            return candidate.resolve()
    mdfind_bin = shutil.which("mdfind")
    if mdfind_bin:
        result = run([mdfind_bin, f'kMDItemFSName == "{candidate_name}"'])
        if result["ok"] and result["stdout"]:
            for line in str(result["stdout"]).splitlines():
                path = Path(line.strip())
                if path.exists() and path.suffix == ".app":
                    return path.resolve()
    return None


def read_info_plist(app_path: Path) -> Dict[str, object]:
    plist_path = app_path / "Contents" / "Info.plist"
    if not plist_path.exists():
        return {}
    with plist_path.open("rb") as fh:
        return plistlib.load(fh)


def list_url_schemes(info: Dict[str, object]) -> List[str]:
    schemes: List[str] = []
    for entry in info.get("CFBundleURLTypes", []) or []:
        for scheme in entry.get("CFBundleURLSchemes", []) or []:
            schemes.append(str(scheme))
    return schemes


def list_document_types(info: Dict[str, object]) -> List[str]:
    results: List[str] = []
    for entry in info.get("CFBundleDocumentTypes", []) or []:
        name = entry.get("CFBundleTypeName")
        role = entry.get("CFBundleTypeRole")
        exts = entry.get("CFBundleTypeExtensions") or []
        item = ", ".join([x for x in [str(name) if name else "", f"role={role}" if role else ""] if x])
        if exts:
            item = f"{item} extensions={list(exts)}".strip()
        if item:
            results.append(item)
    return results


def list_extensions(app_path: Path) -> List[str]:
    plugins_dir = app_path / "Contents" / "PlugIns"
    if not plugins_dir.exists():
        return []
    return sorted(p.name for p in plugins_dir.iterdir())


def list_services(info: Dict[str, object]) -> List[str]:
    services = info.get("NSServices", []) or []
    results: List[str] = []
    for service in services:
        menu = service.get("NSMenuItem", {}) if isinstance(service, dict) else {}
        default = menu.get("default")
        message = service.get("NSMessage") if isinstance(service, dict) else None
        item = ", ".join(x for x in [str(default) if default else "", f"message={message}" if message else ""] if x)
        if item:
            results.append(item)
    return results


def share_extension_hints(app_path: Path) -> List[str]:
    plugins_dir = app_path / "Contents" / "PlugIns"
    if not plugins_dir.exists():
        return []
    hints: List[str] = []
    for appex in plugins_dir.glob("*.appex"):
        info = read_info_plist(appex)
        ext = info.get("NSExtension", {}) or {}
        point = ext.get("NSExtensionPointIdentifier")
        if point:
            hints.append(f"{appex.name}: {point}")
    return hints


def scriptability(app_path: Path) -> Dict[str, object]:
    sdef_bin = shutil.which("sdef")
    if not sdef_bin:
        return {"available": "unknown", "details": "sdef not available"}
    result = run([sdef_bin, str(app_path)])
    if result["ok"] and result["stdout"]:
        return {"available": "yes", "details": "sdef returned a scripting dictionary"}
    return {"available": "no", "details": result["stderr"] or "no scripting dictionary returned"}


def cli_candidates(app_path: Path, app_name: str, info: Dict[str, object]) -> Dict[str, object]:
    executable = info.get("CFBundleExecutable")
    bundle_exec = app_path / "Contents" / "MacOS" / str(executable) if executable else None
    which_name = normalize_name(app_name).lower().replace(" ", "")
    which_result = run(["which", which_name]) if which_name else {"ok": False, "stdout": "", "stderr": ""}
    return {
        "bundle_executable": str(bundle_exec) if bundle_exec and bundle_exec.exists() else None,
        "which_candidate": which_name,
        "which_result": which_result["stdout"] if which_result["ok"] else None,
    }


def classify_surface(info: Dict[str, object], url_schemes: List[str], scriptable: Dict[str, object], cli: Dict[str, object], share_hints: List[str]) -> Dict[str, str]:
    return {
        "url_scheme": "yes" if url_schemes else "no",
        "applescript_jxa": scriptable["available"],
        "cli_hint": "yes" if cli["bundle_executable"] or cli["which_result"] else "no",
        "share_extension_hint": "yes" if share_hints else "no",
        "document_type_hint": "yes" if (info.get("CFBundleDocumentTypes") or []) else "no",
    }


def build_report(app_path: Path) -> Dict[str, object]:
    info = read_info_plist(app_path)
    name = normalize_name(app_path.name)
    url_schemes = list_url_schemes(info)
    document_types = list_document_types(info)
    extensions = list_extensions(app_path)
    share_hints = share_extension_hints(app_path)
    services = list_services(info)
    scriptable = scriptability(app_path)
    cli = cli_candidates(app_path, name, info)

    return {
        "app_name": name,
        "app_path": str(app_path),
        "bundle_identifier": info.get("CFBundleIdentifier"),
        "version": info.get("CFBundleShortVersionString"),
        "url_schemes": url_schemes,
        "document_types": document_types,
        "plugins": extensions,
        "services": services,
        "share_extension_hints": share_hints,
        "scriptability": scriptable,
        "cli": cli,
        "surface_hints": classify_surface(info, url_schemes, scriptable, cli, share_hints),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True, help="App name like 'Buzz' or full path to .app")
    args = parser.parse_args()

    app_path = find_app(args.app)
    if app_path is None:
        print(json.dumps({"app": args.app, "installed": False, "error": "App not found locally"}, ensure_ascii=False, indent=2))
        return 1

    report = build_report(app_path)
    report["installed"] = True
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
