import logging

_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    # Allow archived partners to be selectable
    partner_ids = fields.Many2many(
        "res.partner",
        string="Recipients",
        help="Contacts of the invoice that will receive the email.",
        context={"active_test": False},
        check_company=True,
    )

    @api.model
    def default_get(self, fields_list):
        _logger.error("🔥 ACCOUNT.INVOICE.SEND default_get")

        # 🔥 CRITICAL: allow archived partners during default computation
        self = self.with_context(active_test=False)

        res = super(AccountInvoiceSend, self).default_get(fields_list)

        active_ids = self.env.context.get("active_ids", [])
        if active_ids:
            moves = (
                self.env["account.move"]
                .with_context(active_test=False)
                .browse(active_ids)
            )

            partners = moves.mapped("partner_id").filtered(lambda p: p.email)
            if partners:
                res["partner_ids"] = [(6, 0, partners.ids)]
                _logger.error(f"🔥 Set partner_ids: {partners.ids}")

        return res

    def action_send_and_print(self):
        _logger.error("🔥 ACCOUNT.INVOICE.SEND action_send_and_print CALLED")
        _logger.error("🔥 Wizard partner_ids: %s", self.partner_ids.ids)

        ctx = dict(self.env.context)

        if self.partner_ids:
            ctx.update(
                {
                    "default_partner_ids": [(6, 0, self.partner_ids.ids)],
                    "active_test": False,
                }
            )

        return super(
            AccountInvoiceSend,
            self.with_context(
                ctx,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
            ),
        ).action_send_and_print()
