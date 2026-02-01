import logging

_logger = logging.getLogger(__name__)

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_invoice_sent(self):
        _logger.error("🔥🔥🔥 HIT action_invoice_sent 🔥🔥🔥")
        return super().action_invoice_sent()

    def action_invoice_send(self):
        _logger.error("🔥🔥🔥 HIT action_invoice_send 🔥🔥🔥")
        return super().action_invoice_send()
