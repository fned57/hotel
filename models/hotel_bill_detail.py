from odoo import  fields, models, api

from datetime import datetime
class HotelBill(models.Model):
    _name = 'hotel.bill.detail'
    _description = "Hotel bill detail"

    data_of_issue = fields.Date(string="Data of issue",default=datetime.today())
    mode_of_payment = fields.Selection([('1', 'Cash'),('2','Online Pay')], string="Mode of  payment", default="1")
    user_time = fields.Integer(string="User time",readonly=False, compute='_compute_user_time')
    total_many = fields.Float(string="Total many",compute='_compute_total_many')
    staff_id = fields.Many2one('hotel.staff', string="Create by")
    reservation_form_id = fields.Many2one('hotel.reservation.form', string="Reservation form")
    promotion_ids = fields.Many2many('hotel.promotion', string="Promotions")
    many = fields.Float(string="Many", compute='_compute_many')

    @api.depends('reservation_form_id', 'promotion_ids', 'user_time')
    def _compute_many(self):
        self.many = self.total_many
        for record in self.promotion_ids:
            self.many = ((100-record.discount)/100)*self.many

    @api.depends('reservation_form_id')
    def _compute_user_time(self):
        self.user_time = (self.reservation_form_id.departure_date - self.reservation_form_id.arrival_date).days

    @api.depends('user_time')
    def _compute_total_many(self):
        self.total_many = self.user_time * self.reservation_form_id.total_many






