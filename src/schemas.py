
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class InvoiceData(BaseModel):

    supplier_name: str | None = None
    customer_name: str | None = None
    invoice_number: str | None = None

    invoice_date: date | None = None
    due_date: date | None = None

    subtotal: Decimal | None = None
    tax: Decimal | None = None
    total: Decimal | None = None

    currency: str | None = None
