import logging

_logger = logging.getLogger(__name__)

from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        _logger.debug("=== MAIL.COMPOSE.MESSAGE DEFAULT_GET ===")

        res = super().default_get(fields)

        ctx = self.env.context
        model = ctx.get("active_model")
        res_id = ctx.get("active_id")

        # -------------------------------------------------
        # 1️⃣ SALE ORDERS (your existing logic, unchanged)
        # -------------------------------------------------
        if model == "sale.order" and res_id:
            _logger.debug(f"Processing sales order {res_id}")

            order = (
                self.env["sale.order"].with_context(active_test=False).browse(res_id)
            )

            if order.exists() and order.partner_id:
                res["partner_ids"] = [(6, 0, [order.partner_id.id])]
                _logger.debug(
                    f"Pre-filled archived partner {order.partner_id.id} for sales order"
                )

        # -------------------------------------------------
        # 2️⃣ INVOICES (THIS WAS MISSING)
        # -------------------------------------------------
        default_partner_ids = ctx.get("default_partner_ids")
        if model == "account.move" and default_partner_ids:
            partner_ids = []
            for cmd in default_partner_ids:
                if isinstance(cmd, (list, tuple)) and cmd[0] == 6:
                    partner_ids = cmd[2]

            if partner_ids:
                partners = (
                    self.env["res.partner"]
                    .with_context(active_test=False)
                    .browse(partner_ids)
                )

                if partners:
                    res["partner_ids"] = [(6, 0, partners.ids)]
                    _logger.error(
                        "🔥 Restored archived invoice partners in mail.compose.message.default_get: %s",
                        partners.ids,
                    )

        return res

    def _prepare_mail_values(self, res_ids):
        _logger.debug("=== _prepare_mail_values ===")

        model = self.env.context.get("active_model") or self.model

        if model in ["sale.order", "account.move"]:
            return super(
                MailComposeMessage,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                ),
            )._prepare_mail_values(res_ids)

        return super()._prepare_mail_values(res_ids)

    def _prepare_recipient_values(self, partner):
        is_manual_send = (
            self.env.context.get("include_archived_partners")
            or self.env.context.get("mail_notify_force")
            or self.env.context.get("force_email")
            or self.env.context.get("mark_invoice_as_sent")
        )

        if is_manual_send and partner and not partner.active:
            return {
                "partner_id": partner.id,
                "email": partner.email,
                "name": partner.name,
                "lang": partner.lang or self.env.context.get("lang") or "en_US",
            }

        return super()._prepare_recipient_values(partner)

    def _action_send_mail(self, auto_commit=False):
        _logger.info("🔥 MAIL.COMPOSE.MESSAGE _action_send_mail")
        return super()._action_send_mail(auto_commit=auto_commit)
