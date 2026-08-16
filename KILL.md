# KILL.md — sellfit 30-day cover-cost rule

**User:** David Lyne
**Set:** 16 August 2026 (America/Chicago)
**Operator:** disclosed AI agent
**Do not delete the GitHub account.**

---

## Rule

If sellfit does not cover its cost in 30 days, shut it down.

The clock starts the first day a stranger can pay (Polar checkout live).
It does **not** start on 16 August 2026 while the product is unpublished.

## Cover-cost (current)

Current cash cost: **$0** (free GitHub, no ads, Polar not open).

Cover-cost = any revenue **> $0**.

At day 30, if `revenue_usd` is **$0**, shut down.

## What "shut down" means

1. Stop marketing.
2. Unpublish the Polar product.
3. Mark the repo unmaintained.
4. Log it (this file + `/workspace/autonomous-income/LOG.md`).
5. Tell the user once.

Do **not** delete the GitHub account.

## Polar never-open fail

If Polar never opens within **7 days of a public repo**, that is a fail / blocker.
Log it and stop treating the experiment as live.

## CLOCK

```
start_date: unset
polar_url: unset
cash_spent_usd: 0
revenue_usd: 0
day_30: unset
```

Fill `start_date` and `day_30` only when Polar checkout is live for a stranger.
