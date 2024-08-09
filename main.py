from fastapi import FastAPI, HTTPException, Depends
from typing import List
import database_operations as db_ops
from schemas import *

app = FastAPI()

# User endpoints
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    user_id = db_ops.create_user(
        username=user.username,
        email=user.email,
        password_hash=user.password,  # Note: In a real app, you should hash the password
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        is_verified=user.is_verified
    )
    if user_id is None:
        raise HTTPException(status_code=400, detail="User creation failed")
    return db_ops.get_user(user_id)

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user = db_ops.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=UserList)
async def list_users():
    users = db_ops.list_users()
    return UserList(users=users)

@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserUpdate):
    update_data = user_update.dict(exclude_unset=True)
    rows_affected = db_ops.update_user(user_id, **update_data)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return db_ops.get_user(user_id)

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    rows_affected = db_ops.delete_user(user_id)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Account endpoints

@app.post("/accounts/", response_model=AccountResponse)
async def create_account(account: AccountCreate):
    account_id = db_ops.create_account(
        user_id=account.user_id,
        balance=account.balance,
        account_type=account.account_type,
        currency=account.currency
    )
    if account_id is None:
        raise HTTPException(status_code=400, detail="Account creation failed")
    return db_ops.get_account(account_id)

@app.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int):
    account = db_ops.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.get("/accounts/", response_model=AccountList)
async def list_accounts():
    accounts = db_ops.list_accounts()
    return AccountList(accounts=accounts)

@app.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, account_update: AccountUpdate):
    update_data = account_update.dict(exclude_unset=True)
    # Convert Decimal to float for database operation
    if 'balance' in update_data:
        update_data['balance'] = float(update_data['balance'])
    rows_affected = db_ops.update_account(account_id, **update_data)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_ops.get_account(account_id)

@app.delete("/accounts/{account_id}", response_model=AccountDelete)
async def delete_account(account_id: int):
    rows_affected = db_ops.delete_account(account_id)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountDelete(deleted=True, message="Account deleted successfully")


# Transaction endpoints

@app.post("/transactions/", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    transaction_id = db_ops.create_transaction(
        sender_account_id=transaction.sender_account_id,
        recipient_account_id=transaction.recipient_account_id,
        amount=transaction.amount,
        currency=transaction.currency,
        status=transaction.status,
        transaction_type=transaction.transaction_type,
        description=transaction.description
    )
    if transaction_id is None:
        raise HTTPException(status_code=400, detail="Transaction creation failed")
    return db_ops.get_transaction(transaction_id)

@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    transaction = db_ops.get_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.get("/transactions/", response_model=TransactionList)
async def list_transactions():
    transactions = db_ops.list_transactions()
    return TransactionList(transactions=transactions)

@app.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(transaction_id: int, transaction_update: TransactionUpdate):
    update_data = transaction_update.dict(exclude_unset=True)
    # Convert Decimal to float for database operation
    if 'amount' in update_data:
        update_data['amount'] = float(update_data['amount'])
    rows_affected = db_ops.update_transaction(transaction_id, **update_data)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_ops.get_transaction(transaction_id)

@app.delete("/transactions/{transaction_id}", response_model=dict)
async def delete_transaction(transaction_id: int):
    rows_affected = db_ops.delete_transaction(transaction_id)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}


# Recipient endpoints

@app.post("/recipients/", response_model=RecipientResponse)
async def create_recipient(recipient: RecipientCreate):
    recipient_id = db_ops.create_recipient(
        user_id=recipient.user_id,
        name=recipient.name,
        account_info=recipient.account_info,
        bank_name=recipient.bank_name,
        swift_code=recipient.swift_code,
        relationship=recipient.relationship,
        is_favorite=recipient.is_favorite
    )
    if recipient_id is None:
        raise HTTPException(status_code=400, detail="Recipient creation failed")
    return db_ops.get_recipient(recipient_id)

@app.get("/recipients/{recipient_id}", response_model=RecipientResponse)
async def get_recipient(recipient_id: int):
    recipient = db_ops.get_recipient(recipient_id)
    if recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return recipient

@app.put("/recipients/{recipient_id}", response_model=RecipientResponse)
async def update_recipient(recipient_id: int, recipient_update: RecipientUpdate):
    update_data = recipient_update.dict(exclude_unset=True)
    rows_affected = db_ops.update_recipient(recipient_id, **update_data)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return db_ops.get_recipient(recipient_id)

@app.delete("/recipients/{recipient_id}", response_model=dict)
async def delete_recipient(recipient_id: int):
    rows_affected = db_ops.delete_recipient(recipient_id)
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return {"message": "Recipient deleted successfully"}

@app.get("/users/{user_id}/recipients/", response_model=RecipientList)
async def get_all_recipients(user_id: int):
    recipients = db_ops.get_all_recipients(user_id)
    return RecipientList(recipients=recipients)

@app.get("/users/{user_id}/recipients/favorites/", response_model=RecipientList)
async def get_favorite_recipients(user_id: int):
    recipients = db_ops.get_favorite_recipients(user_id)
    return RecipientList(recipients=recipients)

@app.post("/recipients/{recipient_id}/toggle-favorite", response_model=FavoriteToggleResponse)
async def toggle_favorite_recipient(recipient_id: int):
    is_favorite = db_ops.toggle_favorite_recipient(recipient_id)
    if is_favorite is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return FavoriteToggleResponse(recipient_id=recipient_id, is_favorite=is_favorite)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)