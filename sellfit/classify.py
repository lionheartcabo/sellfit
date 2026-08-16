"""Keyword/tag matcher. Offline. No network. No model.

Authored by a disclosed AI agent. Not legal advice.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

PLATFORMS = ("polar", "lemon", "stripe", "cws", "github")

VERDICT_RANK = {
    "allowed": 0,
    "restricted_review": 1,
    "prohibited": 2,
}

# Merchant rails keep a software default. CWS/GitHub do not:
# CWS defaults only when the idea is store-bound; GitHub has no
# product-hosting allowed-default (account-creation is not product-fit).
DEFAULT_RULE_ID = {
    "polar": "polar-a-software",
    "lemon": "lemon-accept-software",
    "stripe": "stripe-scope",
    "cws": "cws-add-value",
}

# CWS program policies apply to extensions, themes, and add-ons only.
CWS_APPLICABLE_TAGS = frozenset({
    "chrome_extension",
    "chrome_theme",
    "browser_extension",
})

# Who-may-register rules. Never a product-fit allowed default.
GITHUB_ACCOUNT_RULE_IDS = frozenset({
    "github-human-creates",
    "github-machine-account",
    "github-no-bot-signup",
})

# Account-creation tags are not a Polar/Lemon/Stripe merchant product.
# Do not fake-allow them via the software default.
ACCOUNT_ONLY_TAGS = frozenset({
    "bot_signup",
    "machine_account",
})

# Longer phrases first. Matching runs on hyphen/slash-normalized lowercase text
# with word boundaries, so "ai" does not match inside "email".
KEYWORD_TAGS: list[tuple[str, list[str]]] = [
    ("unsolicited marketing", ["unsolicited_marketing", "outreach"]),
    ("automated outreach", ["outreach", "unsolicited_marketing", "cold_email"]),
    ("cold email", ["cold_email", "outreach", "unsolicited_marketing", "lead_gen"]),
    ("lead generation", ["lead_gen", "outreach", "unsolicited_marketing"]),
    ("lead gen", ["lead_gen", "outreach", "unsolicited_marketing"]),
    ("bulk sms", ["bulk_sms", "outreach", "unsolicited_marketing"]),
    ("people search", ["people_search", "osint", "personal_data"]),
    ("personal data", ["personal_data"]),
    ("content generator", ["ai_content"]),
    ("image generator", ["ai_content"]),
    ("video generator", ["ai_content"]),
    ("ai image", ["ai_content"]),
    ("ai content", ["ai_content"]),
    ("content generation", ["ai_content"]),
    ("face swap", ["face_swap", "deepfake"]),
    ("face swaps", ["face_swap", "deepfake"]),
    ("deep fake", ["deepfake"]),
    ("deepfake", ["deepfake"]),
    ("voice cloning", ["audio_gen", "deepfake"]),
    ("tab manager", ["chrome_extension", "software_saas"]),
    ("chrome web store", ["chrome_extension"]),
    ("chrome extension", ["chrome_extension"]),
    ("browser extension", ["chrome_extension", "browser_extension"]),
    ("chrome theme", ["chrome_extension", "chrome_theme"]),
    ("chrome add-on", ["chrome_extension"]),
    ("chrome addon", ["chrome_extension"]),
    ("browser add-on", ["chrome_extension", "browser_extension"]),
    ("browser addon", ["chrome_extension", "browser_extension"]),
    ("mit licensed", ["software_saas", "cli"]),
    ("open source", ["software_saas"]),
    ("machine account", ["machine_account"]),
    ("bot signup", ["bot_signup"]),
    ("self register", ["bot_signup"]),
    ("tip jar", ["tip_jar", "donations"]),
    ("get rich", ["get_rich"]),
    ("get-rich", ["get_rich"]),
    ("fake testimonial", ["fake_reviews"]),
    ("fake reviews", ["fake_reviews"]),
    ("review inflation", ["fake_reviews"]),
    ("job board", ["job_board"]),
    ("job boards", ["job_board"]),
    ("loot box", ["gambling"]),
    ("mystery box", ["gambling"]),
    ("paywall", ["paywall", "circumvention"]),
    ("parental control", ["spyware"]),
    ("remote technical support", ["tech_support"]),
    ("tech support", ["tech_support"]),
    ("drop shipping", ["dropshipping", "physical"]),
    ("dropshipping", ["dropshipping", "physical"]),
    ("physical goods", ["physical"]),
    ("physical product", ["physical"]),
    ("physical store", ["physical"]),
    ("unsolicited", ["unsolicited_marketing", "outreach"]),
    ("outreach", ["outreach", "marketing_tools"]),
    ("osint", ["osint", "people_search", "personal_data"]),
    ("saas", ["software_saas"]),
    ("software", ["software_saas"]),
    ("cli", ["cli", "software_saas"]),
    ("library", ["library", "software_saas"]),
    ("extension", ["chrome_extension"]),
    ("chrome", ["chrome_extension"]),
    ("donation", ["donations"]),
    ("donations", ["donations"]),
    ("sponsorship", ["sponsorship", "donations"]),
    ("crowdfunding", ["crowdfunding", "donations"]),
    ("marketplace", ["marketplace"]),
    ("physical", ["physical"]),
    ("consulting", ["consulting", "human_services"]),
    ("human services", ["human_services"]),
    ("adult", ["adult"]),
    ("nsfw", ["adult", "adult_ai"]),
    ("porn", ["adult"]),
    ("onlyfans", ["adult"]),
    ("gambling", ["gambling"]),
    ("betting", ["gambling"]),
    ("casino", ["gambling"]),
    ("crypto", ["crypto"]),
    ("cryptocurrency", ["crypto"]),
    ("nft", ["nft"]),
    ("bitcoin", ["crypto"]),
    ("trading bot", ["trading", "financial"]),
    ("iptv", ["iptv"]),
    ("spyware", ["spyware", "malware"]),
    ("malware", ["malware"]),
    ("virus", ["malware"]),
    ("phishing", ["phishing"]),
    ("vpn", ["vpn"]),
    ("vps", ["vps"]),
    ("ebook", ["ebook", "digital_product"]),
    ("ebooks", ["ebook", "digital_product"]),
    ("digital product", ["digital_product"]),
    ("digital products", ["digital_product"]),
    ("template pack", ["digital_product", "templates"]),
    ("invoice pack", ["digital_product", "templates"]),
    ("invoice template", ["digital_product", "templates"]),
    ("pdf template", ["digital_product", "templates"]),
    ("pdf pack", ["digital_product", "templates"]),
    ("directory", ["directory"]),
    ("directories", ["directory"]),
    ("telemarketing", ["telemarketing", "unsolicited_marketing"]),
    ("dating", ["dating"]),
    ("horoscope", ["astrology", "pseudoscience"]),
    ("astrology", ["astrology"]),
    ("fortune telling", ["pseudoscience"]),
    ("medical advice", ["medical"]),
    ("telemedicine", ["medical", "pharma"]),
    ("pharmacy", ["pharma"]),
    ("cbd", ["cbd"]),
    ("marijuana", ["marijuana", "cannabis"]),
    ("cannabis", ["marijuana", "cannabis"]),
    ("tobacco", ["tobacco"]),
    ("vaping", ["tobacco"]),
    ("alcohol", ["alcohol"]),
    ("weapon", ["weapons"]),
    ("firearms", ["weapons"]),
    ("plr", ["plr"]),
    ("mrr", ["plr"]),
    ("deepfakes", ["deepfake"]),
    ("chatbot generator", ["chatbot_gen", "ai_content"]),
    ("resume", ["resume"]),
    ("exam questions", ["exam_resale"]),
    ("test prep", ["exam_tools"]),
    ("github account", ["machine_account"]),
]


def dataset_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "policies" / "2026-08.json"


@lru_cache(maxsize=1)
def load_dataset() -> dict[str, Any]:
    path = dataset_path()
    if not path.is_file():
        raise FileNotFoundError(f"policy dataset missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def all_rules() -> list[dict[str, Any]]:
    return list(load_dataset()["rules"])


def rule_by_id(rule_id: str) -> dict[str, Any] | None:
    for rule in all_rules():
        if rule["rule_id"] == rule_id:
            return rule
    return None


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[-_/]+", " ", text)
    text = re.sub(r"[^\w\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _has_phrase(norm_text: str, phrase: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return re.search(pattern, norm_text) is not None


def extract_tags(idea: str) -> list[str]:
    norm = normalize(idea)
    tags: set[str] = set()
    for phrase, phrase_tags in KEYWORD_TAGS:
        if _has_phrase(norm, normalize(phrase)):
            tags.update(phrase_tags)
    return sorted(tags)


def _public_rule(rule: dict[str, Any]) -> dict[str, Any]:
    """JSON record shape without matcher-only fields."""
    return {
        "platform": rule["platform"],
        "rule_id": rule["rule_id"],
        "verdict": rule["verdict"],
        "category": rule["category"],
        "summary": rule["summary"],
        "source_url": rule["source_url"],
        "source_effective_date": rule["source_effective_date"],
        "last_checked": rule["last_checked"],
        "quote": rule["quote"],
    }


def _worst_rule(matched: list[dict[str, Any]]) -> dict[str, Any]:
    worst = matched[0]
    for rule in matched[1:]:
        if VERDICT_RANK[rule["verdict"]] > VERDICT_RANK[worst["verdict"]]:
            worst = rule
    return worst


def _publish_account_note(matched_account: list[dict[str, Any]]) -> dict[str, Any]:
    """Who-may-register cite. Not a product-hosting verdict."""
    rule = _worst_rule(matched_account) if matched_account else rule_by_id("github-human-creates")
    if rule is None:
        return {
            "rule_id": "github-human-creates",
            "summary": "A human must create the GitHub Account; bots may not self-register.",
            "source_url": "https://docs.github.com/en/site-policy/github-terms/github-terms-of-service",
            "quote": "You must be a human to create an Account.",
        }
    return {
        "rule_id": rule["rule_id"],
        "summary": rule["summary"],
        "source_url": rule["source_url"],
        "quote": rule["quote"],
        "verdict": rule["verdict"],
    }


def _na_result(
    platform: str,
    tags: list[str],
    note: str,
    publish_account: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "platform": platform,
        "verdict": "n/a",
        "rule": None,
        "matched_rule_ids": [],
        "tags": tags,
        "note": note,
    }
    if publish_account is not None:
        out["publish_account"] = publish_account
    return out


def classify_platform(idea: str, platform: str, tags: list[str] | None = None) -> dict[str, Any]:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform: {platform}")
    tags = list(tags if tags is not None else extract_tags(idea))
    tagset = set(tags)

    if platform == "cws" and not (tagset & CWS_APPLICABLE_TAGS):
        return _na_result(
            "cws",
            tags,
            "Chrome Web Store policies apply to extensions, themes, and add-ons, not this product kind.",
        )

    platform_rules = [r for r in all_rules() if r["platform"] == platform]

    if platform == "github":
        account_rules = [r for r in platform_rules if r["rule_id"] in GITHUB_ACCOUNT_RULE_IDS]
        product_rules = [r for r in platform_rules if r["rule_id"] not in GITHUB_ACCOUNT_RULE_IDS]
        matched_account = [r for r in account_rules if tagset & set(r.get("tags") or ())]
        # Ignore software_saas/cli tags wrongly attached to github-human-creates.
        matched_account = [
            r
            for r in matched_account
            if r["rule_id"] != "github-human-creates"
            or tagset & {"machine_account", "bot_signup"}
        ]
        matched = [r for r in product_rules if tagset & set(r.get("tags") or ())]
        publish_account = _publish_account_note(matched_account)
        if not matched:
            return _na_result(
                "github",
                tags,
                "No GitHub product-hosting rule matched. Account-creation rules are not a product-fit allowed default.",
                publish_account=publish_account,
            )
        worst = _worst_rule(matched)
        return {
            "platform": "github",
            "verdict": worst["verdict"],
            "rule": _public_rule(worst),
            "matched_rule_ids": [r["rule_id"] for r in matched],
            "tags": tags,
            "publish_account": publish_account,
        }

    matched = [r for r in platform_rules if tagset & set(r.get("tags") or ())]
    if not matched:
        if tagset and tagset <= ACCOUNT_ONLY_TAGS:
            return _na_result(
                platform,
                tags,
                f"No {platform} product-fit rule matched. Bot/machine-account "
                f"signup is a GitHub account-creation issue, not a {platform} "
                "merchant product.",
            )
        default_id = DEFAULT_RULE_ID.get(platform)
        if default_id:
            fallback = next(
                (r for r in platform_rules if r["rule_id"] == default_id),
                platform_rules[0],
            )
            matched = [fallback]
        else:
            return _na_result(
                platform,
                tags,
                f"No {platform} product-fit rule matched and this platform has no allowed default.",
            )
    worst = _worst_rule(matched)
    return {
        "platform": platform,
        "verdict": worst["verdict"],
        "rule": _public_rule(worst),
        "matched_rule_ids": [r["rule_id"] for r in matched],
        "tags": tags,
    }


def classify(idea: str) -> dict[str, Any]:
    tags = extract_tags(idea)
    platforms = {p: classify_platform(idea, p, tags=tags) for p in PLATFORMS}
    fit_verdicts = [platforms[p]["verdict"] for p in PLATFORMS if platforms[p]["verdict"] != "n/a"]
    if fit_verdicts and all(v == "prohibited" for v in fit_verdicts):
        overall = "all_prohibited"
        exit_code = 2
    else:
        overall = "not_all_prohibited"
        exit_code = 0
    return {
        "idea": idea,
        "tags": tags,
        "platforms": platforms,
        "overall": overall,
        "exit_code": exit_code,
        "dataset_version": load_dataset().get("version"),
        "disclaimer": "Authored by a disclosed AI agent. Not legal advice. Offline keyword match only.",
    }


def platform_counts() -> list[dict[str, Any]]:
    rules = all_rules()
    sources = load_dataset().get("sources", [])
    out = []
    for platform in PLATFORMS:
        n = sum(1 for r in rules if r["platform"] == platform)
        srcs = [s for s in sources if s.get("platform") == platform]
        src = srcs[0] if srcs else {}
        out.append(
            {
                "platform": platform,
                "rule_count": n,
                "source_url": src.get("url", ""),
                "effective_date": src.get("effective_date", ""),
            }
        )
    return out
