from odoo import models, api


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.model
    def _get_default_mail_partner_ids(self, move, mail_template, mail_lang):
        """
        Allow archived partners to be included as recipients when
        sending invoices via the 'Send by Email' wizard.
        This is the ONLY place where partner_ids are computed.
        """
        # Temporarily disable active_test so archived partners are not filtered out
        wiz = self.with_context(
            active_test=False,
            include_archived_partners=True,
        )

        return super(
            AccountInvoiceSend,
            wiz
        )._get_default_mail_partner_ids(move, mail_template, mail_lang)
