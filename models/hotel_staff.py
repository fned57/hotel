from odoo import  fields, models


class HotelStaff(models.Model):
    _name = 'hotel.staff'
    _description = "Hotel staff"
    _rec_name = 'user_id'
    position_id = fields.Many2one('hotel.position', string='Position')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user.id)

