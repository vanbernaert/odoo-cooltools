from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_get_recipients(self, message, msg_vals):
        """Main method that controls notification recipients"""
        if self._name in ("sale.order", "account.move"):
            # Get recipients normally, then ensure archived partners are included
            recipients = super()._notify_get_recipients(message, msg_vals)
            
            for recipient in recipients:
                if recipient.get('partner_id'):
                    # Re-fetch partner without active filter
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(recipient['partner_id'])
                    
                    if partner.exists():
                        recipient.update({
                            'partner': partner,
                            'active_partner': partner,
                            'is_partner': True,
                            'shared_partner': partner,
                        })
            
            return recipients
        
        return super()._notify_get_recipients(message, msg_vals)