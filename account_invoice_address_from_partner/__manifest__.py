{
    "name": "Invoice address same as customer",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "summary": "Keep invoice address exactly the same as the selected customer",
    "description": """
When selecting a customer on an invoice, the invoice address
(partner_invoice_id) is set to exactly the same partner record,
without collapsing to the commercial parent.
""",
    "depends": [
        "account",
    ],
    "data": [],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
