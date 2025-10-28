from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order' #Herencia del módelo de ventas

    is_related = fields.Boolean(string='Obtener el tipo de movimiento', compute='relational_moves', default=False)

    def relational_moves(self):
        if not self.procurement_group_id:
            self.is_related = False
            return
        pickings = self.env['stock.picking'].search([('group_id', '=', self.procurement_group_id.id)])
        auto_picks = pickings.filtered(lambda p: p.picking_type_id.sequence_code == 'PICK') #Cambiar en producción a NWH/PICK/
        auto_outs = pickings.filtered(lambda p: p.picking_type_id.sequence_code == 'OUT')   #Cambiar en producción a NWH/OUT/
        # Solo tomamos los primeros de cada tipo para la relación automática
        if auto_picks and auto_outs:
            pick = auto_picks[0]
            out = auto_outs[0]

            pick.related_out_id = out.id
            out.related_pick_id = pick.id

            self.is_related = True
        else:
            self.is_related = False


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_out_id = fields.Many2one('stock.picking', string='OUT relacionada', help='Muestra el movimiento relacionado', domain=[["picking_type_id.sequence_code","=","OUT"]], tracking = True)
    related_pick_id = fields.Many2one('stock.picking', string='PICK relacionado', help='Muestra el movimiento relacionado', domain=[["picking_type_id.sequence_code","=","PICK"]], tracking = True)
    #picking_id = fields.Many2many('stock.picking',string='OUT Complemento', help='Muestra los OUT complemento', domain=[["picking_type_id.sequence_code","=","OUT"]], index=True)
    #x_studio_sale_type = fields.Boolean(string='Tipo de venta')
    #x_studio_completamente_pagado = fields.Boolean(string='Totalmente pagado')