from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    partner_is_archived = fields.Boolean(
        string='Partner Archived',
        compute='_compute_partner_is_archived',
        store=False
    )
    
    @api.depends('partner_id', 'partner_id.active')
    def _compute_partner_is_archived(self):
        for order in self:
            order.partner_is_archived = order.partner_id and not order.partner_id.active
