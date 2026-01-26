import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        """
        DEBUG VERSION - Trace everything
        """
        _logger.info("=== MAIL.COMPOSE.MESSAGE DEFAULT_GET START ===")
        _logger.info(f"Context: {dict(self.env.context)}")
        _logger.info(f"Fields requested: {fields}")
        
        res = super().default_get(fields)
        _logger.info(f"Super result partner_ids: {res.get('partner_ids')}")
        
        model = self.env.context.get("active_model")
        res_id = self.env.context.get("active_id")
        _logger.info(f"Active model: {model}, Active ID: {res_id}")
        
        if model == "account.move" and res_id:
            _logger.info(f"Processing invoice {res_id}")
            
            # Test 1: Without context
            invoice_normal = self.env["account.move"].browse(res_id)
            _logger.info(f"Normal browse - Partner: {invoice_normal.partner_id.id if invoice_normal.partner_id else 'None'}")
            _logger.info(f"Normal browse - Partner active: {invoice_normal.partner_id.active if invoice_normal.partner_id else 'N/A'}")
            
            # Test 2: With context
            invoice_with_context = self.env["account.move"].with_context(
                active_test=False
            ).browse(res_id)
            _logger.info(f"With context - Partner: {invoice_with_context.partner_id.id if invoice_with_context.partner_id else 'None'}")
            
            # Test 3: Direct partner search
            if invoice_normal.partner_id:
                partner = self.env["res.partner"].with_context(
                    active_test=False
                ).search([('id', '=', invoice_normal.partner_id.id)])
                _logger.info(f"Direct partner search found: {len(partner)} partners")
            
            # Now do the actual logic
            invoice = self.env["account.move"].with_context(
                active_test=False
            ).browse(res_id)
            
            if invoice.exists():
                _logger.info(f"Invoice exists: {invoice.exists()}")
                _logger.info(f"Invoice partner: {invoice.partner_id.id if invoice.partner_id else 'None'}")
                _logger.info(f"Invoice partner email: {invoice.partner_id.email if invoice.partner_id else 'None'}")
                
                if invoice.partner_id:
                    res["partner_ids"] = [(6, 0, [invoice.partner_id.id])]
                    _logger.info(f"SET partner_ids to: {res['partner_ids']}")
        
        _logger.info("=== MAIL.COMPOSE.MESSAGE DEFAULT_GET END ===")
        return res

    def _prepare_mail_values(self, res_ids):
        """
        Debug this too
        """
        _logger.info("=== _prepare_mail_values START ===")
        _logger.info(f"Context before: {dict(self.env.context)}")
        
        model = self.env.context.get("active_model") or self.model
        _logger.info(f"Model: {model}, res_ids: {res_ids}")
        
        if model in ["sale.order", "account.move"]:
            _logger.info(f"Setting context for {model} to allow archived partners")
            result = super(
                MailComposeMessage,
                self.with_context(
                    active_test=False,
                    include_archived_partners=True,
                    mail_notify_force=True,
                )
            )._prepare_mail_values(res_ids)
            _logger.info(f"Context after: {dict(self.env.context)}")
            _logger.info("=== _prepare_mail_values END ===")
            return result
        
        result = super()._prepare_mail_values(res_ids)
        _logger.info("=== _prepare_mail_values END ===")
        return result

    def _prepare_recipient_values(self, partner):
        """
        Debug recipient values
        """
        _logger.info(f"=== _prepare_recipient_values ===")
        _logger.info(f"Partner: {partner.id if partner else 'None'}")
        _logger.info(f"Partner active: {partner.active if partner else 'N/A'}")
        _logger.info(f"Context include_archived: {self.env.context.get('include_archived_partners')}")
        _logger.info(f"Context mail_notify_force: {self.env.context.get('mail_notify_force')}")
        
        include_archived = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force")
        )
        
        if include_archived and partner and not partner.active:
            _logger.info(f"Including archived partner {partner.name}")
            result = {
                "partner_id": partner.id,
                "email": partner.email,
                "name": partner.name,
                "lang": partner.lang or self.env.context.get("lang") or "en_US",
            }
            _logger.info(f"Returning: {result}")
            return result
        
        parent_result = super()._prepare_recipient_values(partner)
        _logger.info(f"Parent returning: {parent_result}")
        return parent_result