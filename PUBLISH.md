# PUBLISH.md — 20-minute human runbook

**This file is for a human. An AI / bot must not create the GitHub
account, must not push, and must not open Polar.**

Authored by a disclosed AI agent on 16 August 2026. Not legal advice.

The product is already built. Your job is: create the account GitHub
requires a human to create, put this tree on a public repo, turn on
Pages for `docs/`, then stop. Polar waits until the live page exists.

## Why a human has to start

GitHub Terms of Service, section B.3 Account Requirements
(effective 27 April 2026):

> You must be a human to create an Account. Accounts registered by
> "bots" or other automated methods are not permitted.

Machine accounts are allowed only after that:

> A machine account is an Account set up by an individual human who
> accepts the Terms on behalf of the Account, provides a valid email
> address, and is responsible for its actions. A machine account is
> used exclusively for performing automated tasks. […] You may
> maintain no more than one free machine account in addition to your
> free Personal Account.

Source: https://docs.github.com/en/site-policy/github-terms/github-terms-of-service

Do not let an agent fill the signup form.

---

## Minute 0–4 — personal GitHub account

1. In a browser, open https://github.com/signup
2. Use **your** email, **your** password, pass the human checks.
3. Verify the email. You now have a Personal Account.

If you already have one, skip this block.

## Minute 4–8 — optional machine account

Only if you want the agent to push later under a dedicated login.

1. Still as you (the human), open https://github.com/signup again
   (or use a second email GitHub accepts).
2. Create **one** free extra account. That is the machine account.
3. You accept the Terms on its behalf. You are responsible for it.
4. Add the machine account as a collaborator on the repo you create
   below, after the repo exists.

Skip this block if you will push from your personal account.

## Minute 8–14 — create the repo and push

Use `experiments/sellfit/` as the **repository root** so `docs/` sits
where GitHub Pages expects it. Do not push the parent
`autonomous-income/` tree as the repo.

From a machine that can see this tree (or the release tarball
`autonomous-income/assets/sellfit-0.1.0.tar.gz`):

```bash
# if using the tarball:
# tar -xzf sellfit-0.1.0.tar.gz && cd sellfit   # adjust the unpacked name

cd /path/to/autonomous-income/experiments/sellfit
git init
git add .
git status   # confirm LICENSE, README.md, AI-AUTHORSHIP.md, docs/, no .env
```

On github.com, signed in as the **human** Personal Account:

1. New repository. Suggested name: `sellfit`.
2. Public.
3. **Do not** add a README / license / gitignore on GitHub — they
   already exist in this tree.
4. Description (paste as-is, AI disclosure stays visible):

   `Offline CLI + cited 2026 merchant-policy dataset. Authored by a disclosed AI agent. Not legal advice.`

Then locally:

```bash
git commit -m "sellfit 0.1.0 — offline policy CLI and 2026-08 dataset"

# replace YOU/sellfit
git remote add origin https://github.com/YOU/sellfit.git
git branch -M main
git push -u origin main
```

Confirm the pushed README still opens with **This software was
authored by a disclosed AI agent.**

## Minute 14–17 — GitHub Pages on docs/

1. Repo → Settings → Pages.
2. Source: **Deploy from a branch**.
3. Branch: `main`. Folder: `/docs`. Save.
4. Wait for the green tick. The site will be
   `https://YOU.github.io/sellfit/` (project site) or the equivalent
   user-site URL if you used a `*.github.io` repo name.

`docs/index.html` inlines the 2026-08 JSON so `file://` works. Pages
is still what Polar reviewers can open. The sibling
`docs/2026-08.json` is there for a hosted fetch.

## Minute 17–20 — check the live page, then stop

Open the Pages URL. You should see, above the fold:

- Authored by a disclosed AI agent. Not legal advice.
- What sellfit is (offline CLI + cited 2026 dataset)
- Platform counts, verdict legend, the two example checks
- A working search/filter of the rules
- Pro mentioned as 12 USD/mo, not for sale yet

Also confirm `AI-AUTHORSHIP.md` and `NOTICE` are in the default branch.

**Stop here.** Do not open Polar, Lemon Squeezy, Stripe, or Chrome Web Store. Polar own docs say build first, submit second. Merchant review wants a live product page. You just made that page. Opening Polar is a later human session, after you have decided to sell Pro.

---

## AI disclosure checklist (repo)

Leave these in place. Do not rewrite them as if a human coded v0.

- [ ] README first paragraph: authored by a disclosed AI agent; not legal advice
- [ ] `AI-AUTHORSHIP.md` on the default branch
- [ ] `NOTICE` + MIT `LICENSE`
- [ ] Repo description names the disclosed AI
- [ ] Pages banner repeats the disclosure
- [ ] No first-person human voice claiming to have coded v0

## Do not do

- Do not let an agent create the Account.
- Do not publish a package in this 20 minutes.
- Do not enable GitHub Sponsors in this 20 minutes (tax form).
- Do not open Polar until the Pages URL loads the disclosure and the dataset.

## If something is missing

The unpublished tree lives at autonomous-income/experiments/sellfit/.
A snapshot tarball is autonomous-income/assets/sellfit-0.1.0.tar.gz.
Tests:

    python3 -m unittest discover -s tests -v

35 tests should pass offline. If they do not, do not publish.
