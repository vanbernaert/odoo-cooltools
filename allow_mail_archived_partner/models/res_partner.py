from odoo import models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """Include archived partners when context indicates email notifications"""
        # Check various context flags
        ctx = self.env.context
        
        should_include_archived = any([
            ctx.get('mail_notification'),
            ctx.get('include_archived_partners'),
            ctx.get('active_test') is False,
            'mail' in self._name.lower() if hasattr(self, '_name') else False,
            'notify' in str(ctx),
        ])
        
        if should_include_archived:
            # Remove any active=True filters
            new_args = []
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 3:
                    if arg[0] == 'active' and arg[1] == '=' and arg[2] is True:
                        continue  # Skip active=True filter
                new_args.append(arg)
            args = new_args
        
        return super()._search(args, offset=offset, limit=limit, order=order, 
                               count=count, access_rights_uid=access_rights_uid)

    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Override search method as well"""
        # Check context for email operations
        ctx = self.env.context
        
        should_include_archived = any([
            ctx.get('mail_notification'),
            ctx.get('include_archived_partners'),
            ctx.get('active_test') is False,
            'mail' in self._name.lower() if hasattr(self, '_name') else False,
        ])
        
        if should_include_archived:
            # Remove any active=True filters
            new_args = []
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 3:
                    if arg[0] == 'active' and arg[1] == '=' and arg[2] is True:
                        continue  # Skip active=True filter
                new_args.append(arg)
            args = new_args
        
        return super().search(args, offset=offset, limit=limit, order=order, count=count)