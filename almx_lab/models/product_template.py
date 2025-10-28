from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product' #Herencia del módelo producto

    verification_lab = fields.Boolean(string='Producto Programable', help='Verifica si producto es programable por el equipo de Laboratorio')
    stock_it = fields.Boolean(string='Equipo de IT', help='Verifica si producto es equipo de cómputo/IT')
    is_laptop = fields.Boolean(string = '¿Es laptop?', help = 'Verifica si es una laptop')
    is_cargador = fields.Boolean(string='¿Es cargador?', help = 'Verifica si es cargador')
    lab_task = fields.One2many(comodel_name='lab.task', inverse_name="product_id", string='Productos Programables')