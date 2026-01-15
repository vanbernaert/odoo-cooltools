from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """Override to fix kwargs issue and add context"""
        # Store kwargs to pass them properly
        if self._name in ("sale.order", "account.move"):
            # Add context flags
            self = self.with_context(mail_notification=True, active_test=False)
        
        # Call parent - it will handle the kwargs properly
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """Accept kwargs to match parent signature"""
        # Get recipients normally
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # Only process for sales orders and invoices
        if self._name in ("sale.order", "account.move"):
            # Re-fetch any partner recipients without active filter
            for recipient in recipients:
                if recipient.get('partner_id'):
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(recipient['partner_id'])
                    
                    if partner.exists():
                        recipient.update({
                            'partner': partner,
                            'active_partner': partner,
                        })
        
        return recipients