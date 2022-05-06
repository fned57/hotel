import json

import werkzeug.wrappers
from odoo import http, _
from odoo.http import request


class ReservationController(http.Controller):

    @http.route('/reservations', type='http', auth='public', methods=['GET'])
    def index(self, **kwargs):
        domain = []
        for i in kwargs:
            domain.append((i, '=', kwargs[i]))
        try:
            reservations = request.env['hotel.reservation.form'].search(domain)
            list_reservations = []
            for i in reservations:
                rooms = []
                for j in i.room_ids:
                    room = {
                        'id': j.room_id.id,
                        'name': j.room_id.name,
                        'price': j.room_id.price
                    }
                    rooms.append(room)
                reservation = {
                    'id': i.id,
                    'date_of_issue': str(i.date_of_issue),
                    'status': i.status,
                    'total_mature': i.total_mature,
                    'total_children': i.total_children,
                    'room_ids': rooms,
                    # # 'service_detail_ids': i.room_type_id.id,
                    'money': i.money,
                    'total_money': i.total_money,
                }
                list_reservations.append(reservation)
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json;charset=utf-8',
                response=json.dumps({
                    'list_reservations': list_reservations,
                }),
            )
        except ValueError:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json;charset=utf-8',
                response=json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "result": {
                            'message': "ValueError"
                        },
                    }
                ),
            )

    @http.route('/reservations', type='json', auth='public', methods=['POST'])
    def create(self, **rec):
        room = request.jsonrequest
        room["status"] = False
        new_room = request.env['hotel.reservation.form'].sudo().create(room)
        return {
            'id': new_room.id,
            'date_of_issue': str(new_room.date_of_issue),
            'status': new_room.status,
            'total_mature': new_room.total_mature,
            'total_children': new_room.total_children,
            'money': new_room.money,
            'total_money': new_room.total_money,

        }

    @http.route('/reservations/<int:id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update(self, **rec):
        reservation = request.jsonrequest
        new_reservation = request.env['hotel.reservation.form'].sudo().browse(rec['id']).write(reservation)
        if new_reservation:
            return {
                "message": "True",
            }
        else:
            return {
                "message": "False",
            }

    @http.route('/reservations/<int:id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete(self, **rec):
        new_reservation = request.env['hotel.reservation.form'].sudo().browse(rec['id']).unlink()
        if new_reservation:
            return {
                "message": "True",
            }
        else:
            return {
                "message": "False",
            }
