import logging
_logger = logging.getLogger(__name__)

from odoo import models, api, fields


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    # OVERRIDE THE FIELD DEFINITION to remove domain filter
    partner_ids = fields.Many2many(
        'res.partner',
        string='Recipients',
        help='Contacts of the invoice that will receive the email.',
        context={'active_test': False},
        check_company=True,
    )

    @api.model
    def default_get(self, fields):
        """
        Pre-fill invoice email wizard with archived partners.
        """
        _logger.info("=== ACCOUNT.INVOICE.SEND DEFAULT_GET ===")
        _logger.info(f"Fields requested: {fields}")
        _logger.info(f"Context: {dict(self.env.context)}")
        
        # Get default result first
        res = super().default_get(fields)
        _logger.info(f"Super result partner_ids: {res.get('partner_ids')}")
        
        active_ids = self.env.context.get('active_ids', [])
        _logger.info(f"Active IDs: {active_ids}")
        
        if active_ids:
            # Find invoices with archived partners allowed
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            partner_ids = []
            for move in moves:
                if move.partner_id:
                    partner_ids.append(move.partner_id.id)
                    _logger.info(f"Found partner {move.partner_id.id} (active={move.partner_id.active}) for invoice {move.id}")
            
            if partner_ids:
                res['partner_ids'] = [(6, 0, partner_ids)]
                _logger.info(f"SET partner_ids: {res['partner_ids']}")
            else:
                _logger.info("No partners found for invoices")
        
        return res

    def _get_composer_values(self, res_ids, template):
        """
        Pass context to mail composer to allow archived partners.
        """
        _logger.info("=== ACCOUNT.INVOICE.SEND _get_composer_values ===")
        _logger.info(f"Passing context to allow archived partners")
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
            )
        )._get_composer_values(res_ids, template)

    def action_send_and_print(self):
        """
        Override send action to add logging and ensure context is passed.
        """
        _logger.info("=== ACCOUNT.INVOICE.SEND action_send_and_print ===")
        _logger.info(f"Wizard ID: {self.id}")
        _logger.info(f"Partner IDs: {self.partner_ids.ids}")
        _logger.info(f"Context before: {dict(self.env.context)}")
        
        # Ensure context is passed when calling action
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
        
        _logger.info("Email send action completed")
        return result