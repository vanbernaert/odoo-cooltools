import logging

_logger = logging.getLogger(__name__)

from odoo import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    def _message_get_suggested_recipients(self):
        """Override to include archived partners when sending invoices."""
        _logger.info("🔥 AccountMove._message_get_suggested_recipients")

        # Check if we're in a manual email sending context
        is_manual_send = (
            self.env.context.get("mail_notify_force")
            or self.env.context.get("include_archived_partners")
            or self.env.context.get("force_email")
            or self.env.context.get("mark_invoice_as_sent")
        )

        if is_manual_send:
            _logger.info(f"🔥 Manual send context detected, allowing archived partners")
            return super(
                AccountMove, self.with_context(active_test=False)
            )._message_get_suggested_recipients()

        return super()._message_get_suggested_recipients()

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=None):
        """Override to include archived partners in notification groups."""
        _logger.info("🔥 AccountMove._notify_get_recipients_groups")

        # Check if we're in a manual email sending context
        is_manual_send = (
            self.env.context.get("mail_notify_force")
            or self.env.context.get("include_archived_partners")
            or self.env.context.get("force_email")
            or self.env.context.get("mark_invoice_as_sent")
        )

        if is_manual_send:
            _logger.info(f"🔥 Manual send - using active_test=False")
            return super(
                AccountMove, self.with_context(active_test=False)
            )._notify_get_recipients_groups(message, model_description, msg_vals)

        return super()._notify_get_recipients_groups(
            message, model_description, msg_vals
        )
