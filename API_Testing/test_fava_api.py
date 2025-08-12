import os
import unittest
import requests
from datetime import date, timedelta

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
LEDGER_SLUG = os.environ.get("LEDGER_SLUG", "example-beancount-file")

def api_url(path: str) -> str:
    base = BASE_URL.rstrip("/")
    slug = LEDGER_SLUG.strip("/ ")
    return f"{base}/{slug}/api/{path.lstrip('/')}"

class TestFavaRealAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # quick smoke to fail fast if server isn't up
        r = requests.get(BASE_URL, timeout=10)
        assert r.status_code == 200, f"Fava not reachable at {BASE_URL}"

    def test_changed_endpoint(self):
        """GET /api/changed/ -> returns a boolean (file change flag)."""
        r = requests.get(api_url("changed/"), timeout=10)
        self.assertEqual(r.status_code, 200)
        self.assertIn(r.headers.get("Content-Type", ""), ("application/json", "application/json; charset=utf-8"))
        self.assertIn(r.json(), (True, False))  # returns a boolean

    def test_options_endpoint(self):
        """GET /api/options/ -> returns Fava+Beancount options as strings."""
        r = requests.get(api_url("options/"), timeout=10)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        # Expect keys like 'fava_options' and 'beancount_options'
        self.assertIsInstance(data, dict)
        self.assertIn("fava_options", data)
        self.assertIn("beancount_options", data)

    def test_income_statement(self):
        """GET /api/income_statement/?time=YYYY -> returns tree report data."""
        # pick a broad period to always have data in example ledgers
        year = str(date.today().year - 1)
        r = requests.get(api_url("income_statement/"), params={"time": year}, timeout=10)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        # Basic shape checks from fava.json_api.TreeReport
        self.assertIn("trees", data)
        self.assertIn("charts", data)

    def test_journal_range_filter(self):
        """GET /api/journal/?from=YYYY-MM-DD&to=YYYY-MM-DD -> list of entries."""
        end = date.today()
        start = end - timedelta(days=365)
        r = requests.get(
            api_url("journal/"),
            params={"from": start.isoformat(), "to": end.isoformat()},
            timeout=10,
        )
        self.assertEqual(r.status_code, 200)
        entries = r.json()
        self.assertIsInstance(entries, list)
        # Optional sanity: entries list contains dict-like items with a 'type'
        if entries:
            self.assertIsInstance(entries[0], dict)
            self.assertIn("type", entries[0])

    def test_disallow_post_on_readonly(self):
        """POST /api/commodities/ should not be allowed on read-only endpoint."""
        r = requests.post(api_url("commodities/"), json={}, timeout=10)
        self.assertIn(r.status_code, (404, 405))

if __name__ == "__main__":
    unittest.main()
