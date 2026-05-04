from pydantic import BaseModel, Field
from typing import Optional

class Expense(BaseModel):
    amount: Optional[str] = Field(title="expense", description="transaction amount")
    merchant: Optional[str] = Field(title="merchant", description="merchant name, null for credit transaction")
    currency: Optional[str] = Field(title="currency", description="currency of the transaction")
    transaction_type: Optional[str] = Field(title="transaction_type", description="debit or credit")
    date: Optional[str] = Field(title="date", description="transaction date in yyyy-mm-dd format")
