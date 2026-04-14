# -*- coding: utf-8 -*-
from odoo import fields, models

PARAM_FISCAL_POSITION = 'partner_default_properties.fiscal_position_id'
PARAM_PAYMENT_TERM = 'partner_default_properties.payment_term_id'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Default Fiscal Position',
    )
    customer_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Default Payment Terms',
    )

    def get_values(self):
        res = super().get_values()
        ICP = self.env['ir.config_parameter'].sudo()
        fp_id = ICP.get_param(PARAM_FISCAL_POSITION)
        pt_id = ICP.get_param(PARAM_PAYMENT_TERM)
        res.update({
            'customer_fiscal_position_id': int(fp_id) if fp_id else False,
            'customer_payment_term_id': int(pt_id) if pt_id else False,
        })
        return res

    def set_values(self):
        super().set_values()
        ICP = self.env['ir.config_parameter'].sudo()
        ICP.set_param(PARAM_FISCAL_POSITION, self.customer_fiscal_position_id.id or False)
        ICP.set_param(PARAM_PAYMENT_TERM, self.customer_payment_term_id.id or False)
