# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Default Fiscal Position',
        related='company_id.customer_fiscal_position_id',
        readonly=False,
    )
    customer_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Default Payment Terms',
        related='company_id.customer_payment_term_id',
        readonly=False,
    )
