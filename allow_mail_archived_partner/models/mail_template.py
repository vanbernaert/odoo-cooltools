from odoo import models

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def _generate_recipients(self, results, res_ids):
        # Allow archived partners during email generation
        return super(
            MailTemplate,
            self.with_context(active_test=False)
        )._generate_recipients(results, res_ids)
