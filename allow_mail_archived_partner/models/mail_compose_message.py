from odoo import models

class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _prepare_mail_values(self, res_ids):
        return super(
            MailComposeMessage,
            self.with_context(active_test=False)
        )._prepare_mail_values(res_ids)
