import logging
_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    _logger.info("=== ACCOUNT.INVOICE.SEND CLASS LOADED ===")

    # OVERRIDE THE FIELD DEFINITION to remove domain filter
    partner_ids = fields.Many2many(
        'res.partner',
        string='Recipients',
        help='Contacts of the invoice that will receive the email.',
        context={'active_test': False},
        check_company=True,
    )

    @api.model
    def create(self, vals):
        _logger.info("=== ACCOUNT.INVOICE.SEND CREATE ===")
        _logger.info(f"Create vals: {vals}")
        return super().create(vals)

    def write(self, vals):
        _logger.info("=== ACCOUNT.INVOICE.SEND WRITE ===")
        _logger.info(f"Write vals: {vals}")
        return super().write(vals)

    @api.model
    def default_get(self, fields):
        _logger.info("=== ACCOUNT.INVOICE.SEND DEFAULT_GET ===")
        _logger.info(f"Fields: {fields}")
        
        res = super().default_get(fields)
        _logger.info(f"Result: {res}")
        
        return res

    def action_send_and_print(self):
        _logger.info("=== ACCOUNT.INVOICE.SEND ACTION_SEND_AND_PRINT ===")
        _logger.info(f"Self ID: {self.id}")
        _logger.info(f"Partner IDs: {self.partner_ids.ids}")
        
        # Call parent with ALL context flags
        result = super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
            )
        ).action_send_and_print()
        
        _logger.info(f"Action result: {result}")
        return result

    # Also try overriding _process_send_and_print which might be the actual method
    def _process_send_and_print(self, invoice, template):
        _logger.info("=== ACCOUNT.INVOICE.SEND _PROCESS_SEND_AND_PRINT ===")
        _logger.info(f"Invoice: {invoice.id}, Template: {template.id}")
        
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
            )
        )._process_send_and_print(invoice, template)