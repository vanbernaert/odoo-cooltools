import logging
_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"


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
                res['email_to'] = ", ".join(partners.mapped('email'))

        return res

    def action_send_and_print(self):
        _logger.info("=== ACCOUNT.INVOICE.SEND action_send_and_print ===")
        _logger.info(f"Wizard ID: {self.id}, Partners: {self.partner_ids.ids}")
        
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

    # LOG ALL POSSIBLE ACTIONS
    def action_send(self):
        _logger.info("=== ACCOUNT.INVOICE.SEND action_send ===")
        return super().action_send()

    def send_and_print_action(self):
        _logger.info("=== ACCOUNT.INVOICE.SEND send_and_print_action ===")
        return super().send_and_print_action()

    def print_action(self):
        _logger.info("=== ACCOUNT.INVOICE.SEND print_action ===")
        return super().print_action()

    @api.model
    def action_send_and_print_invoices(self, invoices):
        _logger.info("=== ACCOUNT.INVOICE.SEND action_send_and_print_invoices ===")
        return super().action_send_and_print_invoices(invoices)