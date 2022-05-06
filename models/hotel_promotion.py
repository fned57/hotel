from odoo import  fields, models, api
from datetime import date


class HotelPromotion(models.Model):
    _name = 'hotel.promotion'
    _description = "Hotel promotion"

    name = fields.Char(string="Name", required=True)
    short_description = fields.Text(string="Short description")
    subject = fields.Char(string="Subject")
    compute_price = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('percentage', 'Discount')
    ], index=True, default='fixed', required=True)
    image = fields.Binary(string="Image promotion")
    starting_date = fields.Date(string="start date", default=date.today(), required=True)
    discount = fields.Float(string="Discount")
    ending_date = fields.Date(string="End Date", default=date.today(), required=True)
    room_type_ids = fields.Many2many('hotel.room.type', string="Room type")
    status = fields.Selection([('1', 'Activated'), ('2', 'No Activated'), ('3', 'Out of day')],
                              'Status', default='2',
                              compute='_compute_status')
    fixed_price = fields.Float(string="Fixed Price")

    @api.depends('starting_date', 'ending_date')
    def _compute_status(self):
        if (date.today() - self.starting_date).days < 0:
            self.status = '2'
        elif (date.today() - self.ending_date).days > 0:
            self.status = '3'
        else:
            self.status = '1'

