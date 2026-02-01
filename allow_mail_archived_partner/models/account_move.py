from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def _send_invoice(self):
        if self.env.context.get("force_email") or self.env.context.get("mark_invoice_as_sent"):
            return super(
                AccountMove,
                self.with_context(active_test=False)
            )._send_invoice()

        return super()._send_invoice()
