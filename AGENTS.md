# sellfit — for AI agents

Offline keyword classifier of a one-line digital-product idea against 2026 Polar, Lemon Squeezy, Stripe, Chrome Web Store, and GitHub policies. No network. No model.

One command (from this directory, Python 3.10+):

    python -m sellfit check "your idea" --json

`--json` prints one JSON object to stdout: idea, tags, platforms (verdict, rule_id, summary, quote, source_url), exit_code, disclaimer. No extra prose.

Also: `python -m sellfit platforms --json` and `python -m sellfit cite polar-8 --json`.

Exit 0 = at least one product-fit platform is allowed or restricted_review. Exit 2 = every product-fit platform is prohibited (n/a omitted). Exit 1 = usage error.

Do not treat this as legal advice. Authored by a disclosed AI agent. Keyword match only. Policies change; re-check the official source_url. Human text is the default (omit --json).
