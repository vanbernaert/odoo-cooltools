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
        _logger.error("🔥 RES.PARTNER._search CALLED 🔥")
        _logger.error(f"🔥 Search args: {args}")
        _logger.error(f"🔥 Context include_archived_partners: {self.env.context.get('include_archived_partners')}")
        _logger.error(f"🔥 Context mail_notify_force: {self.env.context.get('mail_notify_force')}")
        _logger.error(f"🔥 Context force_email: {self.env.context.get('force_email')}")
        _logger.error(f"🔥 Context mark_invoice_as_sent: {self.env.context.get('mark_invoice_as_sent')}")
        _logger.error(f"🔥 Context active_test: {self.env.context.get('active_test')}")
        
        # Check if we should include archived partners
        include_archived = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force") or
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent")
        )
        
        _logger.error(f"🔥 Should include archived? {include_archived}")
        
        if include_archived:
            _logger.error("🔥🔥🔥 RES.PARTNER: CONTEXT FLAGS FOUND - Allowing archived partners 🔥🔥🔥")
            
            # Remove both active and partner_share filters
            filtered_args = []
            for arg in args:
                if isinstance(arg, (list, tuple)) and len(arg) == 3:
                    # Skip active filters
                    if arg[0] == "active":
                        _logger.error(f"🔥 Removing active filter: {arg}")
                        continue
                    # Skip partner_share filter for manual sends
                    if arg[0] == "partner_share" and arg[1] == "=" and arg[2] is True:
                        _logger.error(f"🔥 Removing partner_share filter: {arg}")
                        continue
                    # Also remove active in ('=', 'in', 'not in') with any value
                    if arg[0] == "active" and arg[1] in ("=", "in", "not in"):
                        _logger.error(f"🔥 Removing active filter (any value): {arg}")
                        continue
                
                filtered_args.append(arg)
            
            args = filtered_args
            self = self.with_context(active_test=False)
            _logger.error(f"🔥 Search args after cleanup: {args}")
        
        result = super()._search(args, offset, limit, order, count, access_rights_uid)
        
        if not count:
            result_ids = list(result)
            _logger.error(f"🔥 Search returned {len(result_ids)} results")
            if result_ids:
                _logger.error(f"🔥 First 3 result IDs: {result_ids[:3]}")
                # Get partner details for debugging
                partners = self.browse(result_ids[:3])
                for partner in partners:
                    _logger.error(f"🔥 Partner {partner.id}: {partner.name}, active={partner.active}, email={partner.email}")
        
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """
        Also override name_search to include archived partners when context allows.
        """
        _logger.error(f"🔥 RES.PARTNER._name_search CALLED: name='{name}', args={args}")
        
        # Check if we should include archived partners
        include_archived = (
            self.env.context.get("include_archived_partners") or
            self.env.context.get("mail_notify_force") or
            self.env.context.get("force_email") or
            self.env.context.get("mark_invoice_as_sent")
        )
        
        if include_archived:
            _logger.error("🔥 _name_search: Allowing archived partners")
            # Remove active filters from args
            if args is None:
                args = []
            args = [
                arg for arg in args
                if not (isinstance(arg, (list, tuple)) and len(arg) == 3 and arg[0] == "active")
            ]
            self = self.with_context(active_test=False)
        
        return super()._name_search(
            name=name, args=args, operator=operator, 
            limit=limit, name_get_uid=name_get_uid
        )