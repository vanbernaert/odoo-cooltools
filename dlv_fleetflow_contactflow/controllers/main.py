# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FleetFlowContactFlowController(http.Controller):

    @http.route(
        "/fleetflow/contactflow/drivers",
        type="http",
        auth="fleetflow_api_key",
        methods=["GET"],
        csrf=False,
    )
    def fleetflow_contactflow_drivers(self, location=None, **kwargs):
        """Return active trip drivers as ContactFlow JSON contacts.

        Optional query param ``location`` filters drivers on
        ``location_id.name``.
        """
        try:
            domain = [("active", "=", True)]
            if location:
                domain.append(("location_id.name", "=", location))

            drivers = request.env["trip.driver"].sudo().search(
                domain, order="name asc"
            )

            contacts = []
            for d in drivers:
                name = d.name or ""
                first_name, sep, last_name = name.partition(" ")
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

            return request.make_response(
                json.dumps({"contacts": contacts}),
                headers=[
                    ("Content-Type", "application/json;charset=utf-8"),
                ],
            )
        except Exception as exc:
            _logger.exception("FleetFlow ContactFlow: error building response")
            return request.make_response(
                json.dumps({"error": str(exc)}),
                headers=[
                    ("Content-Type", "application/json;charset=utf-8"),
                ],
                status=500,
            )
