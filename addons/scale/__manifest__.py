# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Scale',
    'version': '1.0',
    'category': 'Manufacturing',
    'author': "Luis Espindola",
    'sequence': 27,
    'summary': 'Truck weighting module',
    'description': "",
    'depends': [
        'base_setup',
        'mail',
        'calendar',
        'contacts',
        'stock',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}