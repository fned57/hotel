from odoo import  fields, models
from datetime import datetime

class HotelEvaluate(models.Model):
    _name = 'hotel.evaluate'
    _description = "Hotel evaluate"

    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user.id,readonly=True)
    subject = fields.Char(string="Subject")
    date_sent = fields.Date(string="Data sent", default=datetime.today(), readonly=True)
    room_id = fields.Many2one('hotel.room', string="Room")
