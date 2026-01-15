from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_get_recipients(self, message, msg_vals):
        """Force include archived partners for sales/invoices"""
        if self._name in ("sale.order", "account.move"):
            # Add context flag before calling parent
            self = self.with_context(mail_notification=True)
        
        recipients = super()._notify_get_recipients(message, msg_vals)
        
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