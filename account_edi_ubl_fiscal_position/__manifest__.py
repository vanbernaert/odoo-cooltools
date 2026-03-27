{
    'name': 'UBL Import - Apply Fiscal Position Tax Mapping',
    'version': '16.0.1.0.0',
    'summary': 'Applies supplier fiscal position tax mapping during UBL/EDI invoice import',
    'description': """
        Odoo 16 does not apply fiscal positions to vendor bills during UBL
        import (_import_fill_invoice_line_taxes only searches by percentage,
        ignoring fiscal position entirely).

        This module overrides that method to apply the partner's fiscal
        position tax mapping immediately after tax detection, so the correct
        tax code is set without any manual correction.

        Usage:
        - Set a Fiscal Position on the supplier (Verkopen & Inkopen tab)
        - Add the correct tax mapping in that Fiscal Position
        - Import UBL invoices as usual - taxes will be corrected automatically
    """,
    'author': 'Busenco / Villajoyosa Digital',
    'category': 'Accounting',
    'depends': ['account_edi_ubl_cii'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
