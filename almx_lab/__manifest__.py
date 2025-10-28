# -*- coding: utf-8 -*-
{
    'name': "Programable Products",

    'summary': """
        Módulo para reconocer productos programables dentro del sistema Odoo""",

    'description': """
        Este módulo añade secciones para indicar si un producto debe ser programado por laboratorio. 
        Si el producto es programable, se habilita una vista con la referencia interna del producto y 
        un botón para registrar el inicio, fin y duración total de la programación.
    """,

    'author': "Celia",
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
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/stock_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
