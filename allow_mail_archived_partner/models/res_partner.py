import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        DEBUG search method - FIXED for Odoo 16 Query object
        """
        _logger.info("=== RES.PARTNER _search ===")
        _logger.info(f"Search args before: {args}")
        _logger.info(f"Context include_archived: {self.env.context.get('include_archived_partners')}")
        _logger.info(f"Context active_test: {self.env.context.get('active_test')}")
        
        if self.env.context.get("include_archived_partners") or self.env.context.get("mail_notify_force"):
            _logger.info("Context flags found - removing active filters")
            # Remove active filters
            args = [
                arg for arg in args
                if not (
                    isinstance(arg, (list, tuple))
                    and len(arg) == 3
                    and arg[0] == "active"
                )
            ]
            self = self.with_context(active_test=False)
            _logger.info(f"Search args after: {args}")
        
        # Call parent
        result = super()._search(args, offset, limit, order, count, access_rights_uid)
        
        # FIX: Don't try to slice Query object
        if not count:
            # Convert to list to check results (only for debugging)
            result_ids = list(result)
            _logger.info(f"Search returned {len(result_ids)} results")
            if result_ids:
                _logger.info(f"First few result IDs: {result_ids[:10]}")
        else:
            _logger.info(f"Search count result: {result}")
        
        return result