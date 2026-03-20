#!/usr/bin/env python3
"""Build a structured capability matrix for a macOS app shortcut integration."""

from __future__ import annotations

import argparse
import json
from typing import Dict, List


STATE_VALUES = ("yes", "no", "unknown")


def classify(capabilities: Dict[str, str]) -> str:
    if capabilities["native_shortcut"] == "yes":
        return "Native Shortcut-capable"
    if capabilities["share_sheet"] == "yes":
        return "Share-sheet bridge"
    if any(capabilities[key] == "yes" for key in ("cli", "url_scheme", "applescript_jxa")):
        return "CLI/URL bridge"
    if capabilities["gui_automation"] == "yes":
        return "UI automation only"
    if all(capabilities[key] == "no" for key in capabilities):
        return "Unsupported"
    return "Needs research"


def confidence(capabilities: Dict[str, str], classification: str) -> str:
    if classification in {"Native Shortcut-capable", "Share-sheet bridge", "CLI/URL bridge"}:
        return "high" if "unknown" not in capabilities.values() else "medium"
    if classification == "UI automation only":
        return "medium" if capabilities["gui_automation"] == "yes" else "low"
    if classification == "Unsupported":
        return "medium" if "unknown" not in capabilities.values() else "low"
    return "low"


def evidence_needed(capabilities: Dict[str, str]) -> List[str]:
    prompts = {
        "native_shortcut": "Confirm whether the app exposes native Shortcuts actions.",
        "share_sheet": "Confirm whether the app appears in the macOS share sheet and accepts file/media input.",
        "cli": "Confirm whether the app ships a stable CLI or documented binary entrypoint.",
        "url_scheme": "Confirm whether the app exposes a documented URL scheme or x-callback-url entrypoint.",
        "applescript_jxa": "Confirm whether the app exposes AppleScript/JXA scripting that is not UI automation.",
        "gui_automation": "Confirm whether GUI automation is possible and acceptable for this workflow.",
    }
    return [prompts[key] for key, value in capabilities.items() if value == "unknown"]


def recommended_path(classification: str) -> str:
    mapping = {
        "Native Shortcut-capable": "Build the shortcut directly with Apple-native actions.",
        "Share-sheet bridge": "Use share-sheet input, optional media encoding, then bridge via files/folders.",
        "CLI/URL bridge": "Use a documented CLI, URL scheme, or AppleScript/JXA bridge instead of GUI automation.",
        "UI automation only": "Use UI automation only as a last resort and label it brittle.",
        "Unsupported": "Do not promise a working shortcut; return a transparent blocker report.",
        "Needs research": "Research missing automation surfaces before committing to a build path.",
    }
    return mapping[classification]


def build_report(args: argparse.Namespace) -> Dict[str, object]:
    capabilities = {
        "native_shortcut": args.native_shortcut,
        "share_sheet": args.share_sheet,
        "cli": args.cli,
        "url_scheme": args.url_scheme,
        "applescript_jxa": args.applescript_jxa,
        "gui_automation": args.gui_automation,
    }
    result = classify(capabilities)
    return {
        "app": args.app,
        "task": args.task,
        "platform": args.platform,
        "installed": args.installed,
        "capabilities": capabilities,
        "classification": result,
        "confidence": confidence(capabilities, result),
        "evidence_needed": evidence_needed(capabilities),
        "recommended_build_path_hint": recommended_path(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--platform", default="macOS")
    parser.add_argument("--installed", choices=STATE_VALUES, default="unknown")
    parser.add_argument("--native-shortcut", dest="native_shortcut", choices=STATE_VALUES, default="unknown")
    parser.add_argument("--share-sheet", dest="share_sheet", choices=STATE_VALUES, default="unknown")
    parser.add_argument("--cli", choices=STATE_VALUES, default="unknown")
    parser.add_argument("--url-scheme", dest="url_scheme", choices=STATE_VALUES, default="unknown")
    parser.add_argument("--applescript-jxa", dest="applescript_jxa", choices=STATE_VALUES, default="unknown")
    parser.add_argument("--gui-automation", dest="gui_automation", choices=STATE_VALUES, default="unknown")
    args = parser.parse_args()

    report = build_report(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
