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
    sophongtrong = fields.Integer(compute='_sophongtrong')
    sophongban = fields.Integer(compute='_sophongban')
    sophongsuachua = fields.Integer(compute='_sophongdangsua')

    @api.depends('room_ids')
    def _sophongtrong(self):
        for i in self:
            i.sophongtrong = len(self.env['hotel.room'].search([('status', '=', '2'), ('room_type_id.id', '=', i.id)]))

    @api.depends('room_ids')
    def _sophongban(self):
        for i in self:
            i.sophongban =  len(self.env['hotel.room'].search([('status', '=', '3'), ('room_type_id.id', '=', i.id)]))

    @api.depends('room_ids')
    def _sophongdangsua(self):
        for i in self:
            i.sophongsuachua = len(self.env['hotel.room'].search([('status', '=', '1'), ('room_type_id.id', '=', i.id)]))
