# account_move_send.py
from odoo import models, api


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.model
    def default_get(self, fields):
        """
        Pre-fill invoice email wizard with archived partner.
        """
        res = super().default_get(fields)
        
        active_ids = self.env.context.get('active_ids', [])
        
        if active_ids:
            # Find invoices WITH archived partners
            invoices = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            partner_ids = []
            for inv in invoices:
                if inv.partner_id:
                    partner_ids.append(inv.partner_id.id)
            
            if partner_ids:
                res['partner_ids'] = [(6, 0, partner_ids)]
        
        return res