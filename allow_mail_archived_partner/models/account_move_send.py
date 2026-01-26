from odoo import models, api


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.model
    def _get_default_mail_partner_ids(self, move, mail_template, mail_lang):
        """
        Allow archived partners when sending invoices via
        the 'Send by Email' wizard.
        """
        wiz = self.with_context(
            active_test=False,
            include_archived_partners=True,
        )
        return super(
            AccountInvoiceSend,
            wiz
        )._get_default_mail_partner_ids(move, mail_template, mail_lang)
