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
        _logger.info("=== MailThread._notify_thread ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Message type: {getattr(message, 'message_type', 'Unknown')}")
        _logger.info(f"Message subject: {getattr(message, 'subject', 'No subject')}")
        _logger.info(f"Context: {dict(self.env.context)}")
        
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Allow archived partners ONLY for explicit manual sends.
        """
        _logger.info("=== MailThread._notify_get_recipients ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Message type: {getattr(message, 'message_type', 'Unknown')}")
        _logger.info(f"Message subject: {getattr(message, 'subject', 'No subject')}")
        _logger.info(f"Full context: {dict(self.env.context)}")
        
        # 1) Check if this is a MANUAL send (invoice wizard or compose message)
        is_manual_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners") or
            self.env.context.get("force_email") or          # From invoice wizard
            self.env.context.get("mark_invoice_as_sent")    # From invoice wizard
        )
        
        _logger.info(f"Is manual send? {is_manual_send}")
        _logger.info(f"Context flags - mail_notify_force: {self.env.context.get('mail_notify_force')}")
        _logger.info(f"Context flags - include_archived_partners: {self.env.context.get('include_archived_partners')}")
        _logger.info(f"Context flags - force_email: {self.env.context.get('force_email')}")
        _logger.info(f"Context flags - mark_invoice_as_sent: {self.env.context.get('mark_invoice_as_sent')}")
        
        # 2) For MANUAL sends, allow archived partners with full context
        if is_manual_send:
            _logger.info("✓ MANUAL SEND DETECTED - Allowing archived partners")
            
            # Get recipients with context that allows archived partners
            recipients = super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._notify_get_recipients(message, msg_vals, **kwargs)
            
            _logger.info(f"Number of recipients found: {len(recipients)}")
            for i, recipient in enumerate(recipients):
                _logger.info(f"Recipient {i}: partner_id={recipient.get('partner_id')}, "
                           f"notif={recipient.get('notif')}, email={recipient.get('email')}, "
                           f"groups={recipient.get('groups', [])}")
            
            return recipients
        
        # 3) BLOCK system notifications completely
        is_system_notification = (
            getattr(message, "message_type", None) == "notification" or
            (getattr(message, "author_id", False) and 
             message.author_id == self.env.ref("base.partner_root", raise_if_not_found=False)) or
            (msg_vals and msg_vals.get("message_type") == "notification")
        )
        
        if is_system_notification:
            _logger.info("✗ SYSTEM NOTIFICATION - Blocking emails, forcing inbox only")
            recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
            _logger.info(f"System notification recipients before blocking: {len(recipients)}")
            
            # Force inbox only, no email
            for recipient in recipients:
                recipient["notif"] = "inbox"
                _logger.info(f"Blocked email for recipient: partner_id={recipient.get('partner_id')}")
            
            return recipients
        
        # 4) Default behavior for non-manual, non-system sends
        _logger.info("○ DEFAULT BEHAVIOR - No special handling")
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
        _logger.info(f"Default recipients found: {len(recipients)}")
        return recipients

    def _message_post(self, **kwargs):
        """
        Log message post calls to trace email flow.
        """
        _logger.info("=== MailThread._message_post ===")
        _logger.info(f"Model: {self._name}")
        _logger.info(f"Kwargs: { {k: v for k, v in kwargs.items() if k != 'body'} }")
        _logger.info(f"Context: {dict(self.env.context)}")
        
        return super()._message_post(**kwargs)