# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class almx_stock_extends(models.Model):
#     _name = 'almx_stock_extends.almx_stock_extends'
#     _description = 'almx_stock_extends.almx_stock_extends'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
