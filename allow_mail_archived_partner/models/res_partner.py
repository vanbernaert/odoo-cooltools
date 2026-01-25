import logging
_logger = logging.getLogger(__name__)

from odoo import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None
    ):
        """
        Only include archived partners when the caller explicitly opts in via:
            context['include_archived_partners'] = True

        Never key off fragile string matches like 'mail'/'notify'/'message'.
        """
        if self.env.context.get("include_archived_partners"):
            # Remove explicit active=True filters only (do not touch other domains)
            args = [
                arg for arg in args
                if not (
                    isinstance(arg, (list, tuple))
                    and len(arg) == 3
                    and arg[0] == "active"
                    and arg[1] == "="
                    and arg[2] is True
                )
            ]
            # Also ensure active_test is off so ORM won't auto-filter archived partners
            self = self.with_context(active_test=False)

        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid
        )
