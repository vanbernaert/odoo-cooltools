from odoo import fields, models


class SaleOrderContextual(models.Model):
    _inherit = 'sale.order'

    contextual_note = fields.Text(
        string='Contextuele opmerking',
    )

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        if self.contextual_note:
            vals['contextual_note'] = self.contextual_note
        return vals
