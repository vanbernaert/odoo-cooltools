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
        Allow archived partners for ANY manual email send.
        """
        _logger.error("🔥🔥🔥🔥🔥 MailThread._notify_get_recipients CALLED 🔥🔥🔥🔥🔥")
        _logger.error(f"🔥 Model: {self._name}")
        _logger.error(f"🔥 Message type: {getattr(message, 'message_type', 'Unknown')}")
        _logger.error(f"🔥 Message subject: {getattr(message, 'subject', 'No subject')}")
        _logger.error(f"🔥 Full context: {dict(self.env.context)}")
        
        # Check MULTIPLE indicators of manual send
        is_manual_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners") or
            self.env.context.get("force_email") or          # From invoice wizard
            self.env.context.get("mark_invoice_as_sent") or # From invoice wizard
            # Additional checks for email sends
            (self._name == "account.move" and 
             self.env.context.get("default_composition_mode") == "comment") or
            (msg_vals and msg_vals.get("message_type") == "email")
        )
        
        _logger.error(f"🔥 Is manual send? {is_manual_send}")
        _logger.error(f"🔥 All context flags: mail_notify_force={self.env.context.get('mail_notify_force')}, "
                     f"include_archived={self.env.context.get('include_archived_partners')}, "
                     f"force_email={self.env.context.get('force_email')}, "
                     f"mark_invoice_as_sent={self.env.context.get('mark_invoice_as_sent')}")
        
        # For MANUAL sends, allow archived partners with full context
        if is_manual_send:
            _logger.error("🔥🔥🔥 ✓ MANUAL SEND DETECTED - Allowing archived partners 🔥🔥🔥")
            _logger.error(f"🔥 Calling super() with context: active_test=False, include_archived_partners=True, mail_notify_force=True")
            
            # Use context that allows archived partners
            recipients = super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._notify_get_recipients(message, msg_vals, **kwargs)
            
            _logger.error(f"🔥 Number of recipients found: {len(recipients)}")
            for i, recipient in enumerate(recipients):
                _logger.error(f"🔥 Recipient {i}: partner_id={recipient.get('partner_id')}, "
                           f"notif={recipient.get('notif')}, email={recipient.get('email')}, "
                           f"groups={recipient.get('groups', [])}")
            
            return recipients
        
        # BLOCK system notifications completely
        is_system_notification = (
            getattr(message, "message_type", None) == "notification" or
            (getattr(message, "author_id", False) and 
             message.author_id == self.env.ref("base.partner_root", raise_if_not_found=False)) or
            (msg_vals and msg_vals.get("message_type") == "notification") or
            getattr(message, "subtype_id", False) and 
            getattr(message.subtype_id, "internal", False)
        )
        
        if is_system_notification:
            _logger.error("🔥🔥🔥 ✗ SYSTEM NOTIFICATION - Blocking emails, forcing inbox only 🔥🔥🔥")
            recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
            _logger.error(f"🔥 System notification recipients before blocking: {len(recipients)}")
            
            # Force inbox only, no email
            for recipient in recipients:
                recipient["notif"] = "inbox"
                _logger.error(f"🔥 Blocked email for recipient: partner_id={recipient.get('partner_id')}")
            
            return recipients
        
        # Default behavior for non-manual, non-system sends
        _logger.error("🔥🔥🔥 ○ DEFAULT BEHAVIOR - No special handling 🔥🔥🔥")
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        _logger.error(f"🔥 Default recipients found: {len(recipients)}")
        for i, recipient in enumerate(recipients):
            _logger.error(f"🔥 Default recipient {i}: partner_id={recipient.get('partner_id')}, "
                       f"notif={recipient.get('notif')}")
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