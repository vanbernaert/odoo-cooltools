from odoo import models, api


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.model
    def default_get(self, fields):
        """
        Override default_get to pre-fill archived partners.
        This is often called BEFORE _get_default_mail_partner_ids.
        """
        res = super().default_get(fields)
        
        # Check if we're in the right context
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        
        if active_model == 'account.move' and active_ids:
            # Get the moves with archived partners allowed
            moves = self.env['account.move'].with_context(
                active_test=False
            ).browse(active_ids)
            
            # Collect all unique partners from the moves
            partner_ids = set()
            for move in moves:
                if move.partner_id and move.partner_id.email:
                    partner_ids.add(move.partner_id.id)
            
            if partner_ids:
                res['partner_ids'] = [(6, 0, list(partner_ids))]
        
        return res

    @api.model
    def _get_default_mail_partner_ids(self, move, mail_template, mail_lang):
        """
        Also fix this method to include archived partners.
        """
        wiz = self.with_context(
            active_test=False,
            include_archived_partners=True,
        )
        return super(
            AccountInvoiceSend,
            wiz
        )._get_default_mail_partner_ids(move, mail_template, mail_lang)
    
    def _get_mail_composer_values(self, move, template, partner_ids):
        """
        Ensure context is passed to mail composer.
        """
        return super(
            AccountInvoiceSend,
            self.with_context(
                active_test=False,
                include_archived_partners=True,
                mail_notify_force=True,
            )
        )._get_mail_composer_values(move, template, partner_ids)