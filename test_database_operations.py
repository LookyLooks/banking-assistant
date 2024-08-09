import unittest
import random
import string
from database_operations import *

class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        # Generate a unique username for each test
        self.unique_username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.unique_email = f"{self.unique_username}@example.com"
        # Create a test user
        self.test_user_id = create_user(self.unique_username, self.unique_email, "password_hash", "John", "Doe", "1234567890", True)
        print(f"Created test user with ID: {self.test_user_id}")  # Debug print

    def tearDown(self):
        # Clean up any created users
        if hasattr(self, 'test_user_id'):
            delete_user(self.test_user_id)
            print(f"Deleted test user with ID: {self.test_user_id}")  # Debug print

    def test_create_user(self):
        new_username = f"new_{self.unique_username}"
        new_email = f"new_{self.unique_email}"
        user_id = create_user(new_username, new_email, "password_hash", "Jane", "Doe", "0987654321", False)
        self.assertIsNotNone(user_id, "Failed to create a new user")
        if user_id:
            delete_user(user_id)

    def test_get_user(self):
        self.assertIsNotNone(self.test_user_id, "Failed to create test user in setUp")
        user = get_user(self.test_user_id)
        self.assertIsNotNone(user, f"Failed to get user with ID {self.test_user_id}")
        self.assertEqual(user['username'], self.unique_username)
        self.assertEqual(user['email'], self.unique_email)
        self.assertEqual(user['first_name'], "John")
        self.assertEqual(user['last_name'], "Doe")

    def test_update_user(self):
        result = update_user(1, username="updateduser")
        self.assertEqual(result, 1)

    def test_delete_user(self):
        # Create a new user specifically for this test
        temp_user_id = create_user(f"temp_{self.unique_username}", f"temp_{self.unique_email}", "password_hash", "Temp", "User", "9876543210", False)
        self.assertIsNotNone(temp_user_id)

        result = delete_user(temp_user_id)
        self.assertEqual(result, 1)
        deleted_user = get_user(temp_user_id)
        self.assertIsNone(deleted_user)

    def test_list_users(self):
        users = list_users()
        self.assertIsInstance(users, list)

    # Accounts CRUD operations tests
    def test_create_account(self):
        account_id = create_account(1, 1000.00, "savings", "USD")
        self.assertIsNotNone(account_id)

    def test_get_account(self):
        if self.test_user_id is None:
            self.skipTest("Failed to create test user")
        print(f"Test user ID: {self.test_user_id}")  # Debug print
        account_id = create_account(self.test_user_id, 1000.00, "savings", "USD")
        print(f"Created account with ID: {account_id}")  # Debug print
        self.assertIsNotNone(account_id, "Failed to create account")
        
        account = get_account(account_id)
        print(f"Retrieved account: {account}")  # Debug print
        self.assertIsNotNone(account, f"Failed to retrieve account with ID {account_id}")
        
        self.assertEqual(account['account_type'], "savings")
        self.assertEqual(float(account['balance']), 1000.00)
        self.assertEqual(account['currency'], "USD")

    def test_update_account(self):
        result = update_account(1, balance=2000.00)
        self.assertEqual(result, 1)

    def test_delete_account(self):
        # Create a test account
        account_id = create_account(self.test_user_id, 1000.00, "savings", "USD")
        self.assertIsNotNone(account_id, "Failed to create test account")

        # Try to delete the account
        result = delete_account(account_id)
        self.assertEqual(result, 1, f"Failed to delete account with ID {account_id}")

        # Verify the account no longer exists
        deleted_account = get_account(account_id)
        self.assertIsNone(deleted_account, f"Account with ID {account_id} still exists after deletion")

    def test_list_accounts(self):
        accounts = list_accounts()
        self.assertIsInstance(accounts, list)

    # Transactions CRUD operations tests
    def test_create_transaction(self):
        transaction_id = create_transaction(1, 2, 100.00, "USD", "completed", "transfer", "Test transaction")
        self.assertIsNotNone(transaction_id)

    def test_get_transaction(self):
        # Create two test accounts
        sender_account_id = create_account(self.test_user_id, 1000.00, "savings", "USD")
        recipient_account_id = create_account(self.test_user_id, 500.00, "checking", "USD")
        
        # Create a test transaction
        transaction_id = create_transaction(sender_account_id, recipient_account_id, 100.00, "USD", "completed", "transfer", "Test transaction")
        self.assertIsNotNone(transaction_id, "Failed to create test transaction")

        # Retrieve the transaction
        transaction = get_transaction(transaction_id)
        self.assertIsNotNone(transaction, f"Failed to retrieve transaction with ID {transaction_id}")
        self.assertEqual(transaction['status'], "completed")
        self.assertEqual(float(transaction['amount']), 100.00)
        self.assertEqual(transaction['currency'], "USD")
        self.assertEqual(transaction['transaction_type'], "transfer")
        self.assertEqual(transaction['description'], "Test transaction")

    def test_update_transaction(self):
        # Create two test accounts
        sender_account_id = create_account(self.test_user_id, 1000.00, "savings", "USD")
        recipient_account_id = create_account(self.test_user_id, 500.00, "checking", "USD")
        
        # Create a test transaction
        transaction_id = create_transaction(sender_account_id, recipient_account_id, 100.00, "USD", "completed", "transfer", "Test transaction")
        self.assertIsNotNone(transaction_id, "Failed to create test transaction")

        # Update the transaction
        result = update_transaction(transaction_id, status="pending")
        self.assertEqual(result, 1, f"Failed to update transaction with ID {transaction_id}")

        # Verify the update
        updated_transaction = get_transaction(transaction_id)
        self.assertIsNotNone(updated_transaction, f"Failed to retrieve updated transaction with ID {transaction_id}")
        self.assertEqual(updated_transaction['status'], "pending")
    
    def test_delete_transaction(self):
        # Create two test accounts
        sender_account_id = create_account(self.test_user_id, 1000.00, "savings", "USD")
        recipient_account_id = create_account(self.test_user_id, 500.00, "checking", "USD")
        
        # Create a test transaction
        transaction_id = create_transaction(sender_account_id, recipient_account_id, 100.00, "USD", "completed", "transfer", "Test transaction")
        self.assertIsNotNone(transaction_id, "Failed to create test transaction")

        # Delete the transaction
        result = delete_transaction(transaction_id)
        self.assertEqual(result, 1, f"Failed to delete transaction with ID {transaction_id}")

        # Verify the transaction no longer exists
        deleted_transaction = get_transaction(transaction_id)
        self.assertIsNone(deleted_transaction, f"Transaction with ID {transaction_id} still exists after deletion")

    def test_list_transactions(self):
        transactions = list_transactions()
        self.assertIsInstance(transactions, list)
    
    # Recipients CRUD operations tests
    def test_create_recipient(self):
        recipient_id = create_recipient(1, "Jane Doe", "123456789", "Test Bank", "TESTSWIFT", "friend", True)
        self.assertIsNotNone(recipient_id)

    def test_get_recipient(self):
        # Create a test recipient
        recipient_id = create_recipient(self.test_user_id, "Jane Doe", "123456789", "Test Bank", "TESTSWIFT", "friend", True)
        self.assertIsNotNone(recipient_id, "Failed to create test recipient")

        # Retrieve the recipient
        recipient = get_recipient(recipient_id)
        self.assertIsNotNone(recipient, f"Failed to retrieve recipient with ID {recipient_id}")
        self.assertEqual(recipient['name'], "Jane Doe")
        self.assertEqual(recipient['account_info'], "123456789")
        self.assertEqual(recipient['bank_name'], "Test Bank")
        self.assertEqual(recipient['swift_code'], "TESTSWIFT")
        self.assertEqual(recipient['relationship'], "friend")
        self.assertTrue(recipient['is_favorite'])

    def test_update_recipient(self):
        # Create a test recipient
        recipient_id = create_recipient(self.test_user_id, "Jane Doe", "123456789", "Test Bank", "TESTSWIFT", "friend", True)
        self.assertIsNotNone(recipient_id, "Failed to create test recipient")

        # Update the recipient
        new_name = "John Smith"
        result = update_recipient(recipient_id, name=new_name)
        self.assertEqual(result, 1, f"Failed to update recipient with ID {recipient_id}")

        # Verify the update
        updated_recipient = get_recipient(recipient_id)
        self.assertIsNotNone(updated_recipient, f"Failed to retrieve updated recipient with ID {recipient_id}")
        self.assertEqual(updated_recipient['name'], new_name)

    def test_delete_recipient(self):
        # Create a test recipient
        recipient_id = create_recipient(self.test_user_id, "Jane Doe", "123456789", "Test Bank", "TESTSWIFT", "friend", True)
        self.assertIsNotNone(recipient_id, "Failed to create test recipient")

        # Delete the recipient
        result = delete_recipient(recipient_id)
        self.assertEqual(result, 1, f"Failed to delete recipient with ID {recipient_id}")

        # Verify the recipient no longer exists
        deleted_recipient = get_recipient(recipient_id)
        self.assertIsNone(deleted_recipient, f"Recipient with ID {recipient_id} still exists after deletion")

    def test_get_all_recipients(self):
        recipients = get_all_recipients(1)  # Assuming user with ID 1 exists
        self.assertIsInstance(recipients, list)

    def test_get_favorite_recipients(self):
        favorites = get_favorite_recipients(1)  # Assuming user with ID 1 exists
        self.assertIsInstance(favorites, list)
    
    def test_toggle_favorite_recipient(self):
        # Create a test recipient
        recipient_id = create_recipient(self.test_user_id, "Jane Doe", "123456789", "Test Bank", "TESTSWIFT", "friend", False)
        self.assertIsNotNone(recipient_id, "Failed to create test recipient")

        # Toggle favorite status
        result = toggle_favorite_recipient(recipient_id)
        self.assertTrue(result, "Failed to toggle favorite status")

        # Verify the change
        updated_recipient = get_recipient(recipient_id)
        self.assertIsNotNone(updated_recipient, f"Failed to retrieve updated recipient with ID {recipient_id}")
        self.assertTrue(updated_recipient['is_favorite'], "Favorite status was not toggled to True")

        # Toggle favorite status again
        result = toggle_favorite_recipient(recipient_id)
        self.assertFalse(result, "Failed to toggle favorite status back")

        # Verify the change again
        updated_recipient = get_recipient(recipient_id)
        self.assertIsNotNone(updated_recipient, f"Failed to retrieve updated recipient with ID {recipient_id}")
        self.assertFalse(updated_recipient['is_favorite'], "Favorite status was not toggled back to False")

if __name__ == '__main__':
    unittest.main()    