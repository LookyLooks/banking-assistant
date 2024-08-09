import unittest
from datetime import datetime
from pydantic import ValidationError
from schemas import (
    UserBase, 
    UserCreate, 
    UserUpdate, 
    UserInDB, 
    UserOut, 
    UserList,
    AccountType,
    Currency,
    AccountCreate,
    AccountResponse,
    AccountUpdate,
    AccountList,
    AccountDelete,
    TransactionBase,
    TransactionCreate,
    TransactionUpdate,
    TransactionInDB,
    Transaction,
    TransactionList,
    RelationshipType,
    RecipientBase,
    RecipientCreate,
    RecipientUpdate,
    RecipientInDB,
    RecipientResponse,
    RecipientList,
    FavoriteToggleResponse,
    )
from decimal import Decimal 

class TestSchemas(unittest.TestCase):

    # User Tests
    
    def test_user_base(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
            "is_verified": True
        }
        user = UserBase(**user_data)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone_number, "1234567890")
        self.assertTrue(user.is_verified)

    def test_user_create(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
            "password": "securepassword"
            }
        user = UserCreate(**user_data)
        self.assertEqual(user.password, "securepassword")

    def test_user_update(self):
        user_data = {
            "username": "updateduser",
            "email": "updated@example.com"
            }
        user = UserUpdate(**user_data)
        self.assertEqual(user.username, "updateduser")
        self.assertEqual(user.email, "updated@example.com")
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)

    def test_user_in_db(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
            "is_verified": True,
            "user_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "password_hash": "hashedpassword"
        }
        user = UserInDB(**user_data)
        self.assertEqual(user.user_id, 1)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
        self.assertEqual(user.password_hash, "hashedpassword")

    def test_user_out(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "1234567890",
            "is_verified": True,
            "user_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
            }
        user = UserOut(**user_data)
        self.assertEqual(user.user_id, 1)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_user_list(self):
        users_data = {
            "users": [
                {
                "username": "user1",
                "email": "user1@example.com",
                "first_name": "User",
                "last_name": "One",
                "phone_number": "1234567890",
                "is_verified": True,
                "user_id": 1,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
                },
                {
                "username": "user2",
                "email": "user2@example.com",
                "first_name": "User",
                "last_name": "Two",
                "phone_number": "0987654321",
                "is_verified": False,
                "user_id": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
                }
            ]
            }
        user_list = UserList(**users_data)
        self.assertEqual(len(user_list.users), 2)
        self.assertEqual(user_list.users[0].username, "user1")
        self.assertEqual(user_list.users[1].username, "user2")

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            UserBase(username="testuser", email="invalid_email", first_name="Test", last_name="User", phone_number="1234567890")

    # Accounts Tests

    def test_account_create(self):  # Add self parameter
        account = AccountCreate(
            user_id=1,
            balance=Decimal("100.00"),
            account_type=AccountType.CHECKING,
            currency=Currency.USD
        )
        self.assertEqual(account.user_id, 1)
        self.assertEqual(account.balance, Decimal("100.00"))
        self.assertEqual(account.account_type, AccountType.CHECKING)
        self.assertEqual(account.currency, Currency.USD)

    def test_account_create_invalid_balance(self):  # Add self parameter
        with self.assertRaises(ValidationError):
            AccountCreate(
                user_id=1,
                balance=Decimal("-100.00"),
                account_type=AccountType.SAVINGS,
                currency=Currency.EUR
            )

    def test_account_response(self):  # Add self parameter
        response = AccountResponse(
            account_id=1,
            user_id=1,
            balance=Decimal("200.00"),
            account_type=AccountType.SAVINGS,
            currency=Currency.GBP
        )
        self.assertEqual(response.account_id, 1)
        self.assertEqual(response.user_id, 1)
        self.assertEqual(response.balance, Decimal("200.00"))
        self.assertEqual(response.account_type, AccountType.SAVINGS)
        self.assertEqual(response.currency, Currency.GBP)

    def test_account_update(self):
        update = AccountUpdate(balance=Decimal("300.00"), account_type=AccountType.CREDIT)
        assert update.balance == Decimal("300.00")
        assert update.account_type == AccountType.CREDIT
        assert update.currency is None

    def test_account_update_partial(self):
        update = AccountUpdate(balance=Decimal("400.00"))
        assert update.balance == Decimal("400.00")
        assert update.account_type is None
        assert update.currency is None

    def test_account_list(self):
        accounts = [
            AccountResponse(
                account_id=1,
                user_id=1,
                balance=Decimal("100.00"),
                account_type=AccountType.CHECKING,
                currency=Currency.USD
            ),
            AccountResponse(
                account_id=2,
                user_id=1,
                balance=Decimal("200.00"),
                account_type=AccountType.SAVINGS,
                currency=Currency.EUR
            )
        ]
        account_list = AccountList(accounts=accounts)
        assert len(account_list.accounts) == 2
        assert account_list.accounts[0].account_id == 1
        assert account_list.accounts[1].account_id == 2

    def test_account_delete(self):
        delete = AccountDelete(deleted=True, message="Account successfully deleted")
        assert delete.deleted is True
        assert delete.message == "Account successfully deleted"

    def test_account_type_enum(self):
        assert AccountType.CHECKING == "checking"
        assert AccountType.SAVINGS == "savings"
        assert AccountType.CREDIT == "credit"

    def test_currency_enum(self):
        assert Currency.USD == "USD"
        assert Currency.EUR == "EUR"
        assert Currency.GBP == "GBP"
        assert Currency.JPY == "JPY"

    # Transactions Tests

    def test_transaction_base(self):
        transaction = TransactionBase(
            sender_account_id=1,
            recipient_account_id=2,
            amount=Decimal("100.00"),
            currency="USD",
            status="pending",
            transaction_type="transfer"
        )
        self.assertEqual(transaction.sender_account_id, 1)
        self.assertEqual(transaction.recipient_account_id, 2)
        self.assertEqual(transaction.amount, Decimal("100.00"))
        self.assertEqual(transaction.currency, "USD")
        self.assertEqual(transaction.status, "pending")
        self.assertEqual(transaction.transaction_type, "transfer")
        self.assertIsNone(transaction.description)
    
    def test_transaction_create(self):
        transaction = TransactionCreate(
            sender_account_id=1,
            recipient_account_id=2,
            amount=Decimal("100.00"),
            currency="USD",
            status="pending",
            transaction_type="transfer",
            description="Test transfer"
        )
        self.assertEqual(transaction.description, "Test transfer")

    def test_transaction_update(self):
        transaction = TransactionUpdate(amount=Decimal("200.00"), status="completed")
        self.assertEqual(transaction.amount, Decimal("200.00"))
        self.assertEqual(transaction.status, "completed")
        self.assertIsNone(transaction.sender_account_id)

    def test_transaction_in_db(self):
        transaction = TransactionInDB(
            transaction_id=1,
            sender_account_id=1,
            recipient_account_id=2,
            amount=Decimal("100.00"),
            currency="USD",
            status="completed",
            transaction_type="transfer",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.assertEqual(transaction.transaction_id, 1)
        self.assertIsInstance(transaction.created_at, datetime)
        self.assertIsInstance(transaction.updated_at, datetime)

    def test_transaction(self):
        transaction = Transaction(
            transaction_id=1,
            sender_account_id=1,
            recipient_account_id=2,
            amount=Decimal("100.00"),
            currency="USD",
            status="completed",
            transaction_type="transfer",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.assertEqual(transaction.transaction_id, 1)

    def test_transaction_list(self):
        transaction1 = Transaction(
            transaction_id=1,
            sender_account_id=1,
            recipient_account_id=2,
            amount=Decimal("100.00"),
            currency="USD",
            status="completed",
            transaction_type="transfer",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        transaction2 = Transaction(
            transaction_id=2,
            sender_account_id=2,
            recipient_account_id=1,
            amount=Decimal("50.00"),
            currency="USD",
            status="pending",
            transaction_type="transfer",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        transaction_list = TransactionList(transactions=[transaction1, transaction2])
        self.assertIsInstance(transaction_list, TransactionList)
        self.assertEqual(len(transaction_list.transactions), 2)
        self.assertEqual(transaction_list.transactions[0].transaction_id, 1)
        self.assertEqual(transaction_list.transactions[1].transaction_id, 2)

    def test_invalid_amount(self):
        with self.assertRaises(ValidationError):
            TransactionBase(
                sender_account_id=1,
                recipient_account_id=2,
                amount=Decimal("-100.00"),  # Invalid negative amount
                currency="USD",
                status="pending",
                transaction_type="transfer"
            )
    
    def test_missing_required_field(self):
        with self.assertRaises(ValidationError):
            TransactionBase(
                sender_account_id=1,
                recipient_account_id=2,
                # Missing required 'amount' field
                currency="USD",
                status="pending",
                transaction_type="transfer"
            )

    # Recipient Tests

    def test_recipient_base(self):
        recipient = RecipientBase(
            name="John Doe",
            account_info="123456789",
            bank_name="Test Bank",
            swift_code="TESTSWIFT",
            relationship=RelationshipType.FRIEND,
        )
        self.assertEqual(recipient.name, "John Doe")
        self.assertEqual(recipient.account_info, "123456789")
        self.assertEqual(recipient.bank_name, "Test Bank")
        self.assertEqual(recipient.swift_code, "TESTSWIFT")
        self.assertEqual(recipient.relationship, RelationshipType.FRIEND)
        self.assertFalse(recipient.is_favorite)
    
    def test_recipient_base_validation(self):
        with self.assertRaises(ValidationError):
            RecipientBase(
                name="",  # Empty name
                account_info="123456789",
                bank_name="Test Bank",
                swift_code="TESTSWIFT",
                relationship=RelationshipType.FRIEND,
            )

        with self.assertRaises(ValidationError):
            RecipientBase(
                name="John Doe",
                account_info="123456789",
                bank_name="Test Bank",
                swift_code="SHORT",  # Too short swift code
                relationship=RelationshipType.FRIEND,
            )
    
    def test_recipient_create(self):
        recipient = RecipientCreate(
            name="John Doe",
            account_info="123456789",
            bank_name="Test Bank",
            swift_code="TESTSWIFT",
            relationship=RelationshipType.FRIEND,
            user_id=1,
        )
        self.assertEqual(recipient.user_id, 1)

    def test_recipient_update(self):
        recipient = RecipientUpdate(name="Jane Doe", is_favorite=True)
        self.assertEqual(recipient.name, "Jane Doe")
        self.assertTrue(recipient.is_favorite)
        self.assertIsNone(recipient.account_info)

    def test_recipient_in_db(self):
        recipient = RecipientInDB(
            name="John Doe",
            account_info="123456789",
            bank_name="Test Bank",
            swift_code="TESTSWIFT",
            relationship=RelationshipType.FRIEND,
            recipient_id=1,
            user_id=1,
        )
        self.assertEqual(recipient.recipient_id, 1)
        self.assertEqual(recipient.user_id, 1)

    def test_recipient_response(self):
        recipient = RecipientResponse(
            name="John Doe",
            account_info="123456789",
            bank_name="Test Bank",
            swift_code="TESTSWIFT",
            relationship=RelationshipType.FRIEND,
            recipient_id=1,
            user_id=1,
        )
        self.assertEqual(recipient.recipient_id, 1)
        self.assertEqual(recipient.user_id, 1)
    
    def test_recipient_list(self):
        recipient1 = RecipientResponse(
            name="John Doe",
            account_info="123456789",
            bank_name="Test Bank",
            swift_code="TESTSWIFT",
            relationship=RelationshipType.FRIEND,
            recipient_id=1,
            user_id=1,
        )
        recipient2 = RecipientResponse(
            name="Jane Doe",
            account_info="987654321",
            bank_name="Another Bank",
            swift_code="ANOTHERSWI",  # Changed to 11 characters
            relationship=RelationshipType.FAMILY,
            recipient_id=2,
            user_id=1,
        )
        recipient_list = RecipientList(recipients=[recipient1, recipient2])
        self.assertEqual(len(recipient_list.recipients), 2)
        self.assertEqual(recipient_list.recipients[0].name, "John Doe")
        self.assertEqual(recipient_list.recipients[1].name, "Jane Doe")
    
    def test_favorite_toggle_response(self):
        response = FavoriteToggleResponse(recipient_id=1, is_favorite=True)
        self.assertEqual(response.recipient_id, 1)
        self.assertTrue(response.is_favorite)




if __name__ == '__main__':
    unittest.main()