from odoo import models, api

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def generate_email(self, res_ids, fields=None):
        """Override to include archived partners for sales/invoices"""
        if self.model in ['sale.order', 'account.move']:
            return super(
                MailTemplate,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True
                )
            ).generate_email(res_ids, fields)
        
        return super().generate_email(res_ids, fields)