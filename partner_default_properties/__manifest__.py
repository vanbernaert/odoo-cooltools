# -*- coding: utf-8 -*-
{
    'name': 'Partner Default Properties',
    'version': '16.0.1.0.0',
    'summary': 'Set company-wide defaults for fiscal position and payment terms on new customers',
    'category': 'Accounting',
    'author': 'Van Bernaert',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
