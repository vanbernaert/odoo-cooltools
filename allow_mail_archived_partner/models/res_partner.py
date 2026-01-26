import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        SIMPLE: Just remove active filters when context says to include archived.
        """
        _logger.error("🔥 RES.PARTNER._search - Checking for archived context")
        _logger.error(f"🔥 Context force_email: {self.env.context.get('force_email')}")
        _logger.error(f"🔥 Context mark_invoice_as_sent: {self.env.context.get('mark_invoice_as_sent')}")
        _logger.error(f"🔥 Context mail_notify_force: {self.env.context.get('mail_notify_force')}")
        
        # Check for manual email context
        include_archived = (
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent") or
            self.env.context.get("mail_notify_force")
        )
        
        _logger.error(f"🔥 Should include archived? {include_archived}")
        
        if include_archived:
            _logger.error("🔥 Removing active filters for archived partners")
            # Simple: remove active filters
            args = [
                arg for arg in args
                if not (isinstance(arg, (list, tuple)) and 
                       len(arg) == 3 and 
                       arg[0] == "active")
            ]
            self = self.with_context(active_test=False)
            _logger.error(f"🔥 Search args after: {args}")
        
        result = super()._search(args, offset, limit, order, count, access_rights_uid)
        
        if not count:
            result_ids = list(result)
            _logger.error(f"🔥 Search returned {len(result_ids)} results")
        
        return result