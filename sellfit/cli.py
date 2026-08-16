"""sellfit CLI: check, platforms, cite, diff. Offline. No network.

Authored by a disclosed AI agent. Not legal advice.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import textwrap

from sellfit import __version__
from sellfit.classify import (
    PLATFORMS,
    classify,
    platform_counts,
    rule_by_id,
)
from sellfit.diff import diff_files, format_human, load_policy_file

USAGE = """\
Authored by a disclosed AI agent. Not legal advice. Offline. No model.

usage:
  python -m sellfit check "one-line product idea" [--json]
  python -m sellfit platforms [--json]
  python -m sellfit cite polar-8 [--json]
  python -m sellfit diff old.json new.json [--out FILE]
"""

DISCLAIMER = "Authored by a disclosed AI agent. Not legal advice. Offline keyword match only."
PRO_WATCH_LINE = (
    "Pro watch (12 USD/mo): CI-fail when a cited platform's text changes — not for sale yet."
)


def _wrap(text: str, indent: str = "    ") -> str:
    return textwrap.fill(text, width=88, initial_indent=indent, subsequent_indent=indent)


def _dump_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _platform_json_row(row: dict) -> dict:
    rule = row.get("rule")
    out = {
        "verdict": row["verdict"],
        "rule_id": rule["rule_id"] if rule else None,
        "summary": (rule["summary"] if rule else None) or row.get("note"),
        "quote": rule["quote"] if rule else None,
        "source_url": rule["source_url"] if rule else None,
    }
    if row.get("note"):
        out["note"] = row["note"]
    if row.get("publish_account"):
        out["publish_account"] = row["publish_account"]
    return out


def _check_json_payload(result: dict) -> dict:
    return {
        "idea": result["idea"],
        "tags": result["tags"],
        "platforms": {name: _platform_json_row(row) for name, row in result["platforms"].items()},
        "exit_code": result["exit_code"],
        "disclaimer": result["disclaimer"],
        "dataset_version": result.get("dataset_version"),
    }


def cmd_check(idea: str, as_json: bool = False) -> int:
    idea = idea.strip()
    if not idea:
        print("error: empty product idea", file=sys.stderr)
        return 1
    result = classify(idea)
    if as_json:
        _dump_json(_check_json_payload(result))
        return result["exit_code"]
    print(f"sellfit {__version__}  dataset {result['dataset_version']}  OFFLINE")
    print(result["disclaimer"])
    print()
    print(f"idea: {result['idea']}")
    print(f"tags: {', '.join(result['tags']) or '(none)'}")
    print()
    width = max(len(p) for p in PLATFORMS)
    for platform in PLATFORMS:
        row = result["platforms"][platform]
        verdict = row["verdict"].upper()
        rule = row.get("rule")
        if row["verdict"] == "n/a" or rule is None:
            print(f"{platform:<{width}}  {verdict:<18}  —")
            print(_wrap(row.get("note") or "No product-fit rule for this platform."))
            pa = row.get("publish_account")
            if pa:
                print(_wrap(
                    f"publish-account: {pa['rule_id']} — {pa['summary']} "
                    "(who may register, not a product-hosting verdict)"
                ))
                if pa.get("source_url"):
                    print(_wrap(pa["source_url"]))
            print()
            continue
        print(f"{platform:<{width}}  {verdict:<18}  {rule['rule_id']}  {rule['category']}")
        print(_wrap(rule["summary"]))
        print(_wrap(f"quote: {rule['quote']}"))
        print(_wrap(rule["source_url"]))
        print()
    if result["exit_code"] == 2:
        print("overall: ALL product-fit platforms prohibited; n/a omitted (exit 2)")
    else:
        print("overall: at least one product-fit platform is allowed or restricted_review (exit 0)")
        print(PRO_WATCH_LINE)
    return result["exit_code"]


def cmd_platforms(as_json: bool = False) -> int:
    rows = platform_counts()
    if as_json:
        _dump_json({
            "platforms": rows,
            "disclaimer": DISCLAIMER,
        })
        return 0
    print(f"sellfit {__version__}  OFFLINE")
    print("Authored by a disclosed AI agent. Not legal advice.")
    print()
    for row in rows:
        print(
            f"{row['platform']:<8}  {row['rule_count']:>3} rules  "
            f"{row['source_url']}  ({row['effective_date']})"
        )
    return 0


def cmd_cite(rule_id: str, as_json: bool = False) -> int:
    rule = rule_by_id(rule_id)
    if rule is None:
        print(f"error: unknown rule_id {rule_id!r}", file=sys.stderr)
        return 1
    if as_json:
        _dump_json({
            "rule_id": rule["rule_id"],
            "platform": rule["platform"],
            "verdict": rule["verdict"],
            "category": rule["category"],
            "summary": rule["summary"],
            "source_url": rule["source_url"],
            "source_effective_date": rule["source_effective_date"],
            "last_checked": rule["last_checked"],
            "quote": rule["quote"],
            "disclaimer": DISCLAIMER,
        })
        return 0
    print(f"rule_id: {rule['rule_id']}")
    print(f"platform: {rule['platform']}")
    print(f"verdict: {rule['verdict']}")
    print(f"category: {rule['category']}")
    print(f"summary: {rule['summary']}")
    print(f"source_url: {rule['source_url']}")
    print(f"source_effective_date: {rule['source_effective_date']}")
    print(f"last_checked: {rule['last_checked']}")
    print(f"quote: {rule['quote']}")
    return 0


def cmd_diff(old: str, new: str, out: str | None, json_only: bool, fail_on_change: bool) -> int:
    try:
        old_data = load_policy_file(old)
        new_data = load_policy_file(new)
        records = diff_files(old, new)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    payload = json.dumps(records, indent=2, ensure_ascii=False)
    if not json_only:
        print(
            format_human(
                records,
                old_label=old,
                new_label=new,
                old_version=old_data.get("version"),
                new_version=new_data.get("version"),
                version=__version__,
            )
        )
        print()
    if out:
        Path(out).write_text(payload + "\n", encoding="utf-8")
        if not json_only:
            print(f"wrote {len(records)} change(s) to {out}")
    else:
        print(payload)
    if fail_on_change and records:
        return 3
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sellfit",
        description="Offline classifier of digital-product ideas against 2026 merchant/store policies. Authored by a disclosed AI agent. Not legal advice.",
    )
    parser.add_argument("--version", action="version", version=f"sellfit {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="classify a one-line product idea")
    p_check.add_argument("idea", help="one-line product idea")
    p_check.add_argument("--json", action="store_true", help="print one JSON object to stdout")

    p_platforms = sub.add_parser("platforms", help="list platforms and rule counts")
    p_platforms.add_argument("--json", action="store_true", help="print one JSON object to stdout")

    p_cite = sub.add_parser("cite", help="print one rule, quote, and URL")
    p_cite.add_argument("rule_id", help="rule id such as polar-8")
    p_cite.add_argument("--json", action="store_true", help="print one JSON object to stdout")

    p_diff = sub.add_parser("diff", help="compare two policy JSON files (offline)")
    p_diff.add_argument("old", help="older policy JSON path")
    p_diff.add_argument("new", help="newer policy JSON path")
    p_diff.add_argument("--out", help="write JSON diff to this file (else stdout)")
    p_diff.add_argument("--json-only", action="store_true", help="print only the JSON list")
    p_diff.add_argument(
        "--fail-on-change",
        action="store_true",
        help="exit 3 when the diff is nonempty (CI gate for later Pro fetch)",
    )

    args = parser.parse_args(argv)
    if args.command is None:
        print(USAGE, file=sys.stderr)
        return 1
    if args.command == "check":
        return cmd_check(args.idea, as_json=args.json)
    if args.command == "platforms":
        return cmd_platforms(as_json=args.json)
    if args.command == "cite":
        return cmd_cite(args.rule_id, as_json=args.json)
    if args.command == "diff":
        return cmd_diff(args.old, args.new, args.out, args.json_only, args.fail_on_change)
    print(USAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
