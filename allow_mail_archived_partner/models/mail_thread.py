import logging
_logger = logging.getLogger(__name__)

from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """Override to add context before calling parent method"""
        _logger.info("=== DEBUG _notify_thread START ===")
        
        if self._name in ("sale.order", "account.move"):
            # Add context flags for partner searches
            self = self.with_context(
                mail_notification=True, 
                active_test=False,
                include_archived_partners=True
            )
        
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _message_get_default_recipients(self):
        """CRITICAL: Include archived partners in default recipients"""
        _logger.info("=== DEBUG _message_get_default_recipients START ===")
        
        if self._name in ("sale.order", "account.move"):
            # Add context BEFORE calling parent
            self = self.with_context(active_test=False)
        
        res = super()._message_get_default_recipients()
        
        # Check if we need to add archived partners
        if self._name in ("sale.order", "account.move"):
            for record in self:
                if record.id not in res and record.partner_id:
                    # Partner not found - likely because it's archived
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(record.partner_id.id)
                    
                    if partner.exists() and partner.email:
                        res[record.id] = {
                            partner.id: {
                                'partner_id': partner.id,
                                'email': partner.email,
                                'name': partner.name,
                            }
                        }
                        _logger.info(f"Added archived partner {partner.id} to recipients")
        
        _logger.info("=== DEBUG _message_get_default_recipients END ===")
        return res

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """Ensure archived partners are included as recipients"""
        _logger.info("=== DEBUG _notify_get_recipients START ===")
        
        # Get recipients normally
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # If we have recipients, make sure they have all required fields
        for recipient in recipients:
            if 'notif' not in recipient:
                recipient['notif'] = recipient.get('notifications', 'email')
        
        _logger.info("=== DEBUG _notify_get_recipients END ===")
        return recipients