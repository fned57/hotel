from odoo import  fields, models, api


class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = "Hotel Rooms Type"

    name = fields.Char(string="Room type")
    description = fields.Text("Description room type")
    price = fields.Float(string="Price Room", digits=(12, 0))
    price_hour = fields.Float(string="Price Hour", digits=(12, 0))
    price_overnight = fields.Float(string="Price over night", digits=(12, 0))
    room_ids = fields.One2many('hotel.room', 'room_type_id', string="Rooms")
    currency_id = fields.Many2one('res.currency', 'currency')

    def test(self):
        print(1)
        print(2)