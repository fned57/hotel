from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError


class HotelReservationForm(models.Model):
    _name = 'hotel.reservation.form'
    _description = "Hotel Reservation form"
    _rec_name = 'guest_id'

    guest_id = fields.Many2one('hr.employee', 'Guest user')
    current_id = fields.Many2one('res.users', 'Current user', default=lambda self: self.env.user.id)
    date_of_issue = fields.Date(string="Date of issue", default=datetime.today())
    status = fields.Selection([('1', 'Scheduled'),
                               ('2', 'In Progress'),
                               ('3', 'Completed'),
                               ('4', 'Canceled')], string="Status", default="1")
    total_mature = fields.Integer(string="Total mature")
    total_children = fields.Integer(string="Total children")
    room_ids = fields.One2many('hotel.room.rental.detail', 'reservation_id', string="List rooms")
    service_detail_ids = fields.One2many('hotel.service.detail', 'reservation_id', string="Service")
    money = fields.Float(string="Money")
    total_money = fields.Float(string="Total money", compute='_compute_total_many')

    @api.depends('room_ids', 'service_detail_ids')
    def _compute_total_many(self):
        total_room = 0.0
        total_service = 0.0
        for record in self:
            for room in record.room_ids:
                total_room += room.total
            for service in self.service_detail_ids:
                total_service += service.amount
        self.total_money = total_room + total_service

    @api.model
    def create(self, value):
        if 'room_ids' in value:
            for room in value['room_ids']:
                self.env['hotel.room'].browse(room[2]['room_id']).status = '2'
        return super().create(value)

    def progress(self):
        self.status = '2'

    def canceled(self):
        self.status = '4'

    def write(self,value):
        if self.status == '3' or self.status == '4':
            raise ValidationError("No edit")
        else:
            return super().write(value)

    def send_mail(self):
        template_id = self.env.ref('hotel.hotel_send_mail_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)



