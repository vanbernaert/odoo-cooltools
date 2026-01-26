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
        _logger.info("=== ACCOUNT.INVOICE.SEND DEFAULT_GET ===")
        
        res = super().default_get(fields)
        _logger.info(f"Initial result: {res}")
        
        active_ids = self.env.context.get('active_ids', [])
        _logger.info(f"Active IDs: {active_ids}")
        
        if active_ids:
            # Find invoices with archived partners allowed
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            partners = moves.mapped('partner_id').filtered(lambda p: p.email)
            _logger.info(f"Found partners: {partners.ids}")
            
            if partners:
                # Set BOTH fields
                res['partner_ids'] = [(6, 0, partners.ids)]
                res['email_to'] = ",".join(partners.mapped('email'))
                _logger.info(f"Set partner_ids: {res['partner_ids']}")
                _logger.info(f"Set email_to: {res['email_to']}")
        
        return res

    def action_send_and_print(self):
        """
        Ensure email_to is set before sending.
        """
        _logger.info("=== ACCOUNT.INVOICE.SEND action_send_and_print ===")
        _logger.info(f"Wizard ID: {self.id}")
        _logger.info(f"Partner IDs: {self.partner_ids.ids}")
        _logger.info(f"Current email_to: {self.email_to}")
        
        # Ensure email_to is set from partner_ids
        if self.partner_ids and not self.email_to:
            emails = [p.email for p in self.partner_ids if p.email]
            if emails:
                self.email_to = ",".join(emails)
                _logger.info(f"Updated email_to: {self.email_to}")
        
        # Also ensure partner_ids are written to the record
        if self.partner_ids:
            _logger.info(f"Writing partner_ids to record")
            self.write({'partner_ids': [(6, 0, self.partner_ids.ids)]})
        
        _logger.info(f"Final context before send: {dict(self.env.context)}")
        
        # Call parent with context
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

    def write(self, vals):
        """
        Ensure when partner_ids are written, email_to is also updated.
        """
        _logger.info("=== ACCOUNT.INVOICE.SEND WRITE ===")
        _logger.info(f"Write vals keys: {vals.keys()}")
        
        if 'partner_ids' in vals and not vals.get('email_to'):
            # Get partner emails
            partner_ids = vals['partner_ids'][0][2] if vals['partner_ids'] else []
            _logger.info(f"Partner IDs in write: {partner_ids}")
            
            if partner_ids:
                partners = self.env['res.partner'].with_context(
                    active_test=False
                ).browse(partner_ids)
                emails = [p.email for p in partners if p.email]
                if emails:
                    vals['email_to'] = ",".join(emails)
                    _logger.info(f"Auto-updated email_to in write: {vals['email_to']}")
        
        result = super().write(vals)
        _logger.info(f"Write completed")
        return result