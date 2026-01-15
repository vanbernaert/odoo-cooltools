import logging
_logger = logging.getLogger(__name__)

from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """Override to add context before calling parent method"""
        _logger.info("=== DEBUG _notify_thread START ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Record IDs: {self.ids}")
        _logger.info(f"Full context: {dict(self.env.context)}")
        
        if self._name in ("sale.order", "account.move"):
            # Add context flags for partner searches
            _logger.info("Adding context flags for sales/invoice")
            self = self.with_context(
                mail_notification=True, 
                active_test=False,
                include_archived_partners=True
            )
        
        result = super()._notify_thread(message, msg_vals=msg_vals, **kwargs)
        _logger.info("=== DEBUG _notify_thread END ===")
        return result

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """Ensure archived partners are included as recipients"""
        # DEBUG LOGGING START
        _logger.info("=" * 50)
        _logger.info("=== DEBUG _notify_get_recipients START ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Record IDs: {self.ids}")
        _logger.info(f"Context keys: {list(self.env.context.keys())}")
        _logger.info(f"Has active_test=False: {self.env.context.get('active_test') == False}")
        _logger.info(f"Has mail_notification: {self.env.context.get('mail_notification')}")
        # DEBUG LOGGING END
        
        # Get recipients normally
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        # DEBUG: Log what we got from parent
        _logger.info(f"=== Parent returned {len(recipients)} recipients ===")
        for i, recipient in enumerate(recipients):
            _logger.info(f"Recipient {i}: partner_id={recipient.get('partner_id')}, "
                        f"email={recipient.get('email')}, "
                        f"notifications={recipient.get('notifications')}, "
                        f"type={recipient.get('type')}")
        
        # Only process for sales orders and invoices
        if self._name in ("sale.order", "account.move"):
            _logger.info("=== Processing sales/invoice recipients ===")
            
            for i, recipient in enumerate(recipients):
                partner_id = recipient.get('partner_id')
                if partner_id:
                    # Re-fetch partner without active filter
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(partner_id)
                    
                    _logger.info(f"Recipient {i} - Partner ID {partner_id}: "
                                f"exists={partner.exists()}, "
                                f"active={partner.active if partner.exists() else 'N/A'}, "
                                f"email={partner.email if partner.exists() else 'N/A'}, "
                                f"name={partner.name if partner.exists() else 'N/A'}")
                    
                    if partner.exists():
                        # Update recipient data
                        recipient.update({
                            'partner': partner,
                            'active_partner': partner,
                            'shared_partner': partner,
                            'is_partner': True,
                        })
                        
                        # Ensure email is set
                        if not recipient.get('email') and partner.email:
                            recipient['email'] = partner.email
                            _logger.info(f"  -> Set email to: {partner.email}")
                            
                        # Ensure notifications are enabled
                        if recipient.get('notifications') != 'email':
                            recipient['notifications'] = 'email'
                            _logger.info(f"  -> Set notifications to 'email'")
                else:
                    _logger.info(f"Recipient {i}: No partner_id (email: {recipient.get('email')})")
        
        # DEBUG: Final result
        _logger.info(f"=== Final: Returning {len(recipients)} recipients ===")
        for i, recipient in enumerate(recipients):
            _logger.info(f"Final Recipient {i}: partner_id={recipient.get('partner_id')}, "
                        f"email={recipient.get('email')}, "
                        f"notifications={recipient.get('notifications')}")
        
        _logger.info("=== DEBUG _notify_get_recipients END ===")
        _logger.info("=" * 50)
        return recipients

    def _message_get_default_recipients(self):
        """Include archived partners in default recipients"""
        _logger.info("=== DEBUG _message_get_default_recipients ===")
        _logger.info(f"Model: {self._name}")
        
        res = super()._message_get_default_recipients()
        
        if self._name in ("sale.order", "account.move"):
            _logger.info("Processing sales/invoice default recipients")
            
            for record in self:
                if record.id in res:
                    recipients = res[record.id]
                    _logger.info(f"Record {record.id} has {len(recipients)} default recipients")
                    
                    for partner_id, recipient_data in recipients.items():
                        _logger.info(f"  Partner {partner_id}: {recipient_data}")
        
        return res