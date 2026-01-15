import logging
_logger = logging.getLogger(__name__)

from odoo import models, api

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def generate_email(self, res_ids, fields=None):
        """Override to include archived partners for sales/invoices"""
        _logger.info("=== MailTemplate.generate_email ===")
        _logger.info(f"Template: {self.name}")
        _logger.info(f"Model: {self.model}")
        _logger.info(f"Res IDs: {res_ids}")
        _logger.info(f"Current context: {dict(self.env.context)}")
        
        if self.model in ['sale.order', 'account.move']:
            _logger.info("Adding active_test=False context for sales/invoice")
            return super(
                MailTemplate,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True
                )
            ).generate_email(res_ids, fields)
        
        return super().generate_email(res_ids, fields)