import logging

_logger = logging.getLogger(__name__)

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_send_and_print(self):
        _logger.error("🔥🔥🔥 CUSTOM action_send_and_print HIT 🔥🔥🔥")
        _logger.error("🔥 Context at entry: %s", dict(self.env.context))

        return super().action_send_and_print()
