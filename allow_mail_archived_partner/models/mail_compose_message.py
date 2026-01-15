from odoo import models, api

class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _prepare_mail_values(self, res_ids):
        # Get the model from context or self
        model = self.env.context.get('active_model') or self.model
        
        if model in ['sale.order', 'account.move']:
            return super(
                MailComposeMessage,
                self.with_context(active_test=False)
            )._prepare_mail_values(res_ids)
        
        return super()._prepare_mail_values(res_ids)

    def _prepare_recipient_values(self, partner):
        """Prepare recipient values, including archived partners"""
        model = self.env.context.get('active_model') or self.model
        
        if model in ['sale.order', 'account.move']:
            # Ensure we can get data from archived partners
            if partner and not partner.active:
                return {
                    'partner_id': partner.id,
                    'email': partner.email,
                    'name': partner.name,
                }
        
        return super()._prepare_recipient_values(partner)