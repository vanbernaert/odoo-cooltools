import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.model
    def default_get(self, fields):
        """
        Force inclusion of archived partners for invoice email wizard
        """
        _logger.info("=== ACCOUNT.INVOICE.SEND DEFAULT_GET ===")
        _logger.info(f"Fields: {fields}")
        _logger.info(f"Context: {self.env.context}")
        
        # Get the default result first
        res = super().default_get(fields)
        _logger.info(f"Super result partner_ids: {res.get('partner_ids')}")
        
        active_ids = self.env.context.get('active_ids', [])
        _logger.info(f"Active IDs: {active_ids}")
        
        if active_ids:
            # Find invoices WITH archived partners allowed
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
        Pass context to allow archived partners in email composition
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