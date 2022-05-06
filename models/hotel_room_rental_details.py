from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class HotelRoomRentalDetail(models.Model):
    _name = 'hotel.room.rental.detail'
    _description = "Hotel room rental detail"

    compute_rent = fields.Selection([
        ('date', 'Date'),
        ('hour', 'Hour'),
        ('overnight', 'Overnight')], index=True, default='date', required=True)
    room_id = fields.Many2one('hotel.room', string='Room', required=True)
    arrival_date = fields.Date(string="Arrival Date", default=date.today(), required=True)
    departure_date = fields.Date(string="Departure Date", default=date.today(), required=True)
    promotion_ids = fields.Many2many('hotel.promotion', string="Promotions")
    total = fields.Float(string="Total money", compute='_compute_total')
    reservation_id = fields.Many2one('hotel.reservation.form')
    time_start = fields.Datetime('Time start', default=lambda self: fields.Datetime.now())
    time_end = fields.Datetime('Time end', default=lambda self: fields.Datetime.now())

    @api.constrains('arrival_date')
    def _onchange_arrival_date(self):
        if (self.arrival_date - date.today()).days >= 0:
            raise ValidationError("arrival date > " + str(date.today()))

    @api.onchange('departure_date')
    def _onchange_arrival_date(self):
        if (self.departure_date - date.today()).days < 0:
            raise ValidationError("departure date < " + str(date.today()))

    @api.depends('promotion_ids', 'arrival_date', 'departure_date', 'compute_rent', 'time_start', 'time_end')
    def _compute_total(self):
        money = 0
        if self.compute_rent == 'date':
            day_uses = (self.departure_date - self.arrival_date).days
            money = self.room_id.price * int(day_uses)
        elif self.compute_rent == 'hour':
            money = (self.time_end - self.time_start).total_seconds() / 60 / 60 * self.room_id.room_type_id.price_hour
        else:
            money = self.room_id.room_type_id.price_overnight

        for record in self.promotion_ids:
            if record.compute_price == "fixed":
                if money != 0:
                    record.discount = record.fixed_price / money * 100

            money = ((100 - record.discount) / 100) * money
        self.total = money

    @api.onchange('room_id')
    def _onchange_room_id(self):
        if self.room_id.room_type_id:
            domain = [
                ('starting_date', '<=', date.today()),
                ('ending_date', '>=', date.today()),
                ('room_type_ids.id', '=', self.room_id.room_type_id.id)
            ]
            self.promotion_ids = self.env['hotel.promotion'].search(domain)

    def write(self, value):
        if 'room_id' in value:
            for room in self.room_ids:
                room.room_id.status = '2'
        return super().write(value)
