import logging
_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Allow archived partners ONLY for explicit manual sends
        """
        # 1) Check if this is a MANUAL send (from invoice wizard or compose message)
        is_manual_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners") or
            self.env.context.get("force_email") or          # From invoice wizard
            self.env.context.get("mark_invoice_as_sent")    # From invoice wizard
        )
        
        _logger.debug(f"MailThread._notify_get_recipients for {self._name}")
        _logger.debug(f"Is manual send: {is_manual_send}")
        _logger.debug(f"Context: mail_notify_force={self.env.context.get('mail_notify_force')}, "
                     f"include_archived={self.env.context.get('include_archived_partners')}, "
                     f"force_email={self.env.context.get('force_email')}")
        
        # 2) For MANUAL sends, allow archived partners with full context
        if is_manual_send:
            _logger.debug(f"Manual send detected for {self._name}, allowing archived partners")
            return super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._notify_get_recipients(message, msg_vals, **kwargs)
        
        # 3) BLOCK system notifications completely
        is_system_notification = (
            getattr(message, "message_type", None) == "notification" or
            getattr(message, "author_id", False) and 
            message.author_id == self.env.ref("base.partner_root", raise_if_not_found=False) or
            (msg_vals and msg_vals.get("message_type") == "notification")
        )
        
        if is_system_notification:
            _logger.debug("Blocking system notification email")
            recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
            # Force inbox only, no email
            for recipient in recipients:
                recipient["notif"] = "inbox"
            return recipients
        
        # 4) Default behavior for non-manual, non-system sends
        return super()._notify_get_recipients(message, msg_vals, **kwargs)