{
    'name': 'Sale Order Contextual Note',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Adds a contextual note field to sale orders and invoices',
    'author': 'DomusLavila',
    'depends': ['sale_management', 'account'],
    'data': [
        'views/sale_order_contextual_view.xml',
        'views/account_move_form.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
