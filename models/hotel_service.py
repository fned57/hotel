from odoo import fields, models


class HotelService(models.Model):
    _name = 'hotel.service'
    _description = "Hotel Service"

    name = fields.Char(string="Name service", required=True)
    price = fields.Float(string="Price", required=True)
    description = fields.Text(string="Description")
    avatar = fields.Binary(string="Avatar")
    type = fields.Selection([('food', 'Food'),
                             ('server', 'Server')], required=True
                            )
