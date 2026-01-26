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
        _logger.debug("Passing context to allow archived partners")
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partner=True,
                mail_notify_force=True,
            )
        )._get_composer_values(res_ids, template)