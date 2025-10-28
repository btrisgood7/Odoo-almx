# -*- coding: utf-8 -*-
# from odoo import http


# class AlmxProgramProducts(http.Controller):
#     @http.route('/almx_program_products/almx_program_products', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almx_program_products/almx_program_products/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('almx_program_products.listing', {
#             'root': '/almx_program_products/almx_program_products',
#             'objects': http.request.env['almx_program_products.almx_program_products'].search([]),
#         })

#     @http.route('/almx_program_products/almx_program_products/objects/<model("almx_program_products.almx_program_products"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almx_program_products.object', {
#             'object': obj
#         })
