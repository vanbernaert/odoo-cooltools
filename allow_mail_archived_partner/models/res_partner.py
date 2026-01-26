import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    _logger.info("=== RES.PARTNER CLASS LOADED (allow_mail_archived_partner) ===")

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        Allow archived partners when context permits.
        """
        _logger.info("=== ResPartner._search ===")
        _logger.info(f"Search args: {args}")
        _logger.info(f"Context include_archived_partners: {self.env.context.get('include_archived_partners')}")
        _logger.info(f"Context mail_notify_force: {self.env.context.get('mail_notify_force')}")
        _logger.info(f"Context force_email: {self.env.context.get('force_email')}")
        _logger.info(f"Context mark_invoice_as_sent: {self.env.context.get('mark_invoice_as_sent')}")
        _logger.info(f"Full context active_test: {self.env.context.get('active_test')}")
        
        # Check if we should include archived partners
        include_archived = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force") or
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent")
        )
        
        if include_archived:
            _logger.info("✓ CONTEXT FLAGS FOUND - Allowing archived partners")
            
            # Remove both active and partner_share filters
            filtered_args = []
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 3:
                    # Skip active filters
                    if arg[0] == "active":
                        _logger.info(f"  Removing active filter: {arg}")
                        continue
                    # Skip partner_share filter for manual sends
                    if arg[0] == "partner_share" and arg[1] == "=" and arg[2] is True:
                        _logger.info(f"  Removing partner_share filter: {arg}")
                        continue
                
                filtered_args.append(arg)
            
            args = filtered_args
            self = self.with_context(active_test=False)
            _logger.info(f"Search args after cleanup: {args}")
        
        result = super()._search(args, offset, limit, order, count, access_rights_uid)
        
        if not count:
            result_ids = list(result)
            _logger.info(f"Search returned {len(result_ids)} results")
            if result_ids:
                _logger.info(f"First 5 result IDs: {result_ids[:5]}")
        
        return result