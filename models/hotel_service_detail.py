from odoo import  fields, models, api


class HotelServiceDetail(models.Model):
    _name = 'hotel.service.detail'
    _description = "Hotel Service detail"
    _rec_name = 'service_id'

    service_id = fields.Many2one('hotel.service', string="Service")
    number_of_uses = fields.Integer(string=" Number of Uses", default="0")
    amount = fields.Float(string="Amount")
    note = fields.Text(string="Node")
    reservation_id = fields.Many2one('hotel.reservation.form')

    @api.onchange("number_of_uses")
    def onchange_number_of_uses(self):
        self.amount = self.number_of_uses * self.service_id.price
