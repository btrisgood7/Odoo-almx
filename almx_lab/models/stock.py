from odoo import models, fields, api
import time
import datetime

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lab_task = fields.One2many(comodel_name='lab.task', inverse_name="picking_id", string='Productos Programables')
    use_products = fields.Boolean(string='Obtener productos', compute='get_programable_product', store = False)
    out_move = fields.Boolean(store = True)

    @api.depends('out_move')
    def get_programable_product(self):
        for picking in self:
            picking.use_products = False  # Valor por defecto
            if picking.out_move:
                stock_ids = self.env['stock.move'].search([('picking_id', '=', picking.id)])
                existing_products = self.env['lab.task'].search([('picking_id', '=', picking.id)]).mapped('product_id.id')
                sale_order = picking.sale_id
                for move in stock_ids:
                    qty = move.product_uom_qty
                    is_program = move.product_id.verification_lab
                    prod_id = move.product_id.id
                    if is_program:
                        for _ in range(int(qty)):
                            if prod_id not in existing_products:
                                self.env['lab.task'].create({
                                    'product_id': prod_id,
                                    'picking_id': picking.id,
                                    'program_product': sale_order.program_product if sale_order else '',})
                                picking.use_products = True
                                print("El registro fue creado exitosamente")
                            else:
                                print("El registro ya existe en la tabla lab task")
                    else:
                        print('No hay productos programables')
            else:
                print("No es un out")
