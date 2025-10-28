# -*- coding: utf-8 -*-
{
    'name': "almx_stock_extends",

    'summary': """
        Módulo para relacionar los picks y outs""",

    'description': """
        Este módulo relaciona de manera automatica los picks y outs con un campo readonly cuando son creados por el sistema.
        Cuando son creados manualmente, se crea un campo many2one para que se pueda seleccionar el el pick u out correspondiente.
    """,

    'author': "Celia y Jorge",
    'website': "www.alam.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '16',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/stock_view.xml',
        'views/sale_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
