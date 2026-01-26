from odoo import models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def generate_email(self, res_ids, fields=None):
        """
        Only allow archived partners when *explicitly* sending through a flow
        that sets context['mail_notify_force'] = True.

        This prevents system notifications from inheriting your relaxed rules.
        """
        if self.model in ["sale.order", "account.move"] and self.env.context.get("mail_notify_force"):
            return super(
                MailTemplate,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True
                )
            ).generate_email(res_ids, fields)

        return super().generate_email(res_ids, fields)