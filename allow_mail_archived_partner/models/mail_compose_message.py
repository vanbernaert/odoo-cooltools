from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _prepare_recipient_values(self, partner):
        """
        Handle archived partners when context allows.
        """
        # Check if we should include archived partners
        # Look for context flags from account.invoice.send OR direct context
        include_archived = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force") or
            (self.env.context.get("active_model") in ["account.move", "sale.order"] and 
             not getattr(partner, 'active', True))
        )
        
        if include_archived and partner and not partner.active:
            # Return complete data for archived partner
            return {
                "partner_id": partner.id,
                "email": partner.email,
                "name": partner.name,
                "lang": partner.lang or self.env.context.get("lang") or "en_US",
            }
        
        return super()._prepare_recipient_values(partner)