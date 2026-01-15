from odoo import models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """Include archived partners when sending emails for sales/invoices"""
        # Check if this is for email notifications
        if self.env.context.get('mail_notification') or 'mail' in str(self._name):
            # Remove active=True filter
            args = [arg for arg in args if not (
                isinstance(arg, (list, tuple)) and 
                len(arg) == 3 and 
                arg[0] == 'active' and 
                arg[1] == '=' and 
                arg[2] is True
            )]
        return super()._search(args, offset=offset, limit=limit, order=order, 
                               count=count, access_rights_uid=access_rights_uid)