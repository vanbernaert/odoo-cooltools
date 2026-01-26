import logging
_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        FIXED: Allow archived partners ONLY for explicit manual sends
        """
        # 1) BLOCK system notifications completely
        is_system_notification = (
            getattr(message, "message_type", None) == "notification" or
            getattr(message, "author_id", False) and 
            message.author_id == self.env.ref("base.partner_root", raise_if_not_found=False)
        )
        
        if is_system_notification:
            _logger.debug("Blocking system notification email")
            recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)
            # Force inbox only, no email
            for recipient in recipients:
                recipient["notif"] = "inbox"
            return recipients

        # 2) Check if this is an EXPLICIT manual send
        is_explicit_send = (
            self.env.context.get("mail_notify_force") or
            self.env.context.get("include_archived_partners")
        )
        
        # 3) For explicit sends, allow archived partners
        if is_explicit_send:
            _logger.debug(f"Explicit send detected for {self._name}, allowing archived partners")
            return super(
                MailThread,
                self.with_context(active_test=False)
            )._notify_get_recipients(message, msg_vals, **kwargs)
        
        # 4) Default behavior for non-explicit sends
        return super()._notify_get_recipients(message, msg_vals, **kwargs)