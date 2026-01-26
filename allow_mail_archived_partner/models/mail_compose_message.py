import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        """
        Pre-fill the email wizard with archived partner's email.
        This makes the archived partner appear in the "To" field.
        """
        res = super().default_get(fields)
        
        model = self.env.context.get("active_model")
        res_id = self.env.context.get("active_id")
        
        # For invoices
        if model == "account.move" and res_id:
            invoice = self.env["account.move"].with_context(
                active_test=False  # CRITICAL: Find archived partner
            ).browse(res_id)
            
            if invoice.exists() and invoice.partner_id:
                res["partner_ids"] = [(6, 0, [invoice.partner_id.id])]
                _logger.debug(f"Pre-filled archived partner {invoice.partner_id.name} for invoice")
        
        # For sales orders
        elif model == "sale.order" and res_id:
            order = self.env["sale.order"].with_context(
                active_test=False  # CRITICAL: Find archived partner
            ).browse(res_id)
            
            if order.exists() and order.partner_id:
                res["partner_ids"] = [(6, 0, [order.partner_id.id])]
                _logger.debug(f"Pre-filled archived partner {order.partner_id.name} for sales order")
        
        return res

    def _prepare_mail_values(self, res_ids):
        """
        Set context to allow archived partners during email sending.
        This ensures the email can actually be sent to archived partners.
        """
        model = self.env.context.get("active_model") or self.model
        
        if model in ["sale.order", "account.move"]:
            _logger.debug(f"Setting context for {model} to allow archived partners")
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
        Handle archived partners when context allows.
        This ensures archived partner data is properly formatted for email.
        """
        include_archived = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force")
        )
        
        if include_archived and partner and not partner.active:
            _logger.debug(f"Including archived partner {partner.name} in email")
            return {
                "partner_id": partner.id,
                "email": partner.email,
                "name": partner.name,
                "lang": partner.lang or self.env.context.get("lang") or "en_US",
            }
        
        return super()._prepare_recipient_values(partner)