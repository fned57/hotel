from docutils.nodes import status
from odoo import http, _
from odoo.http import request


class BookingController(http.Controller):

    @http.route('/booking', website=True, auth='public', methods=['GET'])
    def index(self, **kwargs):
        room_type = request.env['hotel.room.type'].sudo().search([])
        return request.render('hotel.booking', {'room_type_ids': room_type})

    @http.route('/bookings', website=True, csrf=False, auth='public', methods=['POST'])
    def post_booking(self, **kwargs):
        rooms = []
        status = ''
        timphong = True
        for i in kwargs:
            try:
                i = int(i)
                rooms = request.env['hotel.room'].sudo().search([('room_type_id.id', '=', str(i)), ('status','=', '2')])
                if int(kwargs[str(i)]) > len(rooms):
                    status = 'không đủ số lượng phòng ' + rooms[0].room_type_id.name
                    timphong = False
                    break
                room = request.env['hotel.room'].sudo().search([('room_type_id.id', '=', str(i)), ('status', '=', '2')],
                                                               limit=int(kwargs[str(i)]))
                rooms.append(room)
            except:
                continue
        employee = request.env['hr.employee'].sudo().search([('name', '=', kwargs['your_name'])])
        if len(employee) < 1:
            employee = request.env['hr.employee'].sudo().create({'name': kwargs['your_name'],
                                                                 'mobile_phone': kwargs['Phone Number'],
                                                                 })
        if timphong:
            value = {
                "guest_id": employee.id,
                'total_mature': kwargs['count_cha'],
                'total_children': kwargs['count_children'],
            }
            booking = request.env['hotel.reservation.form'].sudo().create(value)
            for i in rooms:
                for j in i:
                    request.env['hotel.room.rental.detail'].sudo().create({
                        'reservation_id': booking.id,
                        'arrival_date': kwargs['Date in'],
                        'departure_date': kwargs['date out'],
                        'room_id': j.id
                })
            status = 'Đặt phòng thành công'
            return request.render('hotel.detail_booking', {'booking': booking,
                                                       'status': status,
                                                       'huy': 'huy/' + str(booking.id),
                                                       'name': kwargs['your_name'],
                                                       'mobile_phone': kwargs['Phone Number'],
                                                       },
                              )
        else:
            return request.render('hotel.detail_booking', {
                                                           'status': status,
                                                           'name': kwargs['your_name'],
                                                           'mobile_phone': kwargs['Phone Number'],
                                                           },
                                  )

    @http.route('/bookings_list', website=True, auth='public', methods=['GET'])
    def rooms(self, **kwargs):
        booking_list = request.env['hotel.reservation.form'].sudo().search(
            [('guest_id.user_id.id', '=', request.env.user.id)])
        return request.render('hotel.hotel_room', {'list_booking': booking_list})

    @http.route('/huy/<int:id>', website=True, auth='public', methods=['GET'])
    def huy(self, **kwargs):
        request.env['hotel.reservation.form'].sudo().browse(kwargs['id']).status = '4'
        rooms = request.env['hotel.room'].sudo().search([])
        return request.render('hotel.hotel_room', {'rooms': rooms})
