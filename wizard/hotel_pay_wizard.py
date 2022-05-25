# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HotelPayWizard(models.TransientModel):
    _name = 'hotel.pay.wizard'
    _description = 'Create new pay'

    reservation_id = fields.Many2one('hotel.reservation.form', string="Reservation", readonly=True)
    total_money = fields.Float(related='reservation_id.total_money', string="Total money")
    cash = fields.Float(string="Cash")
    excess_cash = fields.Float(string='excess cash', compute='_compute_excess_cash')

    @api.depends('cash')
    def _compute_excess_cash(self):
        self.excess_cash = self.total_money - self.cash

    def pay(self):
        self.reservation_id.status = '3'
        for room in self.reservation_id.room_ids:
            room.room_id.status = '2'


