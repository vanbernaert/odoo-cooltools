import logging

_logger = logging.getLogger(__name__)

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    _logger.info("=== MAILTHREAD CLASS LOADED (allow_mail_archived_partner) ===")

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        """
        Keep default behavior.
        """
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    def _notify_get_recipients(self, message, msg_vals, **kwargs):
        """
        Force correct email recipients for manual sends (invoices),
        including archived partners, and avoid incomplete recipient dicts.
        """
        _logger.error("🔥🔥🔥 MailThread._notify_get_recipients CALLED 🔥🔥🔥")

        # --- Ignore system / automatic notifications ---
        is_system_message = (
            getattr(message, "message_type", None) == "notification"
            or (
                getattr(message, "author_id", False)
                and message.author_id
                == self.env.ref("base.partner_root", raise_if_not_found=False)
            )
            or (msg_vals and msg_vals.get("message_type") == "notification")
        )

        if is_system_message:
            _logger.debug("SYSTEM MESSAGE – using parent behavior")
            return super()._notify_get_recipients(message, msg_vals, **kwargs)

        # --- Detect manual send ---
        is_manual_send = (
            self.env.context.get("mail_notify_force")
            or self.env.context.get("include_archived_partners")
            or self.env.context.get("force_email")
            or self.env.context.get("mark_invoice_as_sent")
        )

        _logger.error(f"🔥 Is manual send? {is_manual_send}")
        _logger.error(
            f"🔥 Message partner_ids: {getattr(message, 'partner_ids', None)}"
        )

        if not (
            is_manual_send and hasattr(message, "partner_ids") and message.partner_ids
        ):
            _logger.debug("Not a manual send or no partners – using parent behavior")
            return super()._notify_get_recipients(message, msg_vals, **kwargs)

        # --- Manual send with partners ---
        partner_ids = message.partner_ids.ids
        _logger.error(f"🔥 Manual send partners: {partner_ids}")

        # Get parent recipients (may be incomplete)
        recipients = (
            super(
                MailThread,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                ),
            )._notify_get_recipients(message, msg_vals, **kwargs)
            or []
        )

        _logger.error(f"🔥 Parent returned {len(recipients)} recipients")

        def _is_bad_recipient(r):
            return not r or not r.get("email") or not r.get("partner_id")

        bad_recipients = [r for r in recipients if _is_bad_recipient(r)]

        if bad_recipients:
            _logger.error(
                f"🔥 Found {len(bad_recipients)} incomplete recipient(s), forcing from partner_ids"
            )

        # Build forced recipients from partner_ids
        forced_recipients = []
        for partner_id in partner_ids:
            partner = (
                self.env["res.partner"]
                .with_context(active_test=False)
                .browse(partner_id)
            )

            if partner.exists() and partner.email:
                forced_recipients.append(
                    {
                        "id": partner.id,
                        "partner_id": partner.id,
                        "email": partner.email,
                        "name": partner.name,
                        "notif": "email",
                        "lang": partner.lang or "en_US",
                        "type": "customer",
                        "is_follower": False,
                        "groups": [],
                        "notifications": [],
                    }
                )
                _logger.error(f"🔥 Forced recipient: {partner.id} – {partner.email}")

        # Prefer forced recipients if parent gave nothing useful
        if forced_recipients and (not recipients or bad_recipients):
            recipients = forced_recipients

        for i, recipient in enumerate(recipients):
            _logger.error(
                f"🔥 Recipient {i}: "
                f"partner_id={recipient.get('partner_id')}, "
                f"notif={recipient.get('notif')}, "
                f"email={recipient.get('email')}"
            )

        return recipients
