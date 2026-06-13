# -*- coding: utf-8 -*-
{
    "name": "FleetFlow ContactFlow API",
    "summary": "Expose Busenco trip drivers as a ContactFlow JSON API "
               "secured by an API key.",
    "description": """
        FleetFlow ContactFlow API
        =========================

        Provides a token-authenticated HTTP endpoint that returns the active
        trip drivers (busenco_custom ``trip.driver``) as JSON contacts,
        optionally filtered by office location.
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
