# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    fleetflow_busenco_installed = fields.Boolean(
        string="busenco_custom installed",
        compute="_compute_fleetflow_busenco_installed",
        readonly=True,
        store=False,
    )

    @api.depends_context("uid")
    def _compute_fleetflow_busenco_installed(self):
        installed = self.env["ir.module.module"].sudo().search_count([
            ("name", "=", "busenco_custom"),
            ("state", "=", "installed"),
        ]) > 0
        for rec in self:
            rec.fleetflow_busenco_installed = installed
