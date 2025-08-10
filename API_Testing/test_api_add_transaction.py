import unittest
import requests

BASE_URL = "http://localhost:5000"
ENDPOINT = "/api/add-transaction"  # Not supported in Fava

class TestAddTransactionAPI(unittest.TestCase):
    def test_add_valid_transaction(self):
        """Try to add a valid transaction via API (should fail)"""
        payload = {
            "date": "2025-08-03",
            "narration": "Valid Add API Test",
            "postings": [
                {"account": "Assets:Cash", "amount": "100.00", "currency": "USD"},
                {"account": "Expenses:Test", "amount": "-100.00", "currency": "USD"},
            ]
        }
        response = requests.post(BASE_URL + ENDPOINT, json=payload)
        self.assertIn(response.status_code, [403, 404])
        print("test_add_valid_transaction: API POST not supported (expected). Status:", response.status_code)

    def test_add_transaction_missing_narration(self):
        """Try to add transaction missing narration (should fail)"""
        payload = {
            "date": "2025-08-03",
            "narration": "",
            "postings": [
                {"account": "Assets:Cash", "amount": "25.00", "currency": "USD"},
                {"account": "Expenses:Test", "amount": "-25.00", "currency": "USD"},
            ]
        }
        response = requests.post(BASE_URL + ENDPOINT, json=payload)
        self.assertIn(response.status_code, [403, 404])
        print("test_add_transaction_missing_narration: API POST not supported (expected). Status:", response.status_code)

    def test_add_transaction_invalid_date(self):
        """Try to add transaction with invalid date (should fail)"""
        payload = {
            "date": "2025-13-01",
            "narration": "Invalid date test",
            "postings": [
                {"account": "Assets:Cash", "amount": "10.00", "currency": "USD"},
                {"account": "Expenses:Test", "amount": "-10.00", "currency": "USD"},
            ]
        }
        response = requests.post(BASE_URL + ENDPOINT, json=payload)
        self.assertIn(response.status_code, [403, 404])
        print("test_add_transaction_invalid_date: API POST not supported (expected). Status:", response.status_code)

    def test_add_transaction_mismatched_amounts(self):
        """Try to add transaction with mismatched amounts (should fail)"""
        payload = {
            "date": "2025-08-03",
            "narration": "Mismatched amounts",
            "postings": [
                {"account": "Assets:Cash", "amount": "50.00", "currency": "USD"},
                {"account": "Expenses:Test", "amount": "-40.00", "currency": "USD"},
            ]
        }
        response = requests.post(BASE_URL + ENDPOINT, json=payload)
        self.assertIn(response.status_code, [403, 404])
        print("test_add_transaction_mismatched_amounts: API POST not supported (expected). Status:", response.status_code)

    def test_add_transaction_special_characters(self):
        """Try to add transaction with special characters (should fail)"""
        payload = {
            "date": "2025-08-03",
            "narration": "Lunch @ Café & Bar #2!",
            "postings": [
                {"account": "Assets:Cash", "amount": "17.00", "currency": "USD"},
                {"account": "Expenses:Dining", "amount": "-17.00", "currency": "USD"},
            ]
        }
        response = requests.post(BASE_URL + ENDPOINT, json=payload)
        self.assertIn(response.status_code, [403, 404])
        print("test_add_transaction_special_characters: API POST not supported (expected). Status:", response.status_code)

if __name__ == '__main__':
    unittest.main()
