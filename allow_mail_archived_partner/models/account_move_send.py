from odoo import models, api


class AccountMoveSend(models.TransientModel):
    _inherit = "account.move.send"

    @api.model
    def _get_default_mail_partner_ids(self, move, mail_template, mail_lang):
        """
        The invoice 'Send by Email' wizard uses this to compute partner_ids (To:).
        We must disable active_test here to include archived partners.
        """
        wiz = self.with_context(active_test=False, include_archived_partners=True)
        return super(AccountMoveSend, wiz)._get_default_mail_partner_ids(move, mail_template, mail_lang)
