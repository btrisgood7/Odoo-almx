# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.tools.misc import format_datetime
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import date
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    not_validate = fields.Boolean(string='No se puede validar', help='Muestra si la condición de pagado aplica para la orden de venta relacionada al movimiento de almacén actual')#, compute='compute_spare_sale_order')
    detect_move_type = fields.Boolean(string='Tipo de movimiento')#, compute='compute_picking_type_move')
    pick_move = fields.Boolean(string='Es un PICK')
    out_move = fields.Boolean(string='Es un OUT')
    in_move = fields.Boolean(string='Es un IN')
    delivery_date = fields.Date(string='Fecha de entrega por contrato', tracking = True)
    delivery_date_material = fields.Date(string='Fecha de entrega por llegada de material', tracking = True)

    @api.depends('picking_type_id.sequence_code')
    def compute_picking_type_move(self):
        for rec in self:
            sequence_code = rec.picking_type_id.sequence_code
            move_flags = {
                'PICK': 'pick_move',#Cambiar en producción a NWH/PICK/
                'OUT': 'out_move',#Cambiar en producción a NWH/OUT/
                'IN': 'in_move',#Cambiar en producción a NWH/IN/
            }

            rec.pick_move = rec.out_move = rec.in_move = False

            move_attr = move_flags.get(sequence_code)
            if move_attr:
                setattr(rec, move_attr, True)
                rec.detect_move_type = True
            else:
                rec.detect_move_type = False

    def compute_spare_sale_order(self):
        op_type = self.picking_type_id.id
        sale_type = self.x_studio_tipo_de_venta
        comp_paid = self.x_studio_completamente_pagado
        if sale_type == 'spare' and comp_paid != True and op_type == 2: #Aplica solo para movimientos que son OUT
            self.not_validate = True
        else:
            self.not_validate = False

    def action_set_to_draft(self):
        if self.state not in ('draft', 'done'):
            self.action_clear_quantities_to_zero()
            self.do_unreserve()
            move = self.env['stock.move'].search([('picking_id', '=', self.id)])
            for each in move:
                each.state = 'draft'
            self.state = 'draft'

    def action_create_related_out(self):
        self.ensure_one()
        if self.state == 'assigned':
            # Encuentra el tipo de operación "Delivery Orders"
            picking_type_out = self.env['stock.picking.type'].search([('code', '=', 'outgoing'),('warehouse_id', '=', self.picking_type_id.warehouse_id.id)], limit=1)
            picking_vals = {
                'partner_id': self.partner_id.id,
                'picking_type_id': picking_type_out.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'origin': self.origin,
                'move_type': self.move_type,
                'company_id': self.company_id.id,
            }

            picking_out = self.env['stock.picking'].create(picking_vals)
            # Crear los movimientos
            for move in self.move_ids_without_package:
                self.env['stock.move'].create({
                    'name': move.name,
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.product_uom_qty,
                    'product_uom': move.product_uom.id,
                    'picking_id': picking_out.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': picking_out.location_dest_id.id,
                    'company_id': self.company_id.id,
                })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Salida Generada',
                'res_model': 'stock.picking',
                'res_id': picking_out.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_create_related_int(self):
        self.ensure_one()
        if self.state == 'done':
            # Encuentra el tipo de operación "Delivery Orders"
            picking_type_out = self.env['stock.picking.type'].search([('code', '=', 'internal'), ('warehouse_id', '=', self.picking_type_id.warehouse_id.id)], limit=1)
            picking_vals = {
                'partner_id': self.partner_id.id,
                'picking_type_id': picking_type_out.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'origin': self.origin,
                'move_type': self.move_type,
                'company_id': self.company_id.id,
            }

            picking_out = self.env['stock.picking'].create(picking_vals)
            # Crear los movimientos
            for move in self.move_ids_without_package:
                self.env['stock.move'].create({
                    'name': move.name,
                    'product_id': move.product_id.id,
                    'product_uom_qty': move.product_uom_qty,
                    'product_uom': move.product_uom.id,
                    'picking_id': picking_out.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': picking_out.location_dest_id.id,
                    'company_id': self.company_id.id,
                })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Transferencia Generada',
                'res_model': 'stock.picking',
                'res_id': picking_out.id,
                'view_mode': 'form',
                'target': 'current',
            }
#Acción de cancelación de un movimiento
    def action_cancel(self):
        res = super().action_cancel()

        mt_note = self.env.ref('mail.mt_note')  # Nota interna, NO dispara emails
        todo_type = self.env.ref('mail.mail_activity_data_todo')

        for picking in self:
            # --- (Opcional) Filtrar por prefijo de secuencia ---
            #No es necesario ya que para eso es la acción automatica, pero por si falla no esta mal tenerlo.
            # if picking.picking_type_id.sequence_code and not picking.picking_type_id.sequence_code.startswith(('OUT', 'PICK')):
            #     continue

            # Fecha/hora local del usuario que cancela
            tz = self.env.context.get('tz') or self.env.user.tz or 'UTC'
            ts_local = format_datetime(self.env, fields.Datetime.now(), tz=tz)

            # 1) Nota en el chatter SIN correos (subtype=mt_note)
            picking.with_context(
                mail_post_autofollow=False,
                mail_create_nosubscribe=True,
                mail_notify_force_send=False,
            ).message_post(
                body=_("⚠️ Este movimiento fue <b>cancelado</b> por <b>%s</b> el <b>%s</b>.")
                     % (self.env.user.display_name, ts_local),
                message_type='comment',
                subtype_id=mt_note.id,
            )

            # 2) Actividades para seguidores internos (excluye cliente y autor)
            follower_partners = picking.message_follower_ids.mapped('partner_id')
            blocked_ids = set()
            if picking.partner_id:
                blocked_ids.add(picking.partner_id.commercial_partner_id.id)  # cliente/proveedor
            blocked_ids.add(self.env.user.partner_id.id)  # quien cancela

            internal_users = (
                follower_partners
                .filtered(lambda p: p.id not in blocked_ids)
                .mapped('user_ids')
                .filtered(lambda u: u.has_group('base.group_user'))
            )

            for user in set(internal_users):
                picking.activity_schedule(
                    activity_type_id=todo_type.id,
                    user_id=user.id,
                    summary=_("Movimiento cancelado"),
                    note=_("El movimiento %s fue cancelado por %s el %s.")
                         % (picking.name, self.env.user.display_name, ts_local),
                    date_deadline=fields.Date.context_today(self),
                )

        return res