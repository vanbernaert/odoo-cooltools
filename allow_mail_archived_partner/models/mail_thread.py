import logging
_logger = logging.getLogger(__name__)

from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """Override to add context before calling parent method"""
        if self._name in ("sale.order", "account.move"):
            self = self.with_context(
                mail_notification=True, 
                active_test=False,
                include_archived_partners=True
            )
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """Force create recipients for archived partners"""
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # If no recipients but we have a partner on the record
        if not recipients and self._name in ("sale.order", "account.move"):
            for record in self:
                if record.partner_id:
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(record.partner_id.id)
                    
                    if partner.exists() and partner.email:
                        recipients = [{
                            'id': partner.id,
                            'partner_id': partner.id,
                            'email': partner.email,
                            'name': partner.name,
                            'partner': partner,
                            'active_partner': partner,
                            'shared_partner': partner,
                            'is_partner': True,
                            'notifications': 'email',
                            'notif': 'email',  # CRITICAL: This was missing!
                            'type': 'customer',
                            'lang': partner.lang or 'en_US',
                            'groups': [],
                            'usr_id': None,
                        }]
        
        return recipients