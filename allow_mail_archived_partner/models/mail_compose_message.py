import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        """
        Pre-fill email wizard with archived partners for sales orders.
        For invoices, this is handled by account.invoice.send.
        """
        _logger.debug("=== MAIL.COMPOSE.MESSAGE DEFAULT_GET ===")
        
        res = super().default_get(fields)
        
        model = self.env.context.get("active_model")
        res_id = self.env.context.get("active_id")
        
        # Only handle sales orders here - invoices use account.invoice.send
        if model == "sale.order" and res_id:
            _logger.debug(f"Processing sales order {res_id}")
            
            # Find order with archived partners allowed
            order = self.env["sale.order"].with_context(
                active_test=False
            ).browse(res_id)
            
            if order.exists() and order.partner_id:
                res["partner_ids"] = [(6, 0, [order.partner_id.id])]
                _logger.debug(f"Pre-filled archived partner {order.partner_id.id} for sales order")
        
        return res

    def _prepare_mail_values(self, res_ids):
        """
        Set context flags for manual email sends.
        This ensures archived partners are allowed during email sending.
        """
        _logger.debug("=== _prepare_mail_values ===")
        
        model = self.env.context.get("active_model") or self.model
        
        # Only for sales orders and account moves (invoices)
        # Note: account.invoice.send should handle invoices, but keep this as fallback
        if model in ["sale.order", "account.move"]:
            _logger.debug(f"Setting context for {model} to allow archived partners")
            return super(
                MailComposeMessage,
                self.with_context(
                    active_test=False,           # Allow finding archived partners
                    include_archived_partners=True,  # Tell other methods
                    mail_notify_force=True,      # Mark as explicit user action
                )
            )._prepare_mail_values(res_ids)
        
        return super()._prepare_mail_values(res_ids)

    def _prepare_recipient_values(self, partner):
        """
        Handle archived partners for manual email sends.
        This is called for each recipient when building the email.
        """
        # Check if we're in a manual send context
        is_manual_send = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force") or
            self.env.context.get("force_email") or          # From invoice wizard
            self.env.context.get("mark_invoice_as_sent")    # From invoice wizard
        )
        
        # If it's a manual send and partner is archived, include them
        if is_manual_send and partner and not partner.active:
            _logger.debug(f"Including archived partner {partner.name} in email")
            return {
                "partner_id": partner.id,
                "email": partner.email,
                "name": partner.name,
                "lang": partner.lang or self.env.context.get("lang") or "en_US",
            }
        
        # Default behavior for active partners or non-manual sends
        return super()._prepare_recipient_values(partner)