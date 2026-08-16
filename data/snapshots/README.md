# Policy snapshots

**Authored by a disclosed AI agent. Not legal advice.**

The current baseline is the dated dataset, not a second copy of the
same file:

- Baseline (2026-08): [`../policies/2026-08.json`](../policies/2026-08.json)

Do not duplicate that JSON here. When a later cut exists
(`2026-09.json`), keep this pointer on the previous cut so

```bash
python -m sellfit diff data/policies/2026-08.json data/policies/2026-09.json
```

is the offline changelog.

CI proves the comparer with the tiny fixtures in
`tests/fixtures/snapshots/` (not this folder). Those fixtures are
synthetic and are not official policy text.

A human can later schedule a fetch of the official `source_url` pages
and write a new dated JSON. That fetch is **not** the default GitHub
Action: public pages need no secrets, but the Action must not hit the
network until a human turns that on. See
`.github/workflows/policy-diff.yml`.
