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
        # REMOVE any domain that filters by active=True
        context={'active_test': False},  # Allow archived in searches
        check_company=True,
    )

    @api.model
    def default_get(self, fields):
        """
        Pre-fill invoice email wizard with archived partners.
        """
        _logger.debug("=== ACCOUNT.INVOICE.SEND DEFAULT_GET ===")
        
        res = super().default_get(fields)
        _logger.debug(f"Super result partner_ids: {res.get('partner_ids')}")
        
        active_ids = self.env.context.get('active_ids', [])
        _logger.debug(f"Active IDs: {active_ids}")
        
        if active_ids:
            # Find invoices with archived partners allowed
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            partner_ids = []
            for move in moves:
                if move.partner_id:
                    partner_ids.append(move.partner_id.id)
                    _logger.debug(f"Found partner {move.partner_id.id} for invoice {move.id}")
            
            if partner_ids:
                res['partner_ids'] = [(6, 0, partner_ids)]
                _logger.debug(f"SET partner_ids: {res['partner_ids']}")
        
        return res

    def _get_composer_values(self, res_ids, template):
        """
        Pass context to mail composer to allow archived partners.
        """
        _logger.debug("=== _get_composer_values ===")
        _logger.debug(f"Passing context to allow archived partners")
        # FIX: Changed include_archived_partner to include_archived_partners (plural)
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,  # FIXED: plural 's'
                mail_notify_force=True,
            )
        )._get_composer_values(res_ids, template)

    def action_send_and_print(self):
        """
        Override send action to add logging and ensure context is passed.
        """
        _logger.debug("=== ACCOUNT.INVOICE.SEND action_send_and_print ===")
        _logger.debug(f"Context before send: {dict(self.env.context)}")
        _logger.debug(f"Partner IDs: {self.partner_ids.ids}")
        
        # Ensure context is passed when calling action
        result = super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,  # Ensure mail_thread.py recognizes this
                mark_invoice_as_sent=True,  # Ensure mail_thread.py recognizes this
            )
        ).action_send_and_print()
        
        _logger.debug("Email send action completed")
        return result
    
    # Also override the regular send action if it exists
    def action_send(self):
        """
        Override send action (without print) to ensure context.
        """
        _logger.debug("=== ACCOUNT.INVOICE.SEND action_send ===")
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
            )
        ).action_send()