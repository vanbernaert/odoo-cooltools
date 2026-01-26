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
        _logger.error("🔥 ACCOUNT.INVOICE.SEND default_get")
        
        res = super().default_get(fields)
        
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            partners = moves.mapped('partner_id').filtered(lambda p: p.email)
            if partners:
                res['partner_ids'] = [(6, 0, partners.ids)]
                _logger.error(f"🔥 Set partner_ids: {res['partner_ids']}")
        
        return res

    def action_send_and_print(self):
        _logger.error("🔥🔥🔥 ACCOUNT.INVOICE.SEND action_send_and_print CALLED 🔥🔥🔥")
        _logger.error(f"🔥 Wizard ID: {self.id}")
        _logger.error(f"🔥 Partner IDs: {self.partner_ids.ids}")
        _logger.error(f"🔥 Current context: {dict(self.env.context)}")
        
        # CRITICAL: Get the actual partner email for logging
        if self.partner_ids:
            for partner in self.partner_ids:
                _logger.error(f"🔥 Wizard partner: {partner.id} - {partner.name}, active={partner.active}, email={partner.email}")
        
        # Call parent with context AND ensure partner_ids are passed
        # We need to pass partner_ids to the message_post call
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
                # Add partner_ids to context so mail_thread can access them
                invoice_partner_ids=self.partner_ids.ids if self.partner_ids else [],
            )
        ).action_send_and_print()

    def _get_composer_values(self, res_ids, template):
        _logger.error("🔥 ACCOUNT.INVOICE.SEND _get_composer_values")
        
        # Also pass context to composer
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
                force_email=True,
                mark_invoice_as_sent=True,
            )
        )._get_composer_values(res_ids, template)