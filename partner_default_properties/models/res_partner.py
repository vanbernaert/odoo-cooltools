# -*- coding: utf-8 -*-
from odoo import models
from .res_config_settings import PARAM_FISCAL_POSITION, PARAM_PAYMENT_TERM


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ICP = self.env['ir.config_parameter'].sudo()

        fp_id = ICP.get_param(PARAM_FISCAL_POSITION)
        if fp_id:
            res['property_account_position_id'] = int(fp_id)

        pt_id = ICP.get_param(PARAM_PAYMENT_TERM)
        if pt_id:
            res['property_payment_term_id'] = int(pt_id)

        return res
