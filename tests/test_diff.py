"""Offline tests for sellfit policy diff. Authored by a disclosed AI agent."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOTS = Path(__file__).resolve().parent / "fixtures" / "snapshots"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sellfit.diff import diff_datasets, diff_files  # noqa: E402


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sellfit", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def _tiny(rules: list[dict]) -> dict:
    return {
        "dataset": "sellfit-policies-fixture",
        "version": "test",
        "rules": rules,
    }


RULE_A = {
    "platform": "polar",
    "rule_id": "polar-8",
    "verdict": "prohibited",
    "category": "outreach",
    "summary": "Outreach is prohibited.",
    "source_url": "https://polar.sh/legal/acceptable-use-policy",
    "source_effective_date": "2026-03-25",
    "last_checked": "2026-08-16",
    "quote": "Advertising and unsolicited marketing services;",
    "tags": ["outreach"],
}

RULE_B = {
    "platform": "lemon",
    "rule_id": "lemon-donations",
    "verdict": "prohibited",
    "category": "donations",
    "summary": "Donations are prohibited.",
    "source_url": "https://docs.lemonsqueezy.com/help/getting-started/prohibited-products",
    "source_effective_date": "2026-08-16",
    "last_checked": "2026-08-16",
    "quote": "Donations or charity giving where no product exists",
    "tags": ["donations"],
}


class DiffLogicTests(unittest.TestCase):
    def test_identical_files_empty_diff(self):
        data = _tiny([RULE_A, RULE_B])
        self.assertEqual(diff_datasets(data, data), [])

    def test_identical_fixture_files_empty_diff(self):
        self.assertEqual(diff_files(SNAPSHOTS / "a.json", SNAPSHOTS / "a.json"), [])

    def test_one_quote_change(self):
        old = _tiny([RULE_A])
        changed = dict(RULE_A)
        changed["quote"] = "Advertising and unsolicited marketing services, including lead generation;"
        new = _tiny([changed])
        records = diff_datasets(old, new)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["op"], "changed")
        self.assertEqual(rec["rule_id"], "polar-8")
        self.assertEqual(rec["field"], "quote")
        self.assertEqual(rec["old"], RULE_A["quote"])
        self.assertEqual(rec["new"], changed["quote"])

    def test_added_rule(self):
        old = _tiny([RULE_A])
        new = _tiny([RULE_A, RULE_B])
        records = diff_datasets(old, new)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["op"], "added")
        self.assertEqual(rec["rule_id"], "lemon-donations")
        self.assertIsNone(rec["field"])
        self.assertIsNone(rec["old"])
        self.assertEqual(rec["new"]["rule_id"], "lemon-donations")

    def test_removed_rule(self):
        old = _tiny([RULE_A, RULE_B])
        new = _tiny([RULE_A])
        records = diff_datasets(old, new)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertEqual(rec["op"], "removed")
        self.assertEqual(rec["rule_id"], "lemon-donations")
        self.assertIsNone(rec["field"])
        self.assertIsNone(rec["new"])
        self.assertEqual(rec["old"]["rule_id"], "lemon-donations")


class DiffCliTests(unittest.TestCase):
    def test_cli_fixture_snapshots(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "diff.json"
            proc = _run(
                "diff",
                str(SNAPSHOTS / "a.json"),
                str(SNAPSHOTS / "b.json"),
                "--out",
                str(out),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("policy-diff", proc.stdout)
            self.assertIn("added", proc.stdout)
            self.assertIn("removed", proc.stdout)
            self.assertIn("changed", proc.stdout)
            records = json.loads(out.read_text(encoding="utf-8"))
            ops = {r["op"] for r in records}
            self.assertIn("added", ops)
            self.assertIn("removed", ops)
            self.assertIn("changed", ops)
            quote_changes = [
                r for r in records if r["op"] == "changed" and r["field"] == "quote"
            ]
            self.assertEqual(len(quote_changes), 1)
            self.assertEqual(quote_changes[0]["rule_id"], "polar-8")

    def test_cli_identical_empty_json(self):
        proc = _run(
            "diff",
            str(SNAPSHOTS / "a.json"),
            str(SNAPSHOTS / "a.json"),
            "--json-only",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), [])

    def test_cli_fail_on_change(self):
        proc = _run(
            "diff",
            str(SNAPSHOTS / "a.json"),
            str(SNAPSHOTS / "b.json"),
            "--json-only",
            "--fail-on-change",
        )
        self.assertEqual(proc.returncode, 3)

    def test_cli_missing_file_exit_1(self):
        proc = _run("diff", str(SNAPSHOTS / "a.json"), str(SNAPSHOTS / "nope.json"))
        self.assertEqual(proc.returncode, 1)

    def test_no_network_in_diff(self):
        src = (ROOT / "sellfit" / "diff.py").read_text(encoding="utf-8")
        for banned in ("urllib", "requests", "httpx", "socket", "http.client"):
            self.assertNotIn(banned, src)


if __name__ == "__main__":
    unittest.main()
