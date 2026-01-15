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

    def _message_get_default_recipients(self):
        """CRITICAL: Include archived partners in default recipients"""
        _logger.info("=== DEBUG _message_get_default_recipients START ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Context before: {dict(self.env.context)}")
        
        if self._name in ("sale.order", "account.move"):
            # Add context BEFORE calling parent
            self = self.with_context(
                active_test=False,
                include_archived_partners=True
            )
            _logger.info(f"Context after: {dict(self.env.context)}")
        
        res = super()._message_get_default_recipients()
        
        _logger.info(f"Default recipients result for records {self.ids}:")
        for record in self:
            if record.id in res:
                recipients = res[record.id]
                _logger.info(f"  Record {record.id} has {len(recipients)} recipients")
                for partner_id, recipient_data in recipients.items():
                    _logger.info(f"    Partner {partner_id}: {recipient_data}")
            else:
                _logger.info(f"  Record {record.id} has NO recipients in result")
                
                # Manually add the partner if missing
                if record.partner_id:
                    _logger.info(f"    But record has partner_id: {record.partner_id.id}")
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(record.partner_id.id)
                    
                    if partner.exists():
                        res[record.id] = {
                            partner.id: {
                                'partner_id': partner.id,
                                'email': partner.email,
                                'name': partner.name,
                            }
                        }
                        _logger.info(f"    Added partner manually: {partner.id} - {partner.email}")
        
        _logger.info("=== DEBUG _message_get_default_recipients END ===")
        return res

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """Ensure archived partners are included as recipients"""
        _logger.info("=== DEBUG _notify_get_recipients START ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Context: {dict(self.env.context)}")
        
        # Get recipients normally
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        
        _logger.info(f"Parent returned {len(recipients)} recipients")
        
        if self._name in ("sale.order", "account.move") and not recipients:
            _logger.info("NO RECIPIENTS FOUND - trying manual fallback")
            
            # Manual fallback: get partner from the record
            for record in self:
                if record.partner_id:
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(record.partner_id.id)
                    
                    if partner.exists() and partner.email:
                        _logger.info(f"Creating recipient for partner {partner.id}")
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
                            'type': 'customer',
                        }]
        
        _logger.info(f"Final: Returning {len(recipients)} recipients")
        _logger.info("=== DEBUG _notify_get_recipients END ===")
        return recipients