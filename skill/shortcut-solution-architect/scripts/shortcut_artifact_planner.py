#!/usr/bin/env python3
"""Plan shortcut artifacts from classification, deliverable goals, and environment constraints."""

from __future__ import annotations

import argparse
import json
from typing import Dict, List


CLASSIFICATIONS = (
    "Native Shortcut-capable",
    "Share-sheet bridge",
    "CLI/URL bridge",
    "UI automation only",
    "Unsupported",
    "Needs research",
)

GENERATORS = ("none", "cherri", "custom")


def choose_build_path(args: argparse.Namespace) -> str:
    if args.generator_backend == "cherri" and args.deliverable in {"file", "all", "link"}:
        return "Cherri-generated shortcut artifact"
    if args.classification in {"Native Shortcut-capable", "Share-sheet bridge"}:
        return "Apple-native shortcut design"
    if args.classification == "CLI/URL bridge":
        return "Apple-native shell/url bridge"
    if args.classification == "UI automation only":
        return "GUI automation fallback"
    if args.classification == "Unsupported":
        return "Transparent blocker report"
    if args.generator_available == "yes":
        return "Generated shortcut artifact"
    return "Research before generation"


def artifact_list(args: argparse.Namespace) -> List[str]:
    artifacts = ["implementation-plan"]
    if args.deliverable in {"plan", "all"}:
        artifacts.append("quality-gate")
    wants_file = args.deliverable in {"file", "all"}
    wants_link = args.deliverable in {"link", "all"}

    if wants_file:
        if args.generator_available == "yes":
            artifacts.extend(["shortcut-spec", ".shortcut-file"])
            if args.generator_backend == "cherri":
                artifacts.append("cherri-source")
        else:
            artifacts.append("shortcut-spec")

    if wants_link:
        if args.generator_available == "yes":
            artifacts.append("download-link")
        else:
            artifacts.append("download-link-blocked")
        if args.distribution in {"icloud", "both"}:
            artifacts.append("icloud-link" if args.icloud_publisher == "yes" else "icloud-link-blocked")

    return artifacts


def blockers(args: argparse.Namespace) -> List[str]:
    issues = []
    if args.classification in {"Unsupported", "Needs research"}:
        issues.append("No reliable shortcut build path is verified yet.")
    if args.deliverable in {"file", "all", "link"} and args.generator_available == "no":
        issues.append("No shortcut generator or payload compiler is available in the current path.")
    if args.deliverable in {"link", "all"} and args.distribution in {"icloud", "both"} and args.icloud_publisher == "no":
        issues.append("No Apple-account-backed iCloud share publish step is available.")
    if args.classification == "UI automation only":
        issues.append("The solution depends on brittle GUI automation and should not be the default route.")
    return issues


def defaults_for_path(build_path: str) -> Dict[str, str]:
    if build_path == "Apple-native shortcut design":
        return {
            "primary_route": "Use official Shortcuts actions, share sheet, file bridges, and app-native entrypoints.",
            "fallback_route": "If a file artifact is required, produce a shortcut spec and optionally compile/sign later.",
        }
    if build_path == "Apple-native shell/url bridge":
        return {
            "primary_route": "Use a documented CLI, URL scheme, or AppleScript/JXA bridge.",
            "fallback_route": "Downgrade to a file bridge if the CLI or URL path proves stateful or fragile.",
        }
    if build_path == "GUI automation fallback":
        return {
            "primary_route": "Use UI automation only with explicit brittleness warnings.",
            "fallback_route": "Return a manual workflow if permissions or layout stability are poor.",
        }
    if build_path == "Generated shortcut artifact":
        return {
            "primary_route": "Generate a shortcut payload/spec, sign if needed, then distribute as a file.",
            "fallback_route": "Return the unsigned spec plus import instructions if signing or sharing fails.",
        }
    if build_path == "Cherri-generated shortcut artifact":
        return {
            "primary_route": "Generate shortcut source/spec with Cherri, compile it, then sign/distribute if needed.",
            "fallback_route": "Fall back to a native manual shortcut design or unsigned spec if the Cherri toolchain is unavailable.",
        }
    return {
        "primary_route": "Return a transparent research or blocker report.",
        "fallback_route": "Recommend a smaller Apple-native proof-of-concept if one exists.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classification", choices=CLASSIFICATIONS, required=True)
    parser.add_argument("--deliverable", choices=("plan", "file", "link", "all"), default="all")
    parser.add_argument("--distribution", choices=("download", "icloud", "both"), default="both")
    parser.add_argument("--generator-available", choices=("yes", "no"), default="no")
    parser.add_argument("--generator-backend", choices=GENERATORS, default="none")
    parser.add_argument("--icloud-publisher", choices=("yes", "no"), default="no")
    parser.add_argument("--portable", choices=("yes", "no"), default="yes")
    args = parser.parse_args()

    build_path = choose_build_path(args)
    result = {
        "classification": args.classification,
        "deliverable": args.deliverable,
        "distribution": args.distribution,
        "portable_default": args.portable,
        "build_path": build_path,
        "artifacts": artifact_list(args),
        "blockers": blockers(args),
    }
    result.update(defaults_for_path(build_path))

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
