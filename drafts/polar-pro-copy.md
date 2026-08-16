# Polar Pro tier copy (draft — not published)

**Authored by a disclosed AI agent. Not legal advice. Do not publish this
from the agent. A human publishes later, after a GitHub machine account
exists and Polar review is actually submitted.**

Suggested price: **12 USD / month**.

## Product name

sellfit Pro

## One-liner

A policy-diff JSON feed plus a GitHub Action that fails CI when Polar,
Lemon Squeezy, Stripe, or Chrome Web Store (or GitHub) policy text
changes.

## What this is

Software we wrote and own. Instant digital fulfillment (license key or
private repo access to the feed + the Action). Not a directory. Not
donations, crowdfunding, or a sponsorship product. Not get-rich content.
Not outreach.

The MIT CLI stays free. Pro is the dated changelog of the cited policy
dataset: added / removed / changed rules (`rule_id`, `field`, `old`,
`new`) and a workflow that turns a nonempty diff into a red CI check.

## What ships in the repo today (unpublished)

- `python -m sellfit diff old.json new.json` — offline comparer
- `.github/workflows/policy-diff.yml` — runs that command on fixture
  snapshots; does **not** fetch live pages and needs no secrets
- `data/snapshots/README.md` — baseline pointer at `2026-08.json`

A human later enables a scheduled fetch of the official public URLs
already listed in the dataset. No API keys. The Action then diffs the
new snapshot against the last cut and fails when quotes or verdicts
move. A human still re-quotes. The feed is not legal advice.

## Checkout blurb (draft)

> sellfit Pro — 12 USD/month
>
> Written by a disclosed AI agent. Not legal advice.
>
> Software: a machine-readable policy-diff JSON feed and a GitHub
> Action that fails your CI when Polar, Lemon Squeezy, Stripe, or
> Chrome Web Store text changes. The MIT checker stays free.
>
> Not a policy directory. Not a tip jar. Re-check the official pages.
> We will refund if a dataset quote no longer appears on the cited URL
> and we have not shipped a fix within 14 days of you telling us.

## What not to claim

- "Guaranteed approval"
- "We talked to Polar"
- "Legal opinion"
- Anything that sounds like a lead-gen, outreach, or paid directory
- Donations or sponsorships (use GitHub Sponsors for optional tips)
