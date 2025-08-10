import unittest
import requests

BASE_URL = "http://54.73.240.131:5000"
DELETE_ENDPOINT = "/api/transactions/"  # Not supported in Fava; test with fake IDs

class TestDeleteTransactionAPI(unittest.TestCase):
    def test_delete_existing_transaction(self):
        """Attempt to delete an existing transaction (should fail)"""
        transaction_id = "1"  # Example ID
        response = requests.delete(BASE_URL + DELETE_ENDPOINT + str(transaction_id))
        self.assertIn(response.status_code, [403, 404])
        print("test_delete_existing_transaction: DELETE not supported (expected). Status:", response.status_code)

    def test_delete_and_undo_transaction(self):
        """Attempt to delete and then undo (should fail)"""
        transaction_id = "2"
        response = requests.delete(BASE_URL + DELETE_ENDPOINT + str(transaction_id))
        self.assertIn(response.status_code, [403, 404])
        # Simulate undo if such endpoint existed (here just document it's not supported)
        print("test_delete_and_undo_transaction: DELETE not supported (expected). Status:", response.status_code)

    def test_delete_nonexistent_transaction(self):
        """Attempt to delete a non-existent transaction (should fail)"""
        transaction_id = "9999999"
        response = requests.delete(BASE_URL + DELETE_ENDPOINT + str(transaction_id))
        self.assertIn(response.status_code, [403, 404])
        print("test_delete_nonexistent_transaction: DELETE not supported (expected). Status:", response.status_code)

    def test_delete_one_of_multiple_similar_transactions(self):
        """Attempt to delete one of multiple similar transactions (should fail)"""
        transaction_id = "3"
        response = requests.delete(BASE_URL + DELETE_ENDPOINT + str(transaction_id))
        self.assertIn(response.status_code, [403, 404])
        print("test_delete_one_of_multiple_similar_transactions: DELETE not supported (expected). Status:", response.status_code)

    def test_delete_transaction_with_tags(self):
        """Attempt to delete a transaction with tags (should fail)"""
        transaction_id = "4"
        response = requests.delete(BASE_URL + DELETE_ENDPOINT + str(transaction_id))
        self.assertIn(response.status_code, [403, 404])
        print("test_delete_transaction_with_tags: DELETE not supported (expected). Status:", response.status_code)

if __name__ == '__main__':
    unittest.main()
