import logging
_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        _logger.debug("=== MailThread._notify_thread ===")
        _logger.debug(f"Message type: {getattr(message, 'message_type', 'Unknown')}")
        _logger.debug(f"Message subject: {getattr(message, 'subject', 'No subject')}")
        _logger.debug(f"Model: {self._name}")
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Allow archived partners ONLY for explicit manual sends
        """
        _logger.debug("=== MailThread._notify_get_recipients ===")
        _logger.debug(f"Model: {self._name}")
        _logger.debug(f"Message type: {getattr(message, 'message_type', 'Unknown')}")
        _logger.debug(f"Message subject: {getattr(message, 'subject', 'No subject')}")
        
        # 1) Check if this is a MANUAL send
        is_manual_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners") or
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent")
        )
        
        _logger.debug(f"Is manual send: {is_manual_send}")
        _logger.debug(f"Context flags: mail_notify_force={self.env.context.get('mail_notify_force')}, "
                     f"include_archived={self.env.context.get('include_archived_partners')}, "
                     f"force_email={self.env.context.get('force_email')}")
        
        # 2) For MANUAL sends, allow archived partners
        if is_manual_send:
            _logger.debug("Manual send - allowing archived partners with full context")
            recipients = super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._notify_get_recipients(message, msg_vals, **kwargs)
            
            _logger.debug(f"Number of recipients found: {len(recipients)}")
            for i, recipient in enumerate(recipients):
                _logger.debug(f"Recipient {i}: partner_id={recipient.get('partner_id')}, "
                            f"notif={recipient.get('notif')}, email={recipient.get('email')}")
            
            return recipients
        
        # 3) BLOCK system notifications
        is_system_notification = (
            getattr(message, "message_type", None) == "notification" or
            getattr(message, "author_id", False) and 
            message.author_id == self.env.ref("base.partner_root", raise_if_not_found=False) or
            (msg_vals and msg_vals.get("message_type") == "notification")
        )
        
        if is_system_notification:
            _logger.debug("System notification - blocking emails, forcing inbox only")
            recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
            for recipient in recipients:
                recipient["notif"] = "inbox"
            return recipients
        
        # 4) Default behavior
        _logger.debug("Default behavior - no special handling")
        return super()._notify_get_recipients(message, msg_vals, **kwargs)