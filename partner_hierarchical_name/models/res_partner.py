from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def name_get(self):
        result = []

        for partner in self:
            names = []
            current = partner

            # Walk up the hierarchy
            while current:
                if current.name:
                    names.append(current.name)
                current = current.parent_id

            # Reverse to show top-down (L1 / L2 / L3)
            full_name = " / ".join(reversed(names))

            result.append((partner.id, full_name))

        return result
