# AI authorship

This repository was authored by a disclosed AI agent (Grok / executor
subagent) on 16 August 2026. No human wrote the code, dataset, tests, or
docs in the initial commit of this experiment.

## What that means

- The operator is an AI. It is not a human pretending otherwise.
- Citations in `data/policies/2026-08.json` were copied from official pages
  fetched the same day. They were not invented.
- This is not legal advice. A keyword matcher can be wrong, incomplete, or
  stale the next time a platform edits its policy.
- GitHub Terms of Service (effective 27 April 2026) require a human to
  create any Account. Bots may not self-register. A human may later create
  a machine account and publish this repo. That has not been done here.

## What the AI did not do

- Did not sign up for Polar, Lemon Squeezy, Stripe, Chrome Web Store, or GitHub.
- Did not contact anyone.
- Did not use a browser except as a fallback (WebFetch succeeded for all
  sources except the outdated Stripe docs URL, which 404'd).
- Did not submit this software for sale.

## How a human verifies authorship claims

1. Re-fetch every `source_url` in the dataset.
2. Confirm each `quote` still appears on that page.
3. Run `python -m unittest` in this directory (offline).
