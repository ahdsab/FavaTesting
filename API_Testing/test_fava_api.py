import os
import re
import unittest
import requests
from datetime import date, timedelta

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000").rstrip("/")
ENV_SLUG = os.getenv("LEDGER_SLUG")  # e.g. example-beancount-file


def discover_slug():
    if ENV_SLUG:
        return ENV_SLUG.strip("/")
    # try root (rare setups)
    try:
        if requests.get(f"{BASE_URL}/api/options/", timeout=5).status_code == 200:
            return ""
    except Exception:
        pass
    # parse landing page for first-level slug
    html = requests.get(BASE_URL, timeout=10).text
    m = re.search(r'href="/([^/]+)/"', html)
    if m:
        slug = m.group(1)
        if requests.get(f"{BASE_URL}/{slug}/api/options/", timeout=5).status_code == 200:
            return slug
    # fallbacks commonly seen in docs/demos
    for c in ("example-beancount-file", "example.beancount", "ledger.beancount"):
        try:
            if requests.get(f"{BASE_URL}/{c}/api/options/", timeout=5).status_code == 200:
                return c
        except Exception:
            pass
    raise RuntimeError("Could not discover ledger slug; set LEDGER_SLUG.")


def u(path: str, slug: str) -> str:
    path = path.lstrip("/")
    return f"{BASE_URL}/api/{path}" if not slug else f"{BASE_URL}/{slug}/api/{path}"


class TestAddTransactionAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = requests.get(BASE_URL, timeout=10)
        assert r.status_code == 200, f"Fava not reachable at {BASE_URL}"
        cls.slug = discover_slug()

    def test_put_add_entries_and_verify(self):
        # 1) Build one minimal, balanced Transaction in Fava's JSON shape
        today = date.today().isoformat()
        marker = f"API Add Test {today}"

        entry = {
            "type": "Transaction",
            "date": today,
            "flag": "*",
            "payee": "QA Bot",
            "narration": marker,
            "tags": [],
            "links": [],
            "meta": {},  # optional metadata
            "postings": [
                {
                    "account": "Assets:Cash",
                    "units": {"number": "-10.00", "currency": "USD"},
                    "meta": {},
                },
                {
                    "account": "Expenses:Testing",
                    "units": {"number": "10.00", "currency": "USD"},
                    "meta": {},
                },
            ],
        }

        # 2) PUT to add_entries
        r = requests.put(u("add_entries/", self.slug), json={"entries": [entry]}, timeout=15)
        self.assertEqual(r.status_code, 200, f"add_entries failed: {r.status_code} {r.text}")

        # 3) Verify via journal API in a tight date window
        rj = requests.get(
            u("journal/", self.slug),
            params={"from": today, "to": today},
            timeout=10,
        )
        self.assertEqual(rj.status_code, 200, rj.text)
        entries = rj.json()
        self.assertTrue(any(e.get("narration") == marker for e in entries), "New entry not found in journal")

        # 4) (Optional) Clean up with a compensating entry so repeat runs stay tidy
        cleanup = {
            "type": "Transaction",
            "date": today,
            "flag": "!",
            "payee": "QA Bot",
            "narration": f"{marker} CLEANUP",
            "tags": [],
            "links": [],
            "meta": {},
            "postings": [
                {"account": "Assets:Cash", "units": {"number": "10.00", "currency": "USD"}, "meta": {}},
                {"account": "Expenses:Testing", "units": {"number": "-10.00", "currency": "USD"}, "meta": {}},
            ],
        }
        rc = requests.put(u("add_entries/", self.slug), json={"entries": [cleanup]}, timeout=15)
        self.assertEqual(rc.status_code, 200, f"cleanup add_entries failed: {rc.status_code} {rc.text}")


if __name__ == "__main__":
    unittest.main()
