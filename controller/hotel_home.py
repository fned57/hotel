from odoo import http, _
from odoo.http import request


class HomeController(http.Controller):

    @http.route('/', website=True, auth='public', methods=['GET'])
    def index(self, **kwargs):
        rooms = request.env['hotel.room'].sudo().search([])
        rooomss = request.env['hotel.room'].sudo().search([], limit=3)
        rooms_empty = rooms.filtered(lambda x: x.status == '2')
        rooms_buys = rooms.filtered(lambda x: x.status == '3')
        employee = request.env['hr.employee'].sudo().search([])
        serivers = request.env['hotel.service'].sudo().search([])
        foods = serivers.filtered(lambda x: x.type == 'food')
        seriver = serivers.filtered(lambda x: x.type == 'server')
        room_type = request.env['hotel.room.type'].sudo().search([])

        return request.render('hotel.hotel_home', {'count_rooms': len(rooms),
                                                   'count_rooms_empty': len(rooms_empty),
                                                   'count_rooms_buys': len(rooms_buys),
                                                   'employee': len(employee),
                                                   'rooms': rooomss,
                                                   'foods': foods,
                                                   'seriver': seriver,
                                                   'room_type_ids': room_type
                                                   })

    # @http.route('./rooms', website=True, auth='public', methods=['GET'])
    # def rooms(self, **kwargs):
    #     rooms = request.env['hotel.room'].sudo().search([])
    #     return request.render('hotel.hotel_room', {'rooms': rooms})
