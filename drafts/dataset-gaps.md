# Dataset gaps (do not invent quotes)

Authored by a disclosed AI agent. Not legal advice. Last reviewed
2026-08-16 against the official pages already used in
`data/policies/2026-08.json`.

## CBD / cannabis

| Platform | Named on the official page? | Dataset |
|---|---|---|
| Lemon Squeezy | Yes — "Regulated products such as: CBD, …" | `lemon-regulated-products` (prohibited). Already present. |
| Stripe | Yes — prohibited **Marijuana** ("Cannabis products"); restricted **Cannabidiol (CBD)** ("CBD products containing only negligible amounts of THC, per local limits") | `stripe-marijuana` (prohibited), `stripe-r-cbd` (restricted_review). Added 2026-08-16 from https://stripe.com/legal/restricted-businesses (last updated 2026-05-13). |
| Polar | **No.** Polar AUP (25 Mar 2026) lists "Illegal or age-restricted products, including, but not limited to, drugs, alcohol, tobacco and vaping" (`polar-12`) and "Regulated services or products" (`polar-16`). It does not say CBD, cannabis, hemp, or marijuana. | **Gap.** A "CBD oil storefront" still defaults to `polar-a-software` (allowed). Do not tag `polar-12` / `polar-16` with `cbd` and do not invent a Polar CBD quote. |

A generic "CBD oil storefront" is tagged `cbd` only. Stripe restricted
(low-THC CBD) is the honest named match; high-THC cannabis is a
separate `marijuana` / `cannabis` tag.

## Bot / machine-account signup

GitHub ToS names this (`github-no-bot-signup`). Polar, Lemon, and
Stripe do not sell "bot signup" and have no such product rule. The
classifier now returns `n/a` on those three instead of fake-allowing
via the software default.

## Invoice / template packs

Not a policy gap. The matcher lacked keywords. "digital product",
"template pack", "invoice pack", "invoice template", "pdf template",
and "pdf pack" now tag `digital_product` / `templates` so Polar cites
`polar-a-digital` (templates, eBooks, PDFs).

`github-api-spam` is about selling GitHub users' personal information via
the API. Its matcher tags are `osint`, `data_resale`, `people_search`
only. `bot_signup` was removed from that rule so a signup idea does not
fake-match API-spam.

