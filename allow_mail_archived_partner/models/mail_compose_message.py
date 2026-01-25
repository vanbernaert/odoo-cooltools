from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _get_default_recipients(self):
        """
        This is the ONLY place that fills the 'To' field in Odoo 16.
        We explicitly allow archived partners here for user-initiated sends.
        """
        recipients = super()._get_default_recipients()

        model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids") or []

        if model == "account.move" and active_ids:
            moves = self.env["account.move"].with_context(
                active_test=False
            ).browse(active_ids)

            partners = moves.mapped("partner_id").filtered(
                lambda p: p.email
            )

            if partners:
                recipients["partner_ids"] = [(6, 0, partners.ids)]
                recipients["email_to"] = ", ".join(partners.mapped("email"))

        return recipients

    def _prepare_mail_values(self, res_ids):
        """
        Explicit user send → allow archived partners internally.
        """
        model = self.env.context.get("active_model") or self.model

        if model in ["sale.order", "account.move"]:
            return super(
                MailComposeMessage,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._prepare_mail_values(res_ids)

        return super()._prepare_mail_values(res_ids)
