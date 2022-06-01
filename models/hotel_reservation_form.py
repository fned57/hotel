from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError


class HotelReservationForm(models.Model):
    _name = 'hotel.reservation.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hotel Reservation form"

    name = fields.Char(string="Ten", default='Nháp')
    guest_id = fields.Many2one('hr.employee', 'Guest user')
    current_id = fields.Many2one('res.users', 'Current user', default=lambda self: self.env.user.id)
    date_of_issue = fields.Datetime(string="Date of issue", default=datetime.now())
    status = fields.Selection([
        ('0', 'Nháp'), ('1', 'Scheduled'),
        ('2', 'In Progress'),
        ('3', 'Completed'),
        ('4', 'Canceled')], string="Status", default='0', store=True,
        track_visibility=True)
    total_mature = fields.Integer(string="Total mature")
    total_children = fields.Integer(string="Total children")
    room_ids = fields.One2many('hotel.room.rental.detail', 'reservation_id', string="List rooms")
    service_detail_ids = fields.One2many('hotel.service.detail', 'reservation_id', string="Service")
    money = fields.Float(string="Money")
    total_money = fields.Float(string="Total money", compute='_compute_total_many')
    date = fields.Date(string="Date")
    sotiendatcoc = fields.Integer('Số tiền đặt cọc', default=0)
    date_readtime = fields.Datetime(string="Date")
    currency_id = fields.Many2one('res.currency')
    date_start = fields.Date(string='Start Date', help="Default start date for this Analytic Account.")
    date_stop = fields.Date(string='End Date', help="Default end date for this Analytic Account.")

    def huy_dat_phong(self):
        for rec in self:
            print((rec.date_of_issue - datetime.now()).total_seconds() / 60)
            if rec.status in ['1', '0'] and rec.sotiendatcoc == 0 and (
                    rec.date_of_issue - datetime.now()).total_seconds() / 60 < -50:
                rec.canceled()


    @api.depends('room_ids', 'service_detail_ids')
    def _compute_total_many(self):
        self.huy_dat_phong()
        self.date_readtime = datetime.today()
        for i in self:

            total_room = 0.0
            total_service = 0.0
            for record in i:
                for room in record.room_ids:
                    total_room += room.total
                for service in i.service_detail_ids:
                    total_service += service.amount
            i.total_money = total_room + total_service

    def getname(self):
        count = len(self.search([('status', '=', self.status)])) + 1
        if self.status == '1':
            self.name = 'I/' + str(count).zfill(3)
        elif self.status == '2':
            self.name = 'S/' + str(count).zfill(3)
        elif self.status == '3':
            self.name = 'D/' + str(count).zfill(3)
        else:
            self.name = 'C/' + str(count).zfill(3)

    def progress(self):
        self.status = '2'
        for room in self.room_ids:
            room.room_id.status = '3'
            room.status = '1'
        self.getname()


    def canceled(self):
        print('cancel')
        self.status = '4'
        self.getname()
        self.thanhtoan()

    def send_mail(self):
        template_id = self.env.ref('hotel.hotel_send_mail_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def _onchange_status_room(self):
        if self.status == '1':
            self.room_ids.room_id.status = '4'
        elif self.status == '2':
            self.room_ids.room_id.status = '3'
        else:
            self.room_ids.room_id.status = '2'

    def Scheduled(self):
        self.status = '1'
        for room in self.room_ids:
            room.room_id.status = '4'
            room.status = '3'
        self.getname()

    def thanhtoan(self):
        for room in self.room_ids:
            room.room_id.status = '2'
            room.status = '2'
