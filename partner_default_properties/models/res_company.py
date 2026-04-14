# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    customer_fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Default Customer Fiscal Position',
    )
    customer_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Default Customer Payment Terms',
    )
