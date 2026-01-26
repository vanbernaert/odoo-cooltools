from odoo import models, api


class AccountMoveSendWizard(models.TransientModel):
    _inherit = "account.move.send.wizard"

    @api.model
    def _get_default_mail_partner_ids(self, move, mail_template, mail_lang):
        """
        Allow archived partners when sending invoices via
        the 'Send by Email' wizard.
        """
        # Force archived partners to be visible ONLY in this context
        wiz = self.with_context(
            active_test=False,
            include_archived_partners=True,
        )

        return super(
            AccountMoveSendWizard,
            wiz
        )._get_default_mail_partner_ids(move, mail_template, mail_lang)
