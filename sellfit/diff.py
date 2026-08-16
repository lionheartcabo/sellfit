"""Compare two sellfit policy JSON files. Offline. No network.

Authored by a disclosed AI agent. Not legal advice.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Identity is rule_id. last_checked is a re-check stamp, not policy text,
# but it is still reported when it changes so a feed can see freshness.
COMPARE_SKIP = frozenset({"rule_id"})


def load_policy_file(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"policy file missing: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "rules" not in data:
        raise ValueError(f"not a sellfit policy JSON (missing rules): {p}")
    return data


def _index(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rule in data.get("rules") or []:
        rid = rule.get("rule_id")
        if not rid:
            continue
        out[str(rid)] = rule
    return out


def _fields(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    keys = set(old) | set(new)
    keys -= COMPARE_SKIP
    return sorted(keys)


def _values_equal(a: Any, b: Any) -> bool:
    return a == b


def diff_datasets(old: dict[str, Any], new: dict[str, Any]) -> list[dict[str, Any]]:
    """Return added / removed / changed records.

    Each record: rule_id, field, old, new, plus op for readers.
    Added/removed use field=None and carry the whole rule.
    Changed emits one record per field.
    """
    old_idx = _index(old)
    new_idx = _index(new)
    records: list[dict[str, Any]] = []

    for rid in sorted(set(old_idx) - set(new_idx)):
        records.append(
            {
                "op": "removed",
                "rule_id": rid,
                "field": None,
                "old": old_idx[rid],
                "new": None,
            }
        )

    for rid in sorted(set(new_idx) - set(old_idx)):
        records.append(
            {
                "op": "added",
                "rule_id": rid,
                "field": None,
                "old": None,
                "new": new_idx[rid],
            }
        )

    for rid in sorted(set(old_idx) & set(new_idx)):
        left, right = old_idx[rid], new_idx[rid]
        for field in _fields(left, right):
            ov, nv = left.get(field), right.get(field)
            if not _values_equal(ov, nv):
                records.append(
                    {
                        "op": "changed",
                        "rule_id": rid,
                        "field": field,
                        "old": ov,
                        "new": nv,
                    }
                )

    order = {"removed": 0, "added": 1, "changed": 2}
    records.sort(key=lambda r: (order[r["op"]], r["rule_id"], r["field"] or ""))
    return records


def diff_files(old_path: str | Path, new_path: str | Path) -> list[dict[str, Any]]:
    return diff_datasets(load_policy_file(old_path), load_policy_file(new_path))


def summarize(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"added": 0, "removed": 0, "changed": 0}
    for rec in records:
        counts[rec["op"]] = counts.get(rec["op"], 0) + 1
    return counts


def format_human(
    records: list[dict[str, Any]],
    *,
    old_label: str,
    new_label: str,
    old_version: str | None = None,
    new_version: str | None = None,
    version: str = "",
) -> str:
    counts = summarize(records)
    n = len(records)
    lines = [
        f"sellfit {version}  policy-diff  OFFLINE".strip(),
        "Authored by a disclosed AI agent. Not legal advice.",
        "",
        f"old: {old_label}" + (f"  ({old_version})" if old_version else ""),
        f"new: {new_label}" + (f"  ({new_version})" if new_version else ""),
        (
            f"{n} change(s): {counts['added']} added, "
            f"{counts['removed']} removed, {counts['changed']} changed"
        ),
    ]
    if not records:
        lines.append("")
        lines.append("identical policy files")
        return "\n".join(lines)

    lines.append("")
    for rec in records:
        rid = rec["rule_id"]
        if rec["op"] == "added":
            lines.append(f"  + added    {rid}")
        elif rec["op"] == "removed":
            lines.append(f"  - removed  {rid}")
        else:
            lines.append(f"  ~ changed  {rid}.{rec['field']}")
            lines.append(f"      old: {rec['old']!r}")
            lines.append(f"      new: {rec['new']!r}")
    return "\n".join(lines)
