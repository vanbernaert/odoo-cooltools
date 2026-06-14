# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FleetFlowContactFlowController(http.Controller):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _json_response(payload, status=200):
        """Return a JSON HTTP response with the ContactFlow content type."""
        return request.make_response(
            json.dumps(payload),
            headers=[("Content-Type", "application/json;charset=utf-8")],
            status=status,
        )

    @staticmethod
    def _busenco_installed():
        """Return True when the busenco_custom module is installed."""
        return request.env["ir.module.module"].sudo().search_count([
            ("name", "=", "busenco_custom"),
            ("state", "=", "installed"),
        ]) > 0

    @staticmethod
    def _split_name(name):
        """Split a free-text name on the first space into (first, last)."""
        first_name, _sep, last_name = (name or "").partition(" ")
        return first_name, last_name

    # ------------------------------------------------------------------
    # Drivers (requires busenco_custom)
    # ------------------------------------------------------------------
    @http.route(
        "/fleetflow/contactflow/drivers",
        type="http",
        auth="fleetflow_api_key",
        methods=["GET"],
        csrf=False,
    )
    def get_drivers(self, location=None, **kwargs):
        """Return active trip drivers as ContactFlow JSON contacts.

        Optional query param ``location`` filters drivers on
        ``location_id.name``. Returns 404 when busenco_custom is not installed.
        """
        if not self._busenco_installed():
            return self._json_response(
                {
                    "error": "busenco_custom module is not installed. "
                             "The drivers endpoint is unavailable."
                },
                status=404,
            )

        try:
            domain = [("active", "=", True)]
            if location:
                domain.append(("location_id.name", "=", location))

            drivers = request.env["trip.driver"].sudo().search(
                domain, order="name asc"
            )

            contacts = []
            for d in drivers:
                first_name, last_name = self._split_name(d.name)
                contacts.append({
                    "id": str(d.id),
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": d.phone_number or "",
                    "mobile": d.phone_number2 or "",
                    "email": d.email or "",
                })

            _logger.info(
                "FleetFlow ContactFlow: returned %s drivers (location=%s)",
                len(contacts), location,
            )

            return self._json_response({"contacts": contacts})
        except Exception as exc:
            _logger.exception("FleetFlow ContactFlow: error building drivers response")
            return self._json_response({"error": str(exc)}, status=500)

    # ------------------------------------------------------------------
    # Customers
    # ------------------------------------------------------------------
    @http.route(
        "/fleetflow/contactflow/customers",
        type="http",
        auth="fleetflow_api_key",
        methods=["GET"],
        csrf=False,
    )
    def get_customers(self, **kwargs):
        """Return active customer partners (with a phone or mobile) as contacts."""
        return self._partner_feed(
            rank_field="customer_rank", label="customers"
        )

    # ------------------------------------------------------------------
    # Suppliers
    # ------------------------------------------------------------------
    @http.route(
        "/fleetflow/contactflow/suppliers",
        type="http",
        auth="fleetflow_api_key",
        methods=["GET"],
        csrf=False,
    )
    def get_suppliers(self, **kwargs):
        """Return active supplier partners (with a phone or mobile) as contacts."""
        return self._partner_feed(
            rank_field="supplier_rank", label="suppliers"
        )

    # ------------------------------------------------------------------
    # Shared res.partner feed
    # ------------------------------------------------------------------
    def _partner_feed(self, rank_field, label):
        """Build a ContactFlow feed from res.partner filtered by rank field."""
        try:
            domain = [
                ("active", "=", True),
                (rank_field, ">", 0),
                "|",
                ("phone", "!=", False),
                ("mobile", "!=", False),
            ]

            partners = request.env["res.partner"].sudo().search(
                domain, order="name asc"
            )

            contacts = []
            for p in partners:
                if p.is_company:
                    first_name = ""
                    last_name = p.name or ""
                else:
                    first_name, last_name = self._split_name(p.name)
                contacts.append({
                    "id": str(p.id),
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": p.phone or "",
                    "mobile": p.mobile or "",
                    "email": p.email or "",
                })

            _logger.info(
                "FleetFlow ContactFlow: returned %s %s", len(contacts), label
            )

            return self._json_response({"contacts": contacts})
        except Exception as exc:
            _logger.exception(
                "FleetFlow ContactFlow: error building %s response", label
            )
            return self._json_response({"error": str(exc)}, status=500)
