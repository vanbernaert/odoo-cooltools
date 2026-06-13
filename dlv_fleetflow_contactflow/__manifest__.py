# -*- coding: utf-8 -*-
{
    "name": "FleetFlow ContactFlow API",
    "summary": "Expose Busenco trip drivers as a ContactFlow JSON API "
               "secured by an API key.",
    'description': """
Exposes trip.driver records as a JSON feed endpoint, consumed by the
WordPress dlv-odoo-contactflow plugin.

Endpoint: GET /fleetflow/contactflow/drivers?location=<location_name>

Authentication: Bearer token via Odoo native API keys.
Generate a key via Settings > Users > (user) > API Keys > New.
""",
    "author": "bv Domus La Vila",
    "website": "https://domuslavila.eu",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base", "busenco_custom"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}
