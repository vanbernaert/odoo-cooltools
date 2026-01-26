from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        Remove active filters when context indicates manual email send
        (to allow finding archived partners).
        """
        # Check for manual email context
        include_archived = (
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent") or
            self.env.context.get("mail_notify_force")
        )
        
        if include_archived:
            # Remove active filters to include archived partners
            args = [
                arg for arg in args
                if not (isinstance(arg, (list, tuple)) and 
                       len(arg) == 3 and 
                       arg[0] == "active")
            ]
            self = self.with_context(active_test=False)
        
        return super()._search(args, offset, limit, order, count, access_rights_uid)