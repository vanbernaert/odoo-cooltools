import logging
_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"


    @api.model
    def default_get(self, fields):
        _logger.info("=== ACCOUNT.INVOICE.SEND DEFAULT_GET ===")
        
        res = super().default_get(fields)
        
        active_ids = self.env.context.get('active_ids', [])
        
        if active_ids:
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            partner_ids = []
            for move in moves:
                if move.partner_id:
                    partner_ids.append(move.partner_id.id)
            
            if partner_ids:
                res['partner_ids'] = [(6, 0, partner_ids)]
                _logger.info(f"SET partner_ids: {res['partner_ids']}")
        
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