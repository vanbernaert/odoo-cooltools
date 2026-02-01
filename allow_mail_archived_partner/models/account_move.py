import logging

_logger = logging.getLogger(__name__)

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _send_invoice(self):
        _logger.error("🔥🔥🔥 CUSTOM _send_invoice HIT 🔥🔥🔥")
        _logger.error("🔥 Context: %s", dict(self.env.context))

        return super(AccountMove, self.with_context(active_test=False))._send_invoice()
