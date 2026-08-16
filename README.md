# sellfit

**This software was authored by a disclosed AI agent.** It is not legal
advice. A keyword matcher is not a lawyer, a reviewer, or a guarantee of
approval. Policies change; re-check the official pages before you rely on
any verdict.

Offline MIT CLI plus a versioned JSON policy dataset. It classifies a
one-line digital-product idea against 2026 Polar, Lemon Squeezy, Stripe,
Chrome Web Store, and GitHub rules. No model at runtime. No network.

## Usage

From this directory (Python 3.10+, stdlib only):

```bash
python -m unittest discover -s tests -v
python -m sellfit check "MIT-licensed CLI that checks Polar AUP"
python -m sellfit check "cold email SaaS"
python -m sellfit platforms
python -m sellfit cite polar-8
python -m sellfit diff data/policies/2026-08.json data/policies/2026-08.json
```

- `check` maps the idea to tags, then reports the **worst** matching
  verdict per platform and the citing rule (quote + URL).
- Chrome Web Store is `n/a` unless the idea is an extension, theme, or
  add-on. GitHub is `n/a` unless a product-hosting rule matches (the
  dataset's account-creation rules are a publish-account note, not an
  allowed default).
- Exit `0` if any **product-fit** platform is `allowed` or `restricted_review`.
- Exit `2` if every product-fit platform is `prohibited` (`n/a` omitted).
- Exit `1` on usage errors (missing command, unknown `rule_id`).

`restricted_review` means the fetched page says the category needs closer
review or extra due diligence, not that it is approved.

## For AI agents

From this directory (offline, stdlib only):

```bash
python -m sellfit check "one-line product idea" --json
python -m sellfit platforms --json
python -m sellfit cite polar-8 --json
```

`--json` prints one JSON object to stdout and nothing else. `check` fields:
`idea`, `tags`, `platforms` (each with `verdict`, `rule_id`, `summary`,
`quote`, `source_url`), `exit_code`, `disclaimer`. Omit `--json` for the
human text default. This is not legal advice. Authored by a disclosed AI
agent. A keyword matcher is not a lawyer.

See `AGENTS.md` for a 15-line agent brief.

## How to re-check sources

1. Open every URL in `data/policies/2026-08.json` (`source_url` on each rule).
2. Confirm the `quote` still appears verbatim. If a page moved, search the
   official domain and replace the URL; do not invent quotes.
3. Set `last_checked` to today. If the page prints an effective or last-
   updated date, copy that into `source_effective_date`.
4. Bump the dataset filename/version when the rules change (`2026-09.json`).
5. Run `python -m unittest`. Stay offline at runtime.

Primary pages fetched 2026-08-16:

| Platform | URL | Date on page |
|---|---|---|
| Polar AUP | https://polar.sh/legal/acceptable-use-policy | Effective Date — March 25, 2026 |
| Polar account reviews | https://polar.sh/docs/merchant-of-record/account-reviews | (none; used last_checked) |
| Lemon Squeezy | https://docs.lemonsqueezy.com/help/getting-started/prohibited-products | (none; used last_checked) |
| Stripe | https://stripe.com/legal/restricted-businesses | Last updated: 2026-05-13 |
| Chrome Web Store | https://developer.chrome.com/docs/webstore/program-policies/policies | (none; used last_checked) |
| CWS trader FAQ | https://developer.chrome.com/docs/webstore/program-policies/trader-verification-faq | (none; used last_checked) |
| GitHub ToS | https://docs.github.com/en/site-policy/github-terms/github-terms-of-service | Effective date: April 27, 2026 |

**Substitution:** `https://docs.stripe.com/restricted-businesses` returned
404. The current official list is `https://stripe.com/legal/restricted-businesses`
(also at `https://stripe.com/restricted-businesses`). Polar sits on Stripe,
so Stripe categories are included.

## How a human would publish later

Do **not** do this from the agent. GitHub Terms (27 April 2026) say a
**human** must create the Account. Bots may not self-register. A human may
then create one free machine account for automated tasks.

Suggested later steps for a human, not done here:

1. Human creates a GitHub account (and optional machine account).
2. Push this tree. Enable GitHub Pages on `docs/` if you want the dataset viewer.
3. Polar: build first, submit second. Complete merchant review before the
   first payout. Polar prohibits donations and sponsorship products; use
   GitHub Sponsors for optional tips, not Polar.
4. Optional later Pro tier copy lives in `drafts/polar-pro-copy.md` and is
   **not published**.

Step-by-step for a human: `PUBLISH.md`.

See `AI-AUTHORSHIP.md` and `NOTICE`.

## Layout

```
sellfit/                 CLI package (python -m sellfit)
data/policies/           versioned JSON rules
data/snapshots/          baseline pointer (no duplicate JSON)
.github/workflows/       offline policy-diff Action (unpublished Pro)
tests/                   unittest + fixtures
docs/                    static dataset viewer
drafts/                  unpublished notes and Pro copy
AGENTS.md               15-line brief for calling agents
```

## Pro (not published)

A later paid SKU — **not listed on Polar**, no checkout, no accounts.

`python -m sellfit diff old.json new.json` compares two policy JSON
files offline and prints added / removed / changed rules (`rule_id`,
`field`, `old`, `new`). JSON goes to stdout or `--out`.

The GitHub Action `.github/workflows/policy-diff.yml` runs that command
on `tests/fixtures/snapshots/` so CI proves the diff works. It does
**not** fetch live Polar / Lemon / Stripe / CWS pages and needs no
secrets. Comments in the workflow explain how a human would later
schedule a public-page fetch and `--fail-on-change`.

Draft Polar copy (software we own, 12 USD/mo, AI-disclosed, not a
directory, not donations): `drafts/polar-pro-copy.md`.

## License

MIT. Policy quotes remain the publishers'. See `LICENSE` and `NOTICE`.
