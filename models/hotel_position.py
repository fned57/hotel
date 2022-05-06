from odoo import  fields, models


class HotelPosition(models.Model):
    _name = 'hotel.position'
    _description = "Hotel position"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description title")
