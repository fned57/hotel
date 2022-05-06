from odoo import  fields, models, api


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _inherit = 'mail.thread'
    _description = "Hotel Rooms"

    name = fields.Char(string="Name room")
    status = fields.Selection([('1', 'Empty'), ('2', 'Busy')], 'Status', default='2')
    description = fields.Text(string="Description Room")
    avatar = fields.Binary(string="Image Avatar")
    room_type_id = fields.Many2one('hotel.room.type', string="Room type")
    reservation_form_ids = fields.Many2many('hotel.reservation.form')
    # evaluate_ids = fields.One2many('hotel.evaluate', 'room_id', string="Evaluate", readonly=False)
    evaluate_ids = fields.One2many('mail.message', string="Messages", store=False)
    price = fields.Float(string="Price", related='room_type_id.price')



