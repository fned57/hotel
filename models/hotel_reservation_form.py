from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError


class HotelReservationForm(models.Model):
    _name = 'hotel.reservation.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hotel Reservation form"
    _rec_name = 'guest_id'

    guest_id = fields.Many2one('hr.employee', 'Guest user')
    current_id = fields.Many2one('res.users', 'Current user', default=lambda self: self.env.user.id)
    date_of_issue = fields.Datetime(string="Date of issue", default=datetime.now())
    status = fields.Selection([('1', 'Scheduled'),
                               ('2', 'In Progress'),
                               ('3', 'Completed'),
                               ('4', 'Canceled')], string="Status", default="1",track_visibility=True)
    total_mature = fields.Integer(string="Total mature")
    total_children = fields.Integer(string="Total children")
    room_ids = fields.One2many('hotel.room.rental.detail', 'reservation_id', string="List rooms")
    service_detail_ids = fields.One2many('hotel.service.detail', 'reservation_id', string="Service")
    money = fields.Float(string="Money")
    total_money = fields.Float(string="Total money", compute='_compute_total_many')
    date = fields.Date(string="Date")
    sotiendatcoc = fields.Integer('Số tiền đặt cọc',default=0)

    # @api.depends('date_of_issue', 'sotiendatcoc')
    # def _compute_status(self):
    #     for rec in self:
    #         if (rec.date_of_issue - datetime.today()).microseconds > 641575 and rec.status == '1' and rec.sotiendatcoc == 0:
    #             rec.status = '4'

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == '4':
            for i in self.room_ids:
                i.room_id.status = '2'


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

    def progress(self):
        self.status = '2'
        for i in self.room_ids:
            i.room_id.status = "3"

    def canceled(self):
        self.status = '4'

    def write(self, value):
        if self.status == '3' or self.status == '4':
            raise ValidationError("No edit")
        else:
            return super().write(value)

    def send_mail(self):
        template_id = self.env.ref('hotel.hotel_send_mail_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def _onchange_status(self):
        res_model_id = self.env['ir.model'].search([('model', '=', 'hotel.reservation.form')]).id

        activity = {
            'summary': 'Test',
            'activity_type_id': self.env.ref('hotel.mail_activity_booking_service').id,
            'res_id': self.id.origin,
            'res_model_id': res_model_id,
            'user_id': self.env.user.id,
        }
        self.env['mail.activity'].sudo().create(activity)