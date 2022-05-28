from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError


class HotelRoomRentalDetail(models.Model):
    _name = 'hotel.room.rental.detail'
    _description = "Hotel room rental detail"

    status = fields.Selection([
        ('1', "Đang sử dụng"),
        ('2', 'Thanh toán')], default='1')
    compute_rent = fields.Selection([
        ('date', 'Date'),
        ('hour', 'Hour'),
        ('overnight', 'Overnight')], index=True, default='date', required=True)
    room_id = fields.Many2one('hotel.room', string='Room', required=True)
    arrival_date = fields.Date(string="Arrival Date", default=date.today(), required=True)
    departure_date = fields.Date(string="Departure Date", default=date.today(), required=True)
    promotion_ids = fields.Many2many('hotel.promotion', string="Promotions")
    total = fields.Float(string="Total money", compute='_compute_total', store=True)
    reservation_id = fields.Many2one('hotel.reservation.form')
    time_start = fields.Datetime('Time start', default=lambda self: fields.Datetime.now())
    time_end = fields.Datetime('Time end', default=lambda self: fields.Datetime.now())
    so_tien_da_thanh_toan = fields.Integer('Số tiền thanh toán')

    @api.onchange('time_start','time_end')
    def _onchange_time_start(self):
        self.arrival_date = self.time_start
        self.departure_date = self.time_end

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
        for i in self:
            money = 0
            if i.compute_rent == 'date':
                day_uses = (i.departure_date - i.arrival_date).days
                money = i.room_id.price * int(day_uses)
            elif i.compute_rent == 'hour':
                money = (i.time_end - i.time_start).total_seconds() / 60 / 60 * i.room_id.room_type_id.price_hour
            else:
                money = i.room_id.room_type_id.price_overnight

            for record in i.promotion_ids:
                if record.compute_price == "fixed":
                    if money != 0:
                        record.discount = record.fixed_price / money * 100

                money = ((100 - record.discount) / 100) * money
            i.total = money

    @api.onchange('room_id')
    def _onchange_room_id(self):
        if self.room_id.room_type_id:
            domain = [
                ('starting_date', '<=', date.today()),
                ('ending_date', '>=', date.today()),
                ('room_type_ids.id', '=', self.room_id.room_type_id.id)
            ]
            self.promotion_ids = self.env['hotel.promotion'].search(domain)

    @api.constrains('room_id')
    def statusroom(self):
        for i in self:
            i.room_id.status = '3'

    def chuyenphong(self):
        pass

    @api.onchange('so_tien_da_thanh_toan')
    def _onchange_so_tien_da_thanh_toan(self):
        self.total -= self.so_tien_da_thanh_toan

    def pay(self):
        self.status = '2'