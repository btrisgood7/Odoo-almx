# -*- coding: utf-8 -*-
# from odoo import http


# class AlmxStockExtends(http.Controller):
#     @http.route('/almx_stock_extends/almx_stock_extends', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almx_stock_extends/almx_stock_extends/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('almx_stock_extends.listing', {
#             'root': '/almx_stock_extends/almx_stock_extends',
#             'objects': http.request.env['almx_stock_extends.almx_stock_extends'].search([]),
#         })

#     @http.route('/almx_stock_extends/almx_stock_extends/objects/<model("almx_stock_extends.almx_stock_extends"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almx_stock_extends.object', {
#             'object': obj
#         })
