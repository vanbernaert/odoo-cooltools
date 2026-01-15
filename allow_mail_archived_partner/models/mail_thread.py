from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, **kwargs):
        if self._name in ("sale.order", "account.move"):
            return super(MailThread, self.with_context(active_test=False)).message_post(
                **kwargs
            )
        return super().message_post(**kwargs)
