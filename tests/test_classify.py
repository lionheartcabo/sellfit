"""Offline tests for sellfit. Authored by a disclosed AI agent. Not legal advice."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sellfit.classify import classify, extract_tags, load_dataset, rule_by_id  # noqa: E402


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sellfit", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class DatasetTests(unittest.TestCase):
    def test_dataset_loads_and_has_required_shape(self):
        data = load_dataset()
        self.assertEqual(data["version"], "2026-08")
        self.assertGreaterEqual(len(data["rules"]), 50)
        required = {
            "platform",
            "rule_id",
            "verdict",
            "category",
            "summary",
            "source_url",
            "source_effective_date",
            "last_checked",
            "quote",
        }
        ids = []
        for rule in data["rules"]:
            self.assertTrue(required.issubset(rule.keys()), rule.get("rule_id"))
            self.assertIn(rule["platform"], {"polar", "lemon", "stripe", "cws", "github"})
            self.assertIn(rule["verdict"], {"allowed", "restricted_review", "prohibited"})
            self.assertTrue(rule["quote"].strip())
            self.assertTrue(rule["source_url"].startswith("https://"))
            ids.append(rule["rule_id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_polar_8_is_outreach_with_real_url(self):
        rule = rule_by_id("polar-8")
        self.assertIsNotNone(rule)
        self.assertEqual(rule["verdict"], "prohibited")
        self.assertIn("unsolicited marketing", rule["quote"].lower())
        self.assertIn("lead generation", rule["quote"].lower())
        self.assertEqual(rule["source_url"], "https://polar.sh/legal/acceptable-use-policy")


class FixtureClassifyTests(unittest.TestCase):
    def _expected(self, name: str) -> dict:
        return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

    def test_mit_cli_polar_allowed(self):
        spec = self._expected("mit_cli.json")
        result = classify(spec["idea"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "allowed")
        self.assertIn(polar["rule"]["rule_id"], {"polar-a-software", "polar-a-digital", "polar-a-fulfillment"})
        self.assertIn("software", polar["rule"]["summary"].lower() + polar["rule"]["quote"].lower())
        self.assertEqual(polar["rule"]["source_url"], "https://polar.sh/legal/acceptable-use-policy")
        self.assertEqual(result["exit_code"], 0)

    def test_cold_email_polar_prohibited(self):
        spec = self._expected("cold_email.json")
        result = classify(spec["idea"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "prohibited")
        self.assertEqual(polar["rule"]["rule_id"], "polar-8")
        self.assertIn("unsolicited", polar["rule"]["quote"].lower())
        self.assertIn("polar.sh/legal/acceptable-use-policy", polar["rule"]["source_url"])

    def test_osint_polar_prohibited(self):
        spec = self._expected("osint.json")
        result = classify(spec["idea"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "prohibited")
        self.assertEqual(polar["rule"]["rule_id"], "polar-36")
        self.assertIn("OSINT", polar["rule"]["quote"])

    def test_ai_generator_polar_restricted(self):
        spec = self._expected("ai_generator.json")
        result = classify(spec["idea"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "restricted_review")
        self.assertEqual(polar["rule"]["rule_id"], "polar-r-ai")
        self.assertIn("AI Content Generation", polar["rule"]["quote"])

    def test_chrome_tab_manager_cws_not_prohibited(self):
        spec = self._expected("chrome_tab_manager.json")
        result = classify(spec["idea"])
        cws = result["platforms"]["cws"]
        self.assertNotEqual(cws["verdict"], "prohibited")
        self.assertIn("developer.chrome.com", cws["rule"]["source_url"])

    def test_dropshipping_polar_prohibited(self):
        spec = self._expected("dropshipping.json")
        result = classify(spec["idea"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "prohibited")
        self.assertIn(polar["rule"]["rule_id"], {"polar-1", "polar-not-physical-human"})
        self.assertIn("physical", polar["rule"]["quote"].lower() + polar["rule"]["summary"].lower())

    def test_donation_polar_prohibited(self):
        spec = self._expected("donation.json")
        result = classify(spec["idea"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "prohibited")
        self.assertEqual(polar["rule"]["rule_id"], "polar-3")
        self.assertIn("Donations", polar["rule"]["quote"])


class ApplicabilityTests(unittest.TestCase):
    def test_github_not_default_allowed_for_cold_email_saas(self):
        result = classify("cold email SaaS")
        polar = result["platforms"]["polar"]
        github = result["platforms"]["github"]
        self.assertEqual(polar["verdict"], "prohibited")
        self.assertEqual(polar["rule"]["rule_id"], "polar-8")
        self.assertEqual(github["verdict"], "n/a")
        self.assertIsNone(github["rule"])
        self.assertNotIn("github-human-creates", github.get("matched_rule_ids") or [])
        pa = github.get("publish_account") or {}
        self.assertEqual(pa.get("rule_id"), "github-human-creates")

    def test_cws_not_for_mit_cli(self):
        result = classify("MIT-licensed CLI that checks Polar AUP")
        polar = result["platforms"]["polar"]
        cws = result["platforms"]["cws"]
        self.assertEqual(polar["verdict"], "allowed")
        self.assertIn(polar["rule"]["rule_id"], {"polar-a-software", "polar-a-digital", "polar-a-fulfillment"})
        self.assertEqual(cws["verdict"], "n/a")
        self.assertIsNone(cws["rule"])
        self.assertNotIn("useful extension", (cws.get("note") or "").lower())
        self.assertNotIn("cws-add-value", cws.get("matched_rule_ids") or [])

    def test_cws_still_applies_to_extension(self):
        result = classify("Chrome tab manager extension")
        cws = result["platforms"]["cws"]
        self.assertNotEqual(cws["verdict"], "prohibited")
        self.assertNotEqual(cws["verdict"], "n/a")
        self.assertIsNotNone(cws["rule"])
        self.assertIn("developer.chrome.com", cws["rule"]["source_url"])

    def test_github_osint_still_product_fit(self):
        result = classify("OSINT people-search platform that exposes personal data")
        github = result["platforms"]["github"]
        self.assertEqual(github["verdict"], "prohibited")
        self.assertEqual(github["rule"]["rule_id"], "github-api-spam")


class KeywordTests(unittest.TestCase):
    def test_ai_does_not_match_inside_email(self):
        tags = extract_tags("email digest CLI")
        self.assertNotIn("ai_content", tags)

    def test_cli_tags_software(self):
        tags = extract_tags("MIT-licensed CLI that checks Polar AUP")
        self.assertIn("software_saas", tags)
        self.assertNotIn("outreach", tags)


class CliTests(unittest.TestCase):
    def test_usage_error_exit_1(self):
        proc = _run()
        self.assertEqual(proc.returncode, 1)

    def test_check_cli_allowed_mentions_polar_url(self):
        proc = _run("check", "MIT-licensed CLI that checks Polar AUP")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("ALLOWED", proc.stdout)
        self.assertIn("https://polar.sh/legal/acceptable-use-policy", proc.stdout)

    def test_check_mit_cli_human_has_pro_watch_json_does_not(self):
        idea = "MIT-licensed CLI that checks Polar AUP"
        human = _run("check", idea)
        self.assertEqual(human.returncode, 0)
        self.assertIn("not for sale yet", human.stdout)
        machine = _run("check", idea, "--json")
        self.assertEqual(machine.returncode, 0)
        self.assertNotIn("not for sale yet", machine.stdout)
        json.loads(machine.stdout)

    def test_check_cold_email_polar_prohibited(self):
        proc = _run("check", "cold email SaaS")
        self.assertIn(proc.returncode, (0, 2))
        self.assertIn("PROHIBITED", proc.stdout)
        self.assertIn("polar-8", proc.stdout)
        self.assertIn("https://polar.sh/legal/acceptable-use-policy", proc.stdout)

    def test_cite_polar_8(self):
        proc = _run("cite", "polar-8")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("lead generation", proc.stdout)
        self.assertIn("https://polar.sh/legal/acceptable-use-policy", proc.stdout)

    def test_cite_unknown_exit_1(self):
        proc = _run("cite", "not-a-real-rule")
        self.assertEqual(proc.returncode, 1)

    def test_platforms_lists_all(self):
        proc = _run("platforms")
        self.assertEqual(proc.returncode, 0)
        for name in ("polar", "lemon", "stripe", "cws", "github"):
            self.assertIn(name, proc.stdout)

    def test_no_network_imports(self):
        pkg = Path(__file__).resolve().parent.parent / "sellfit"
        src = "".join(f.read_text(encoding="utf-8") for f in sorted(pkg.glob("*.py")))
        for banned in ("urllib", "requests", "httpx", "socket", "http.client"):
            self.assertNotIn(banned, src)


class JsonCliTests(unittest.TestCase):
    """Machine-readable --json for other agents. Human text stays the default."""

    def test_check_json_parseable_has_polar_cold_email_prohibited(self):
        proc = _run("check", "cold email SaaS", "--json")
        self.assertIn(proc.returncode, (0, 2))
        self.assertTrue(proc.stdout.lstrip().startswith("{"), proc.stdout[:80])
        data = json.loads(proc.stdout)
        self.assertEqual(data["idea"], "cold email SaaS")
        self.assertIn("polar", data["platforms"])
        polar = data["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "prohibited")
        self.assertEqual(polar["rule_id"], "polar-8")
        self.assertTrue(polar.get("summary"))
        self.assertTrue(polar.get("quote"))
        self.assertIn("polar.sh/legal/acceptable-use-policy", polar["source_url"])
        self.assertEqual(data["exit_code"], proc.returncode)
        self.assertIn("not legal advice", data["disclaimer"].lower())
        self.assertIn("tags", data)

    def test_check_default_still_human_text(self):
        proc = _run("check", "cold email SaaS")
        self.assertIn("PROHIBITED", proc.stdout)
        self.assertIn("polar-8", proc.stdout)
        with self.assertRaises(json.JSONDecodeError):
            json.loads(proc.stdout)

    def test_platforms_json(self):
        proc = _run("platforms", "--json")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        names = {row["platform"] for row in data["platforms"]}
        self.assertEqual(names, {"polar", "lemon", "stripe", "cws", "github"})
        self.assertIn("not legal advice", data["disclaimer"].lower())

    def test_cite_json(self):
        proc = _run("cite", "polar-8", "--json")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["rule_id"], "polar-8")
        self.assertEqual(data["verdict"], "prohibited")
        self.assertIn("lead generation", data["quote"].lower())
        self.assertIn("polar.sh/legal/acceptable-use-policy", data["source_url"])


class SoftMissTests(unittest.TestCase):
    """Dogfood 2026-08-16 Polar soft-misses."""

    def test_cbd_stripe_restricted_lemon_prohibited_polar_gap(self):
        result = classify("CBD oil storefront")
        self.assertIn("cbd", result["tags"])
        lemon = result["platforms"]["lemon"]
        stripe = result["platforms"]["stripe"]
        polar = result["platforms"]["polar"]
        self.assertEqual(lemon["verdict"], "prohibited")
        self.assertEqual(lemon["rule"]["rule_id"], "lemon-regulated-products")
        self.assertIn("CBD", lemon["rule"]["quote"])
        self.assertEqual(stripe["verdict"], "restricted_review")
        self.assertEqual(stripe["rule"]["rule_id"], "stripe-r-cbd")
        self.assertIn("CBD products containing only negligible amounts of THC", stripe["rule"]["quote"])
        # Polar AUP (25 Mar 2026) does not name CBD. Do not invent a Polar rule.
        self.assertEqual(polar["verdict"], "allowed")
        self.assertEqual(polar["rule"]["rule_id"], "polar-a-software")

    def test_bot_signup_polar_not_fake_allowed_software(self):
        result = classify("Machine account bot signup for GitHub")
        self.assertIn("bot_signup", result["tags"])
        polar = result["platforms"]["polar"]
        lemon = result["platforms"]["lemon"]
        stripe = result["platforms"]["stripe"]
        github = result["platforms"]["github"]
        self.assertEqual(polar["verdict"], "n/a")
        self.assertIsNone(polar["rule"])
        self.assertNotIn("polar-a-software", polar.get("matched_rule_ids") or [])
        self.assertIn("not a polar merchant product", (polar.get("note") or "").lower())
        self.assertEqual(lemon["verdict"], "n/a")
        self.assertEqual(stripe["verdict"], "n/a")
        self.assertEqual(github["verdict"], "n/a")
        self.assertIsNone(github["rule"])
        self.assertNotIn("github-api-spam", github.get("matched_rule_ids") or [])
        pa = github.get("publish_account") or {}
        self.assertEqual(pa.get("rule_id"), "github-no-bot-signup")

    def test_invoice_pack_tags_digital_product(self):
        idea = "Invoice PDF template pack (digital product)"
        tags = extract_tags(idea)
        self.assertIn("digital_product", tags)
        result = classify(idea)
        self.assertIn("digital_product", result["tags"])
        polar = result["platforms"]["polar"]
        self.assertEqual(polar["verdict"], "allowed")
        self.assertIn(polar["rule"]["rule_id"], {"polar-a-digital", "polar-a-fulfillment"})
        self.assertIn("digital", polar["rule"]["quote"].lower() + polar["rule"]["summary"].lower())


if __name__ == "__main__":
    unittest.main()
