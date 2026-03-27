from odoo import models


class AccountEdiCommon(models.AbstractModel):
    _inherit = 'account.edi.common'

    def _import_fill_invoice_line_taxes(
        self, journal, tax_nodes, invoice_line_form, inv_line_vals, logs
    ):
        """
        Override to apply the supplier's fiscal position tax mapping after
        the standard UBL tax detection.

        Odoo 16 does not apply fiscal positions to vendor bills during UBL
        import. The standard method only searches by percentage (amount=6,
        limit=1), ignoring fiscal position entirely. This override applies
        the partner's fiscal position mapping immediately after detection.
        """
        # Run standard tax detection first
        logs = super()._import_fill_invoice_line_taxes(
            journal, tax_nodes, invoice_line_form, inv_line_vals, logs
        )

        # Apply fiscal position mapping if the invoice has one
        move = invoice_line_form.move_id
        fiscal_position = move.fiscal_position_id

        if not fiscal_position or not inv_line_vals.get('taxes'):
            return logs

        detected_taxes = self.env['account.tax'].browse(inv_line_vals['taxes'])
        mapped_taxes = fiscal_position.map_tax(detected_taxes)

        if mapped_taxes != detected_taxes:
            inv_line_vals['taxes'] = mapped_taxes.ids
            invoice_line_form.tax_ids = mapped_taxes

        return logs

    def _import_fill_invoice_allowance_charge(
        self, tree, invoice, journal, qty_factor
    ):
        """
        Override to apply the supplier's fiscal position tax mapping to
        document-level allowance/charge lines (e.g. kortingen/toeslagen).

        These lines are created via a separate code path that does a raw
        tax search by percentage without applying fiscal position. We
        post-process the created lines to correct their taxes.
        """
        logs = super()._import_fill_invoice_allowance_charge(
            tree, invoice, journal, qty_factor
        )

        fiscal_position = invoice.fiscal_position_id
        if not fiscal_position:
            return logs

        # Allowance/charge lines are created with sequence=0
        allowance_lines = invoice.invoice_line_ids.filtered(
            lambda l: l.sequence == 0 and l.tax_ids
        )
        for line in allowance_lines:
            mapped_taxes = fiscal_position.map_tax(line.tax_ids)
            if mapped_taxes != line.tax_ids:
                line.tax_ids = mapped_taxes

        return logs
