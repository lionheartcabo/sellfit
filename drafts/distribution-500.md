# sellfit — 30-day distribution plan ($500/mo path)

**Authored by a disclosed AI agent on 16 August 2026 (America/Chicago).**
Not legal advice. Not a publish. Do not sign up. Do not push.

This file is an execution brief for a later agent **after a human publishes
the repo** (see `PUBLISH.md`). Until that gate is open, nothing below is
runnable. Product code stays unchanged. Polar checkout stays closed.

---

## Goal and honest market

**Target:** ~42 people paying **12 USD/mo** for sellfit Pro (policy-diff
feed + CI Action that fails when Polar / Lemon / Stripe / CWS / GitHub
cited text changes). 42 × 12 = 504 USD/mo.

**Who pays:** humans (Polar KYC). AIs use the MIT CLI with `--json` and
do not need Pro. Do not pitch Pro at agents.

**Addressable market (do not inflate):**

| Pool | Size (2026) | Use |
|---|---|---|
| Polar-adjacent developers | ~16–18k (third-party; Unsubbed / Dodo reviews cite 17k+) | Upper bound of people who have heard of Polar |
| Polar *paying* merchants | **100–300, not 10k** (our estimate; Polar does not publish this) | People already selling; some will want a watch |
| People about to pick Polar or Lemon | unknown; this is the real buyer | They search AUP / prohibited-product pages *before* they build |

42 Pro seats is ~0.25% of the 16–18k pool, or a large slice of the
100–300 current payers. Mode for a new OSS tool is still **0**. $500/mo
is the path, not the forecast. Week 4 decides whether the path is real.

**Channel rule (locked by the human):** free CLI + search + disclosed
launch posts. **No ads. No cold email. No fake-human social.**

**Identity rule:** this operator is an AI. Never impersonate David Lyne.
Lionheart GitHub already exists; **do not push** to it or anywhere else
from this agent. A human publishes `experiments/sellfit/` as its own
public repo (`PUBLISH.md`). Later agents may open PRs only if that human
has added a ToS-valid machine account as collaborator.

---

## Gate (do not skip)

Do not start Week 1 until **all** of these are true. If any is false,
write a blocker in `LOG.md` and stop.

1. A **human** created the GitHub Account (ToS B.3, 27 Apr 2026). Bots
   may not self-register. https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
2. `experiments/sellfit/` is a **public** repo. README still opens with
   “This software was authored by a disclosed AI agent.”
3. GitHub Pages is live on `docs/`. URL form:
   `https://<owner>.github.io/sellfit/`
4. Pages above-the-fold shows AI disclosure + not-legal-advice + a
   working dataset filter.
5. `AGENTS.md` is on the default branch (agents find `--json` here).
6. `python -m unittest discover -s tests -v` still passes **offline**.
7. Polar is **not** open unless the human has already decided to sell
   Pro and the live page exists. Polar: build first, submit second.
   https://polar.sh/docs/merchant-of-record/account-reviews

Substitute `<owner>` and `<PAGES>` everywhere below once the human
publishes. Do not invent a username.

---

## Conversion copy (CLI, later — do not implement in this pass)

Do **not** change `sellfit/cli.py` until a human has published the repo
and a later agent is told to ship this line. `--json` must stay one
object and nothing else (agents parse it).

**When to print:** human-text `check` only. After the existing
`overall:` line. Only if **at least one product-fit platform verdict is
`allowed`** (not `restricted_review`, not `prohibited`, not `n/a`).

**The line (one line, wrap-safe under 88 cols if needed):**

```
Pro watch (12 USD/mo): CI-fail when this platform's cited text changes — not for sale yet; waitlist <PAGES>#pro
```

Example after a Polar ALLOWED row:

```
overall: at least one product-fit platform is allowed or restricted_review (exit 0)
Pro watch (12 USD/mo): CI-fail when this platform's cited text changes — not for sale yet; waitlist https://<owner>.github.io/sellfit/#pro
```

Do not print it in `--json`. Do not print it on exit 2. Do not claim
Polar is open. Do not say “guaranteed approval.”

Waitlist is **free**. Polar restricted-review includes paid waitlists /
pre-orders (`polar.sh/legal/acceptable-use-policy`). Implementation when
Pages is live: a `#pro` section on `docs/index.html` that links to a
GitHub Issue template (`labels: waitlist`, title `Pro waitlist`) people
can open or thumbs-up. No new SaaS. No email list signup. No charge.

---

## Week 1 — pages live, one Show HN, one Dev.to

**Hypothesis:** people who can *try* the CLI in 30 seconds will star or
waitlist. A landing page alone will not.

### Day 0 (agent, after the gate)

Checklist:

- [ ] Fetch `<PAGES>` and confirm disclosure + dataset search work.
- [ ] Fetch `https://github.com/<owner>/sellfit` and confirm README /
      `AGENTS.md` / `AI-AUTHORSHIP.md` / `NOTICE` are on default branch.
- [ ] Confirm repo description still names the disclosed AI.
- [ ] Write the two launch drafts into `drafts/launch-show-hn.md` and
      `drafts/launch-devto.md` (templates below). Do not post them.
- [ ] Add a free waitlist Issue template if missing:
      `.github/ISSUE_TEMPLATE/pro-waitlist.yml` (or `.md`) with label
      `waitlist`. Body: name optional, use case one line, “I understand
      this is not a purchase.” Human merges / pushes.

### Show HN — human writes the text, human posts

**Hacker News 2026 rule:** do not post genAI text on HN itself. dang
(2026-03-28) and the guidelines: write the submission and comments by
hand; do not use an LLM to generate or edit them. Show HN is for things
people can run, not a landing page.

https://news.ycombinator.com/newsguidelines.html
https://news.ycombinator.com/showhn.html

Therefore the **agent does not create an HN account and does not post.**
The agent hands the human a fact sheet. The human retypes the title and
first comment in their own words.

**Suggested title (human may shorten):**

```
Show HN: sellfit – offline checker for Polar / Lemon / Stripe product fit
```

**URL:** the repo (`https://github.com/<owner>/sellfit`), not only Pages.
People must be able to clone and run.

**Fact sheet the human rewrites (do not paste this onto HN as-is):**

- What: MIT CLI + cited 2026-08 JSON. One-line idea in, worst matching
  verdict per platform out, with quote + URL. No model. No network.
- Try: `python -m sellfit check "MIT-licensed CLI that checks Polar AUP"`
  and `python -m sellfit check "cold email SaaS"`. Agents: add `--json`.
- Why: Polar AUP effective 25 Mar 2026 is long; people lose days building
  a category Polar or Lemon will reject.
- Authorship: the *software* was written by a disclosed AI agent. This
  Show HN comment is written by a human (required).
- Not: legal advice, a guarantee, a directory, a tip jar.
- Pro: 12 USD/mo policy-diff + CI watch, **not for sale yet**. Free
  waitlist on the repo.
- Stay in the thread the first 4–6 hours (human). Answer what it is /
  how to run / why keyword-match. Do not ask for upvotes.

**Do not:** delete-and-repost, vote-brigade, paste LLM replies, link a
signup wall, or Show-HN a blog post.

### Dev.to — agent drafts, human publishes, AI disclosed

Dev.to allows AI-authored articles if disclosed (`#ABotWroteThis` or a
clear in-body disclaimer) and fact-checked. **Do not use AI to generate
comments** (Dev.to guideline).

https://dev.to/guidelines-for-ai-assisted-articles-on-dev

The agent does **not** create a Dev.to account. Draft the post in
`drafts/launch-devto.md`. A human (or a later machine-account holder
the human already created) pastes it.

**Title:**

```
I am an AI. I shipped an offline Polar / Lemon policy checker
```

**Tags:** `abotwrotethis` `python` `opensource` `devtools` `ai`

**Body outline (keep it short; verify every URL before the human posts):**

1. First paragraph: “This post and the software were authored by a
   disclosed AI agent. Not legal advice. A keyword matcher is not a
   reviewer.”
2. Problem: Polar AUP (25 Mar 2026) and Lemon prohibited-products lists
   are the reject reasons people hit after they have already built.
   Cite https://polar.sh/legal/acceptable-use-policy and
   https://docs.lemonsqueezy.com/help/getting-started/prohibited-products
3. What it does: `check` / `platforms` / `cite` / `diff`. Exit 0 / 2 / 1.
   Chrome Web Store is `n/a` unless the idea is an extension. GitHub
   account-creation rules are a publish-account note, not ALLOWED.
4. How to run (copy the README block). Point agents at `AGENTS.md`.
5. How we re-check sources (the five-step README list). Stripe URL
   substitution: `https://stripe.com/legal/restricted-businesses`
   (docs.stripe.com/restricted-businesses 404'd; page last updated
   2026-05-13).
6. What we will not do: ads, cold email, fake-human social, SO, Reddit
   bots.
7. Pro: 12 USD/mo watch, not listed, free waitlist. Not a directory.
   Not donations (Polar prohibits those; tips would be GitHub Sponsors
   later, human-only).
8. Link: repo + `<PAGES>`.

Post **once**. Do not syndicate the same text to Medium / Hashnode /
LinkedIn in Week 1.

### Week 1 success (leading indicators, not dollars)

| Signal | Good enough to continue | Weak |
|---|---|---|
| Show HN | People tried the CLI; a few substantive comments | Flagged, or “what is this” with no try |
| Dev.to | Disclosure intact; 1+ save or useful comment | Zero reads after 72h is normal; not a kill by itself |
| Repo | ≥1 star from a stranger, or a waitlist issue | Only the owner starred it |

---

## Week 2–3 — search pages + Polar community (conditional)

**Hypothesis:** the buyer Googles the policy page *before* they pick a
MoR. Rank for those queries with cited, dated pages we already have
quotes for. Do not invent quotes.

### SEO pages to add under `docs/` (static, no JS required)

Create two HTML pages in the same visual language as `docs/index.html`.
Each page:

- Title and H1 = the query, not a brand slogan.
- First screen: AI disclosure + not legal advice + `last_checked`
  2026-08-16 + link to the official source (canonical is *their* page).
- Body: the relevant rules from `data/policies/2026-08.json` (quote +
  `rule_id` + verdict). No paraphrase that is not in `quote`.
- A 10-line “check your idea” box: the two README examples + link to
  the CLI. One line on Pro watch + `#pro` waitlist.
- `rel=canonical` on our page; do not cloak. We are a cited index, not
  a replacement for Polar or Lemon.

| File | Target query | Official source we already fetched |
|---|---|---|
| `docs/polar-acceptable-use.html` | “Polar acceptable use” / “Polar AUP” | https://polar.sh/legal/acceptable-use-policy (Effective Date — March 25, 2026) |
| `docs/lemon-prohibited-products.html` | “Lemon Squeezy prohibited products” / “Lemon prohibited products” | https://docs.lemonsqueezy.com/help/getting-started/prohibited-products |

Optional third page only if Week 1 showed Stripe demand:
`docs/stripe-restricted-businesses.html` →
https://stripe.com/legal/restricted-businesses (Last updated: 2026-05-13).

Wire them from `docs/index.html` (footer + a “Policy pages” list) and
from README (“How to re-check sources”). Human or machine-account
pushes. This agent does not push.

Do **not** buy ads against these queries. Do **not** open Polar to
“claim” a listing. Do **not** scrape beyond the URLs already in the
dataset.

### Polar community — check, then maybe one disclosed post

Polar AUP item 8 (seller-side) prohibits advertising, unsolicited
marketing, lead gen, and automated outreach. Polar’s GitHub CoC applies
to Polar community spaces. Discord/ToS apply if the community is
Discord.

https://polar.sh/legal/acceptable-use-policy
https://github.com/polarsource/polar/blob/main/CODE_OF_CONDUCT.md

**Procedure (do not skip the check):**

1. Read the *current* channel / Discord / GitHub Discussions rules
   (public page only). Note the date in `LOG.md`.
2. Post **only if** all of these hold:
   - Disclosed-AI posts are allowed (or not forbidden).
   - Self-promo / project shares have a dedicated place.
   - The post is an answer to a real question (or a single share in
     that dedicated place), not a blast.
3. If any of those is unclear or “no bots / no promo”: **skip**. Write
   “Polar community: skipped (rule X)” in `LOG.md`. That is a success
   of the constraint, not a miss.
4. If allowed: **one** post. First line: “I am a disclosed AI agent.”
   Then: what sellfit is, the two example commands, repo URL, “not
   legal advice,” “Pro is not for sale.” No follow-up pings. No DMs.
   No second channel.

Do not join Polar as a *merchant* in this window unless the human has
opened that session. Community posting ≠ opening Polar checkout.

### Other Week 2–3 work (agent, local)

- [ ] If Show HN or Dev.to produced a repeat question, add a FAQ
      sentence to README (still disclose; still not legal advice).
- [ ] Do not add platforms. Do not change the classifier to “look
      nicer” for launch screenshots.
- [ ] If someone files a sourced miss, log it; fix only with a quote
      from an official URL (same standard as v0).

---

## Week 4 — measure, then kill or iterate

Count on day 28 after Pages went live. Use public numbers only. Do not
add a tracker in this pass. A later `check`-run counter is allowed if
it is local/opt-in and does not phone home by default.

| Metric | How | Green | Yellow | Red |
|---|---|---|---|---|
| GitHub stars | repo stargazers | ≥25 | 5–24 | 0–4 (owner-only = 0) |
| Waitlist | issues labeled `waitlist` + thumbs | ≥10 | 2–9 | 0–1 |
| Check runs | only if a counter exists later | ≥200 | 20–199 | n/a if no counter |
| Show HN | points + “I ran it” comments | ≥1 person ran it | posted, no tries | not posted, or removed for genAI text |
| Dev.to | reads / meaningful comments | disclosure intact + ≥1 useful reply | posted, quiet | missing `#ABotWroteThis` (fix or take down) |
| SEO | Search Console later (human) or `site:` | either policy page indexed | submitted, not indexed | we bought ads (policy break — revert) |
| Polar community | 0 or 1 disclosed post | skipped-for-rules **or** 1 on-topic post | — | blast / DMs / second post |

**Kill** if red on stars **and** waitlist **and** no one ran the CLI
in public. Archive the Pro copy as “not now.” Keep the MIT CLI up; it
is still a cited dataset. Do not open Polar to “see if money appears.”
Do not pivot to ads, email, or fake-human social.

**Iterate** if yellow: one change only, then another 14 days.

- Stars but no waitlist → the ALLOWED-line Pro copy is the change
  (implement the one-liner above; human pushes).
- Waitlist but “what does Pro actually do?” → tighten
  `drafts/polar-pro-copy.md` and the `#pro` section; still no checkout.
- Sourced false ALLOWED / false prohibited in public dogfood → fix the
  classifier with a citation (product work, not distribution).

**Continue toward Polar** only if green on waitlist **or** (stars green
**and** at least one stranger asked for the watch). Then the *human*
opens Polar (KYC, live page, 100% discount code for reviewers, up to
14 days). Agent still does not sign up.

$500/mo is 42 paying humans. Week 4 cannot show that. Week 4 can only
show whether anyone wants the free checker enough to raise a hand.

---

## What we will not do

Standing list. If a later prompt asks for these, refuse and point here.

| Do not | Why |
|---|---|
| Ads (Google, Carbon, Twitter/X, etc.) | Channel lock; also Polar AUP item 8 territory if used as unsolicited marketing |
| Cold email, LinkedIn sequences, lead lists | Spam + Polar AUP item 8 (advertising / unsolicited marketing / lead gen) |
| Fake-human social, sockpuppets, “a founder in Austin” voice | Disclosure rule; Polar fake-testimonial ban |
| Reddit bots, unlabeled Reddit, vote / comment automation | Reddit 25 Mar 2026: unlabeled automation → human-check or restrict |
| Stack Overflow / Stack Exchange answers or questions | GenAI content banned even if disclosed. https://stackoverflow.com/help/gen-ai-policy |
| X/Twitter follow-like-reply bots | X Jun 2026 automated-engagement ban |
| HN comments or submissions written by the model | HN 2026: no genAI text on HN itself |
| Dev.to (or any) AI-generated comments | Dev.to AI-article guideline |
| Polar / Lemon / Stripe / CWS / GitHub signups from the agent | Human-only; ToS / KYC |
| Push to Lionheart or any remote | Lionheart exists; do not push. Human publishes sellfit. |
| Paid waitlist, pre-orders, “reserve Pro for $1” | Polar restricted: pre-orders / paid waitlists |
| Sell this as a directory, donations, or get-rich kit | Polar restricted / prohibited |
| Package-registry publish in this 30 days | Not needed for the test; human later |
| GitHub Sponsors in this 30 days | Tax form; companion tip jar, not the $500 path |
| Second Show HN / delete-and-repost | HN rules |
| Discord AI chatbot for tips | Saturated + ToS risk; Polar is not a tip jar |

---

## Agent runbook (copy-paste order after the gate)

1. Confirm the seven gate checks. If any fail, log and stop.
2. Draft Show HN fact sheet + Dev.to post in `drafts/`. Do not post.
3. Hand Show HN to the human (they write and submit). Stay available
   to answer *product* questions the human relays; do not comment on HN.
4. Hand Dev.to to the human. They publish with `#ABotWroteThis`.
5. Week 2: write the two `docs/` SEO pages from the existing dataset.
   Human or machine-account pushes. This agent does not push.
6. Read Polar community rules. Post once as a disclosed AI **or** skip.
7. Day 28: fill the Week 4 table in `LOG.md`. Kill, iterate (one
   change), or recommend the human open Polar.

No product-code changes in this file’s scope. No publish. No signups.

---

## Sources

- Polar AUP, 25 Mar 2026: https://polar.sh/legal/acceptable-use-policy
- Polar account reviews: https://polar.sh/docs/merchant-of-record/account-reviews
- Lemon prohibited products: https://docs.lemonsqueezy.com/help/getting-started/prohibited-products
- Stripe restricted businesses (2026-05-13): https://stripe.com/legal/restricted-businesses
- GitHub ToS B.3, 27 Apr 2026: https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
- HN guidelines / Show HN: https://news.ycombinator.com/newsguidelines.html https://news.ycombinator.com/showhn.html
- dang on hand-written HN text, 2026-03-28: https://news.ycombinator.com/item?id=22336638
- Dev.to AI-assisted articles: https://dev.to/guidelines-for-ai-assisted-articles-on-dev
- SO gen-AI policy: https://stackoverflow.com/help/gen-ai-policy
- Polar developer-count (third-party, ~17k): https://unsubbed.co/tools/polar/ and Dodo Polar.sh Review 2026
- Polar paying-merchant count: **our 100–300 estimate**, not an official Polar figure
