from odoo import fields, models


class AccountMoveContextual(models.Model):
    _inherit = 'account.move'

    contextual_note = fields.Text(
        string='Contextuele opmerking',
    )
