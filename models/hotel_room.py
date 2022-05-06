from email.policy import default

from odoo import  fields, models, api


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _inherit = ['mail.thread']
    _description = "Hotel Rooms"

    name = fields.Char(string="Name room")
    status = fields.Selection([('1', 'Empty'), ('2', 'Busy')], 'Status', default='2')
    description = fields.Text(string="Description Room")
    avatar = fields.Binary(string="Image Avatar")
    room_type_id = fields.Many2one('hotel.room.type', string="Room type")
    reservation_form_ids = fields.Many2many('hotel.reservation.form')
    evaluate_ids = fields.One2many('mail.message', string="Messages", store=False)
    price = fields.Float(string="Price Room", digits=(12, 0), related='room_type_id.price')
    price_hour = fields.Float(string="Price Hour", digits=(12, 0), related='room_type_id.price_hour')
    price_overnight = fields.Float(string="Price over night", digits=(12, 0), related='room_type_id.price_overnight')
    currency_id = fields.Many2one('res.currency', 'currency', compute='_compute_currency')

    def _compute_currency(self):
        self.currency_id = self.env.company.currency_id


    def test(self):
        print(1)


    def test1(self):
        print(2)

