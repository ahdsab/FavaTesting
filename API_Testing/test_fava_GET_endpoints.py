import unittest
import requests

BASE = "http://54.73.240.131:5001/example-beancount-file/api"

def get_json(path, params=None, timeout=15):
    # Try without slash, then once with slash if 404.
    r = requests.get(f"{BASE}{path}", params=params, timeout=timeout)
    if r.status_code == 404 and not path.endswith("/"):
        r = requests.get(f"{BASE}{path}/", params=params, timeout=timeout)
    return r

def extract_data(j):
    # Accept both {success, data} and raw list/dict responses.
    if isinstance(j, dict) and "data" in j:
        return j["data"]
    return j

class TestFavaSimpleGET(unittest.TestCase):
    def test_options(self):
        r = get_json("/options", timeout=10)
        self.assertEqual(r.status_code, 200, r.text)
        data = extract_data(r.json())
        self.assertIsInstance(data, dict)
        self.assertIn("fava_options", data)
        self.assertIn("beancount_options", data)

    def test_journal_range(self):
        params = {"from": "2017-06-01", "to": "2017-06-30"}
        r = get_json("/journal", params=params, timeout=15)
        self.assertEqual(r.status_code, 200, r.text)
        data = extract_data(r.json())
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        # Entries should look like dicts with at least a type/date
        self.assertIsInstance(data[0], dict)
        self.assertTrue("t" in data[0] or "type" in data[0])

    def test_narrations(self):
        r = get_json("/narrations", timeout=10)
        self.assertEqual(r.status_code, 200, r.text)
        data = extract_data(r.json())
        self.assertIsInstance(data, list)
        self.assertTrue(any(isinstance(x, str) for x in data))

    def test_payee_accounts(self):
        r = get_json("/payee_accounts", params={"payee": "Starbucks"}, timeout=10)
        self.assertEqual(r.status_code, 200, r.text)
        data = extract_data(r.json())
        self.assertIsInstance(data, list)

    def test_query_balance_assets(self):
        q = 'SELECT account, sum(position) WHERE account ~ "Assets" GROUP BY 1'
        r = get_json("/query", params={"query_string": q}, timeout=15)
        self.assertEqual(r.status_code, 200, r.text)
        data = extract_data(r.json())
        # Accept table-shaped dict or text output depending on config
        self.assertTrue(isinstance(data, dict) or isinstance(data, str))

if __name__ == "__main__":
    unittest.main()
