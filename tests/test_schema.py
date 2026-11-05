from src.schemas import InvoiceData

invoice = InvoiceData(
    supplier_name="ABC Company",
    customer_name="XYZ Traders",
    invoice_number="INV-001",
    invoice_date="2026-08-14",
    due_date=None,
    subtotal="16700.00",
    tax="2304.00",
    total="19004.00",
    currency="INR"
)

print(invoice.model_dump_json(indent=4))