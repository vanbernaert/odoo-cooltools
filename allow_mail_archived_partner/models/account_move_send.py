import logging
_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    # Allow archived partners to remain selectable
    partner_ids = fields.Many2many(
        'res.partner',
        string='Recipients',
        help='Contacts of the invoice that will receive the email.',
        context={'active_test': False},
        check_company=True,
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)

            partners = moves.mapped('partner_id').filtered(lambda p: p.email)
            if partners:
                res['partner_ids'] = [(6, 0, partners.ids)]

        return res

    def action_send_and_print(self):
        """
        Explicitly set email_to on the wizard record.
        This is REQUIRED for account.invoice.send.
        """
        self.ensure_one()

        emails = [p.email for p in self.partner_ids if p.email]
        if not emails:
            _logger.warning("No recipient emails found; skipping send.")
            return {'type': 'ir.actions.act_window_close'}

        # 🔥 THIS is the critical line
        self.email_to = ",".join(emails)

        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
            )
        ).action_send_and_print()
