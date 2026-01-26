import logging
_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    _logger.info("=== MAILTHREAD CLASS LOADED (allow_mail_archived_partner) ===")

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """
        Log notification thread calls.
        """
        _logger.error("🔥🔥🔥 MailThread._notify_thread CALLED 🔥🔥🔥")
        _logger.error(f"🔥 Model: {self._name}")
        _logger.error(f"🔥 Message type: {getattr(message, 'message_type', 'Unknown')}")
        _logger.error(f"🔥 Message subject: {getattr(message, 'subject', 'No subject')}")
        _logger.error(f"🔥 Context: {dict(self.env.context)}")
        
        # Check message attributes
        _logger.error(f"🔥 Message author_id: {getattr(message, 'author_id', None)}")
        _logger.error(f"🔥 Message partner_ids: {getattr(message, 'partner_ids', None)}")
        _logger.error(f"🔥 Message record: {message.model if hasattr(message, 'model') else 'N/A'} {message.res_id if hasattr(message, 'res_id') else 'N/A'}")
        
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Force inclusion of archived partners for manual sends.
        """
        _logger.error("🔥🔥🔥🔥🔥 MailThread._notify_get_recipients CALLED 🔥🔥🔥🔥🔥")
        
        # Check if this is a manual send
        is_manual_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners") or
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent")
        )
        
        _logger.error(f"🔥 Is manual send? {is_manual_send}")
        _logger.error(f"🔥 Message partner_ids: {getattr(message, 'partner_ids', None)}")
        
        # For manual sends, we need to handle archived partners
        if is_manual_send and hasattr(message, 'partner_ids') and message.partner_ids:
            _logger.error("🔥🔥🔥 MANUAL SEND WITH PARTNERS - Handling archived partners 🔥🔥🔥")
            
            # Get the partner IDs from the message
            partner_ids = message.partner_ids.ids
            _logger.error(f"🔥 Message has partners: {partner_ids}")
            
            # Force the lookup of THESE partners (the recipients), not the author
            # We need to ensure these partners are found even if archived
            
            # Call parent with context that allows archived partners
            recipients = super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                    # Add the partner IDs we want to look up
                    force_notification_partner_ids=partner_ids,
                )
            )._notify_get_recipients(message, msg_vals, **kwargs)
            
            _logger.error(f"🔥 Number of recipients found: {len(recipients)}")
            
            # If no recipients found, create them manually
            if len(recipients) == 0 and partner_ids:
                _logger.error("🔥 No recipients found, creating manually")
                recipients = []
                for partner_id in partner_ids:
                    partner = self.env['res.partner'].with_context(
                        active_test=False
                    ).browse(partner_id)
                    
                    if partner.exists() and partner.email:
                        recipients.append({
                            'id': partner.id,
                            'partner_id': partner.id,
                            'email': partner.email,
                            'name': partner.name,
                            'notif': 'email',  # Force email notification
                            'lang': partner.lang or 'en_US',
                            'type': 'customer',
                            'is_follower': False,
                            'groups': [],
                            'notifications': [],
                        })
                        _logger.error(f"🔥 Created recipient for archived partner: {partner.id} - {partner.email}")
            
            for i, recipient in enumerate(recipients):
                _logger.error(f"🔥 Recipient {i}: partner_id={recipient.get('partner_id')}, "
                        f"notif={recipient.get('notif')}, email={recipient.get('email')}")
            
            return recipients
    

    def _message_post(self, **kwargs):
        """
        Log message post calls to trace email flow.
        """
        _logger.error("🔥🔥🔥 MailThread._message_post CALLED 🔥🔥🔥")
        _logger.error(f"🔥 Model: {self._name}")
        _logger.error(f"🔥 Kwargs keys: {kwargs.keys()}")
        _logger.error(f"🔥 Context: {dict(self.env.context)}")
        
        return super()._message_post(**kwargs)

    def message_post(self, **kwargs):
        """
        Override to ensure partner_ids are passed correctly.
        """
        _logger.error("🔥🔥🔥 MailThread.message_post CALLED 🔥🔥🔥")
        _logger.error(f"🔥 Model: {self._name}")
        _logger.error(f"🔥 Kwargs keys: {kwargs.keys()}")
        _logger.error(f"🔥 Context: {dict(self.env.context)}")
        _logger.error(f"🔥 Partner IDs in kwargs: {kwargs.get('partner_ids', [])}")
        
        # Check if we have partner_ids from context (passed from account.invoice.send)
        context_partner_ids = self.env.context.get('invoice_partner_ids', [])
        if context_partner_ids and not kwargs.get('partner_ids'):
            _logger.error(f"🔥 Using partner_ids from context: {context_partner_ids}")
            # Convert to simple list of IDs, NOT ORM tuple format
            kwargs['partner_ids'] = context_partner_ids
        
        # Also check for other sources of partner_ids
        if not kwargs.get('partner_ids'):
            # Try to get from the record itself
            if self and hasattr(self, 'partner_id') and self.partner_id:
                _logger.error(f"🔥 Getting partner_id from record: {self.partner_id.id}")
                kwargs['partner_ids'] = [self.partner_id.id]
        
        # Convert ORM tuple format to simple list if needed
        if kwargs.get('partner_ids') and isinstance(kwargs['partner_ids'], list):
            # Check if it's in ORM format [(6, 0, [id1, id2])]
            if (len(kwargs['partner_ids']) == 1 and 
                isinstance(kwargs['partner_ids'][0], (list, tuple)) and 
                len(kwargs['partner_ids'][0]) == 3 and
                kwargs['partner_ids'][0][0] == 6):
                
                # Extract IDs from ORM format
                partner_ids = kwargs['partner_ids'][0][2]
                _logger.error(f"🔥 Converting ORM format to simple list: {kwargs['partner_ids']} -> {partner_ids}")
                kwargs['partner_ids'] = partner_ids
        
        _logger.error(f"🔥 Final partner_ids being passed: {kwargs.get('partner_ids', [])}")
        
        return super().message_post(**kwargs)