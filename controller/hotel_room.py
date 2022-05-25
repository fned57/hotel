from odoo import http, _
from odoo.http import request


class RoomsController(http.Controller):

    @http.route('/rooms', website=True, auth='public', methods=['GET'])
    def index(self, **kwargs):
        rooms = request.env['hotel.room'].sudo().search([])
        return request.render('hotel.hotel_room', {'rooms': rooms})
