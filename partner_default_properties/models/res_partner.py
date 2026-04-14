# -*- coding: utf-8 -*-
from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        company = self.env.company

        if company.customer_fiscal_position_id:
            res['property_account_position_id'] = company.customer_fiscal_position_id.id

        if company.customer_payment_term_id:
            res['property_payment_term_id'] = company.customer_payment_term_id.id

        return res
