from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    partner_is_archived = fields.Boolean(
        string='Partner Archived',
        compute='_compute_partner_is_archived',
        store=False
    )
    
    @api.depends('partner_id', 'partner_id.active')
    def _compute_partner_is_archived(self):
        for invoice in self:
            invoice.partner_is_archived = invoice.partner_id and not invoice.partner_id.active
