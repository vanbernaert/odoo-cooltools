{
    "name": "Partner Hierarchical Name",
    "version": "16.0.1.0.0",
    "summary": "Show full partner hierarchy in dropdowns (Company / Delivery / Contact)",
    "category": "Contacts",
    "author": "Van Bernaert (Developer), Domus La Vila (Distributor)",
    "license": "LGPL-3",
    "depends": ["base"],
    "installable": True,
    "application": False,

    "assets": {
        "web.assets_backend": [
            "partner_hierarchical_name/static/src/css/many2one_dropdown.css",
        ],
    },
}
