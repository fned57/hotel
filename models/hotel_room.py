from odoo import fields, models, api


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hotel Rooms"

    name = fields.Char(string="Name room")
    status = fields.Selection([('1', 'Plan'), ('2', 'Empty'), ('3', 'Busy'), ('4', 'Lên kế hoạch')], 'Status', default='1', store=True)
    description = fields.Text(string="Description Room")
    avatar = fields.Binary(string="Image Avatar")
    room_type_id = fields.Many2one('hotel.room.type', string="Room type")
    reservation_form_ids = fields.Many2many('hotel.reservation.form')
    evaluate_ids = fields.One2many('mail.message', string="Messages", store=False)
    price = fields.Float(string="Price Room", digits=(12, 0), related='room_type_id.price')
    price_hour = fields.Float(string="Price Hour", digits=(12, 0), related='room_type_id.price_hour')
    price_overnight = fields.Float(string="Price over night", digits=(12, 0), related='room_type_id.price_overnight')
    currency_id = fields.Many2one('res.currency', related='room_type_id.currency_id')
    date_start = fields.Date(string='Start Date', help="Default start date for this Analytic Account.")
    date_stop = fields.Date(string='Stop Date', help="Default start date for this Analytic Account.")

    def name_get(self):
        return [(rec.id, '[ ' + rec.room_type_id.name + ' ] ' + rec.name) for rec in self]

    def _compute_currency(self):
        self.currency_id = self.env.company.currency_id

    def button_ready(self):
        self.status = '2'

    # @api.depends('reservation_form_ids.status')
    # def _compute_status(self):
    #     for rec in self:
    #         if rec.reservation_form_ids.status == '1':
    #             rec.status = '4'
    #         elif rec.reservation_form_ids.status == '2':
    #             rec.status = '3'
    #         else:
    #             rec.status = '2'
