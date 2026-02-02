{
    "name": "Invoice legal address from customer",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "summary": "Use the exact customer as invoice address",
    "description": """
Copies the selected customer (Klant) directly to the invoice address
on sale orders and invoices, without collapsing to the commercial partner.
""",
    "depends": [
        "account",
        "sale",
    ],
    "installable": True,
    "license": "LGPL-3",
}
