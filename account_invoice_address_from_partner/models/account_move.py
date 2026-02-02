from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange("partner_id")
    def _onchange_partner_copy_to_invoice_address(self):
        for move in self:
            if move.partner_id:
                # Copy Klant exactly to Factuuradres
                move.partner_invoice_id = move.partner_id
