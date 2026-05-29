from odoo import fields, models


class SaleOrderContextual(models.Model):
    _inherit = 'sale.order'

    contextual_note = fields.Text(
        string='Contextuele opmerking',
    )
