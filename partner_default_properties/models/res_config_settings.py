# -*- coding: utf-8 -*-
from odoo import fields, models

PARAM_FISCAL_POSITION = 'partner_default_properties.fiscal_position_id'
PARAM_PAYMENT_TERM = 'partner_default_properties.payment_term_id'


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string='Default Fiscal Position',
        compute='_compute_customer_fiscal_position_id',
        inverse='_set_customer_fiscal_position_id',
    )
    customer_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Default Payment Terms',
        compute='_compute_customer_payment_term_id',
        inverse='_set_customer_payment_term_id',
    )

    def _compute_customer_fiscal_position_id(self):
        ICP = self.env['ir.config_parameter'].sudo()
        param = ICP.get_param(PARAM_FISCAL_POSITION)
        for rec in self:
            rec.customer_fiscal_position_id = int(param) if param else False

    def _set_customer_fiscal_position_id(self):
        ICP = self.env['ir.config_parameter'].sudo()
        for rec in self:
            ICP.set_param(PARAM_FISCAL_POSITION, rec.customer_fiscal_position_id.id or False)

    def _compute_customer_payment_term_id(self):
        ICP = self.env['ir.config_parameter'].sudo()
        param = ICP.get_param(PARAM_PAYMENT_TERM)
        for rec in self:
            rec.customer_payment_term_id = int(param) if param else False

    def _set_customer_payment_term_id(self):
        ICP = self.env['ir.config_parameter'].sudo()
        for rec in self:
            ICP.set_param(PARAM_PAYMENT_TERM, rec.customer_payment_term_id.id or False)
