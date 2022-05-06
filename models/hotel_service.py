from odoo import  fields, models


class HotelService(models.Model):
    _name = 'hotel.service'
    _description = "Hotel Service"

    name = fields.Char(string="Name service")
    price = fields.Float(string="Price")
    description = fields.Text(string="Description")