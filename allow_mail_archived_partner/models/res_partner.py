from odoo import models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """Override search to include archived partners in email context"""
        # Check context for specific email operations
        ctx = self.env.context
        
        # Check if this is an email operation for our target models
        model = ctx.get('active_model') or ctx.get('default_model')
        
        # Flag to indicate we're in email generation context
        is_email_generation = any([
            ctx.get('thread_model') in ['sale.order', 'account.move'],
            ctx.get('model') in ['sale.order', 'account.move'],
            'mail' in self._name.lower() if hasattr(self, '_name') else False
        ])
        
        if model in ['sale.order', 'account.move'] or is_email_generation:
            # Remove any active=True filters
            new_args = []
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 3:
                    if arg[0] == 'active' and arg[1] == '=' and arg[2] is True:
                        continue  # Skip active=True filters
                new_args.append(arg)
            args = new_args
        
        return super()._search(args, offset=offset, limit=limit, order=order, 
                               count=count, access_rights_uid=access_rights_uid)