{
    "name": "Archived Contact Warning",
    "version": "1.0",
    "category": "Sales",
    "summary": "Show warning when using archived contacts",
    "depends": ["sale", "account"],
    "data": [
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "archived_partner_show_warning/static/src/css/style.css",
        ],
    },
    "installable": True,
    "application": False,
}
