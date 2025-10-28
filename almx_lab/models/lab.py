# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
import datetime


class Labtask(models.Model):
    _name = 'lab.task'
    _description = 'Lab Task'

    id = fields.Integer(string='ID')
    picking_id = fields.Many2one('stock.picking', string='Stock Picking', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    date_start = fields.Datetime(string='Start Date', readonly=True)
    date_end = fields.Datetime(string='End Date', readonly=True)
    duration = fields.Char(string='Duration', readonly=True)
    state = fields.Selection([('draft', 'Sin iniciar'),
                              ('progress', 'En proceso'),
                              ('done', 'Hecho'), ],
                             string='State', default='draft', readonly=True)
    program_product = fields.Char(string='Program Product', readonly=True)

    def start_program(self):
        today_date = datetime.datetime.now()
        self.date_start = today_date.strftime("%Y-%m-%d %H:%M:%S")
        self.state = 'progress'

    def end_program(self):
        today_date = datetime.datetime.now()
        self.date_end = today_date.strftime("%Y-%m-%d %H:%M:%S")
        self.state = 'done'
        if self.state == 'done':
            if self.date_start and self.date_end:
                self.duration = self.date_end - self.date_start