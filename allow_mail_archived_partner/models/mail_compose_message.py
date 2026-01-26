from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        """
        For sales orders and other models using generic composer.
        """
        res = super().default_get(fields)
        
        model = self.env.context.get("active_model")
        res_id = self.env.context.get("active_id")
        
        # For sales orders
        if model == "sale.order" and res_id:
            order = self.env["sale.order"].with_context(
                active_test=False
            ).browse(res_id)
            
            if order.exists() and order.partner_id and order.partner_id.email:
                res["partner_ids"] = [(6, 0, [order.partner_id.id])]
        
        return res

    def _prepare_mail_values(self, res_ids):
        """
        For explicit user sends from sales orders.
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

    def _prepare_recipient_values(self, partner):
        """
        For sales orders and generic composers.
        """
        model = self.env.context.get("active_model") or self.model

        if (
            model in ["sale.order", "account.move"]
            and self.env.context.get("include_archived_partners")
            and partner
        ):
            # Use parent method with proper context
            return super(
                MailComposeMessage,
                self.with_context(active_test=False)
            )._prepare_recipient_values(partner)
        
        return super()._prepare_recipient_values(partner)