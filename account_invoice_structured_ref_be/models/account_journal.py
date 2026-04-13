# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    invoice_reference_type = fields.Selection(
        selection_add=[('be_structured', 'Based on Invoice Number (BE Structured)')],
        ondelete={'be_structured': 'set default'},
    )
