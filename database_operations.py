import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect("postgresql://postgres:123456@localhost:5432/postgres")

def create_user(username, email, password_hash, first_name, last_name, phone_number, is_verified):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO transfer.Users (username, email, password_hash, first_name, last_name, phone_number, is_verified)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING user_id;
                """, (username, email, password_hash, first_name, last_name, phone_number, is_verified))
                user_id = cur.fetchone()[0]
                conn.commit()
                print(f"Created user with ID: {user_id}")  # Debug print
                return user_id
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                print(f"User with username {username} or email {email} already exists")
                return None
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error creating user: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return None

def get_user(user_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Users WHERE user_id = %s", (user_id,))
            return cur.fetchone()

def list_users():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Users")
            return cur.fetchall()

def update_user(user_id, **kwargs):
    set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
    values = list(kwargs.values()) + [user_id]
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                UPDATE transfer.Users
                SET {set_clause}
                WHERE user_id = %s
            """, values)
            return cur.rowcount

def delete_user(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                # First, delete related transactions
                cur.execute("DELETE FROM transfer.Transactions WHERE sender_account_id IN (SELECT account_id FROM transfer.Accounts WHERE user_id = %s) OR recipient_account_id IN (SELECT account_id FROM transfer.Accounts WHERE user_id = %s)", (user_id, user_id))
                
                # Then, delete related accounts
                cur.execute("DELETE FROM transfer.Accounts WHERE user_id = %s", (user_id,))
                
                # Finally, delete the user
                cur.execute("DELETE FROM transfer.Users WHERE user_id = %s", (user_id,))
                
                conn.commit()
                return cur.rowcount
            except psycopg2.Error as e:
                conn.rollback()
                print(f"An error occurred: {e}")
                return 0

def list_users():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Users")
            return cur.fetchall()


# Accounts CRUD operations
def create_account(user_id, balance, account_type, currency):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO transfer.Accounts (user_id, balance, account_type, currency)
                VALUES (%s, %s, %s, %s)
                RETURNING account_id;
            """, (user_id, balance, account_type, currency))
            return cur.fetchone()[0]

def get_account(account_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                cur.execute("SELECT * FROM transfer.Accounts WHERE account_id = %s", (account_id,))
                account = cur.fetchone()
                print(f"Retrieved account: {account}")  # Debug print
                return account
            except psycopg2.Error as e:
                print(f"Error getting account: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return None

def update_account(account_id, **kwargs):
    set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
    values = list(kwargs.values()) + [account_id]
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                UPDATE transfer.Accounts
                SET {set_clause}
                WHERE account_id = %s
            """, values)
            return cur.rowcount

def delete_account(account_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                # First, delete related transactions
                cur.execute("""
                    DELETE FROM transfer.Transactions 
                    WHERE sender_account_id = %s OR recipient_account_id = %s
                """, (account_id, account_id))
                
                # Then, delete the account
                cur.execute("DELETE FROM transfer.Accounts WHERE account_id = %s", (account_id,))
                
                conn.commit()
                return cur.rowcount
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error deleting account: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return 0

def list_accounts():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Accounts")
            return cur.fetchall()

# Transactions CRUD
def create_transaction(sender_account_id, recipient_account_id, amount, currency, status, transaction_type, description):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO transfer.Transactions 
                    (sender_account_id, recipient_account_id, amount, currency, status, transaction_type, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING transaction_id;
                """, (sender_account_id, recipient_account_id, amount, currency, status, transaction_type, description))
                transaction_id = cur.fetchone()[0]
                conn.commit()
                print(f"Created transaction with ID: {transaction_id}")  # Debug print
                return transaction_id
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error creating transaction: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return None

def get_transaction(transaction_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Transactions WHERE transaction_id = %s", (transaction_id,))
            return cur.fetchone()

def update_transaction(transaction_id, **kwargs):
    set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
    values = list(kwargs.values()) + [transaction_id]
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    UPDATE transfer.Transactions
                    SET {set_clause}
                    WHERE transaction_id = %s
                """, values)
                conn.commit()
                return cur.rowcount
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error updating transaction: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return 0

def delete_transaction(transaction_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM transfer.Transactions WHERE transaction_id = %s", (transaction_id,))
                conn.commit()
                return cur.rowcount
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error deleting transaction: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return 0

def list_transactions():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Transactions")
            return cur.fetchall()

# Recipient CRUD
def create_recipient(user_id, name, account_info, bank_name, swift_code, relationship, is_favorite):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO transfer.Recipients 
                    (user_id, name, account_info, bank_name, swift_code, relationship, is_favorite)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING recipient_id;
                """, (user_id, name, account_info, bank_name, swift_code, relationship, is_favorite))
                recipient_id = cur.fetchone()[0]
                conn.commit()
                print(f"Created recipient with ID: {recipient_id}")  # Debug print
                return recipient_id
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error creating recipient: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return None

def get_recipient(recipient_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                cur.execute("SELECT * FROM transfer.Recipients WHERE recipient_id = %s", (recipient_id,))
                recipient = cur.fetchone()
                print(f"Retrieved recipient: {recipient}")  # Debug print
                return recipient
            except psycopg2.Error as e:
                print(f"Error getting recipient: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return None

def update_recipient(recipient_id, **kwargs):
    set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
    values = list(kwargs.values()) + [recipient_id]
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"""
                    UPDATE transfer.Recipients
                    SET {set_clause}
                    WHERE recipient_id = %s
                """, values)
                conn.commit()
                return cur.rowcount
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error updating recipient: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return 0

def delete_recipient(recipient_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM transfer.Recipients WHERE recipient_id = %s", (recipient_id,))
                conn.commit()
                return cur.rowcount
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error deleting recipient: {e}")
                print(f"Error details: {e.diag.message_detail}")
                return 0

def get_all_recipients(user_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Recipients WHERE user_id = %s", (user_id,))
            return cur.fetchall()

def get_favorite_recipients(user_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM transfer.Recipients WHERE user_id = %s AND is_favorite = TRUE", (user_id,))
            return cur.fetchall()

def toggle_favorite_recipient(recipient_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE transfer.Recipients
                SET is_favorite = NOT is_favorite
                WHERE recipient_id = %s
                RETURNING is_favorite
            """, (recipient_id,))
            return cur.fetchone()[0]