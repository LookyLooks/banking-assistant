from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from decimal import Decimal 

# USER SCHEMAS

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    is_verified: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_verified: Optional[bool] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    password_hash: str

    class Config:
        orm_mode = True

class UserOut(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserList(BaseModel):
    users: list[UserOut]

    class Config:
        orm_mode = True

# Accounts SCHEMAS

class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"

class AccountCreate(BaseModel):
    user_id: int
    balance: Decimal = Field(..., ge=0)
    account_type: AccountType
    currency: Currency

class AccountResponse(BaseModel):
    account_id: int
    user_id: int
    balance: Decimal
    account_type: AccountType
    currency: Currency

class AccountUpdate(BaseModel):
    balance: Optional[Decimal] = Field(None, ge=0)
    account_type: Optional[AccountType] = None
    currency: Optional[Currency] = None

class AccountList(BaseModel):
    accounts: List[AccountResponse]

class AccountDelete(BaseModel):
    deleted: bool
    message: str

# Transaction Schemas

class TransactionBase(BaseModel):
    sender_account_id: int
    recipient_account_id: int
    amount: Decimal = Field(..., ge=0)
    currency: str
    status: str
    transaction_type: str
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    sender_account_id: Optional[int] = None
    recipient_account_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    status: Optional[str] = None
    transaction_type: Optional[str] = None
    description: Optional[str] = None

class TransactionInDB(TransactionBase):
    transaction_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Transaction(TransactionInDB):
    pass

class TransactionList(BaseModel):
    transactions: list[Transaction]

# Recipients Schemas

class RelationshipType(str, Enum):
    FAMILY = "family"
    FRIEND = "friend"
    BUSINESS = "business"
    OTHER = "other"

class RecipientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    account_info: str = Field(..., min_length=1, max_length=100)
    bank_name: str = Field(..., min_length=1, max_length=100)
    swift_code: str = Field(..., min_length=8, max_length=11)
    relationship: RelationshipType
    is_favorite: bool = False

class RecipientCreate(RecipientBase):
    user_id: int

class RecipientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    account_info: Optional[str] = Field(None, min_length=1, max_length=100)
    bank_name: Optional[str] = Field(None, min_length=1, max_length=100)
    swift_code: Optional[str] = Field(None, min_length=8, max_length=11)
    relationship: Optional[RelationshipType] = None
    is_favorite: Optional[bool] = None

class RecipientInDB(RecipientBase):
    recipient_id: int
    user_id: int

    class Config:
        orm_mode = True

class RecipientResponse(RecipientInDB):
    pass

class RecipientList(BaseModel):
    recipients: list[RecipientResponse]

class FavoriteToggleResponse(BaseModel):
    recipient_id: int
    is_favorite: bool