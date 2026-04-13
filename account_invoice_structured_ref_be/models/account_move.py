# -*- coding: utf-8 -*-
import re
from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_invoice_reference_be_structured(self):
        """Compute a Belgian structured communication (OGM/VCS) from the invoice name.

        1. Strip all non-digit characters from the invoice name.
        2. Zero-pad left to 10 digits.
        3. Check digits = (number % 97) or 97 if result is 0, zero-padded to 2 digits.
        4. Format: +++XXX/XXXX/XXXCC+++ (positions 0-2, 3-6, 7-9, then 2-digit check).
        """
        self.ensure_one()
        digits = re.sub(r'\D', '', self.name or '').zfill(10)
        check = int(digits) % 97 or 97
        cc = str(check).zfill(2)
        return '+++{}/{}/{}{}+++'.format(digits[0:3], digits[3:7], digits[7:10], cc)

    def _get_invoice_computed_reference(self):
        self.ensure_one()
        if self.journal_id.invoice_reference_type == 'be_structured':
            return self._get_invoice_reference_be_structured()
        return super()._get_invoice_computed_reference()
