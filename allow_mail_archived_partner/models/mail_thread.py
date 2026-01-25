import logging
_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """
        Do NOT force notifications, do NOT set mail_notification=True,
        do NOT globally disable active_test here.

        The parent method decides whether a message should notify.
        """
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        CRITICAL RULES:
        - Never turn system notifications into outgoing emails.
        - Never fabricate recipients when Odoo returns none.
        - Never force notif='email'.

        If archived partners should be allowed, that must be opt-in
        via context['include_archived_partners'] and only for explicit user sends,
        not tracking/system messages.
        """
        # 1) Never email system notifications (tracking, auto messages, etc.)
        # These are the ones that caused "Re: Draft Bill ..." and odoobot@example.com.
        if getattr(message, "message_type", None) == "notification":
            return super()._notify_get_recipients(message, msg_vals, **kwargs)

        # 2) Never auto-notify supplier bills. Vendor bills created from email/EDI
        # must not trigger replies to vendors via chatter notifications.
        # (If you DO want it for customer invoices, leave those alone.)
        if self._name == "account.move":
            # self can be multi; if any are supplier bills, just don't customize at all
            # (safer than partial overriding recipient lists)
            if any(m.move_type == "in_invoice" for m in self):
                return super()._notify_get_recipients(message, msg_vals, **kwargs)

        # 3) Default behavior first
        recipients = super()._notify_get_recipients(message, msg_vals, **kwargs)

        # 4) Do NOT fabricate recipients if empty.
        # If you need archived partner support, handle it in explicit sending flows
        # (compose + template), not here.
        return recipients
