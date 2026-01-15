import logging
_logger = logging.getLogger(__name__)

from odoo import models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """ALWAYS include archived partners for our module"""
        # Check if this is related to mail/notification
        if any(key in str(self.env.context) for key in ['mail', 'notify', 'message']):
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