from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def _onchange_partner_copy_to_invoice_address(self):
        for order in self:
            if order.partner_id:
                # Copy Klant exactly to Factuuradres
                order.partner_invoice_id = order.partner_id
