import json

import werkzeug.wrappers
from odoo import http, _
from odoo.http import request


class RoomsController(http.Controller):

    @http.route('/rooms', type='http', auth='public', methods=['GET'])
    def index(self, **kwargs):
        domain = []
        for i in kwargs:
            domain.append((i, '=', kwargs[i]))
        try:
            print(domain)
            rooms = request.env['hotel.room'].sudo().search(domain)
            room = []
            for r in rooms:
                ro = {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "room_type_id": r.room_type_id.id,
                    "status": r.status,
                    # "imager": r.avatar
                }
                room.append(ro)
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json;charset=utf-8',
                response=json.dumps(
                    {
                        "rooms": room
                    }
                ),
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

    # @http.route('/rooms', type='json', auth='public', methods=['POST'])
    # def create(self, **rec):
    #     room = request.jsonrequest
    #     new_room = request.env['hotel.room'].sudo().create(room)
    #
    #     ro = {
    #         "id": new_room.id,
    #         "name": new_room.name,
    #         "description": new_room.description,
    #         "room_type_id": new_room.room_type_id.id,
    #         "status": new_room.status,
    #         # "imager": r.avatar
    #     }
    #
    #     return werkzeug.wrappers.Response(
    #         status=200,
    #         content_type='application/json;charset=utf-8',
    #         response={
    #             "room": ro,
    #         },
    #     )
    #
    # @http.route('/rooms/avatar/<int:id>', type='http', auth='public', methods=['PUT'], csrf=False)
    # def update_avatar(self, **rec):
    #     room = {
    #         'avatar': request.httprequest.data
    #     }
    #     new_room = request.env['hotel.room'].sudo().browse(rec['id']).write(room)
    #
    #     return werkzeug.wrappers.Response(
    #         status=200,
    #         content_type='application/json;charset=utf-8',
    #         response={
    #                 "status": "create done",
    #             }
    #         ),
    #
    # @http.route('/rooms/<int:id>', type='json', auth='public', methods=['PUT'], csrf=False)
    # def update(self, **rec):
    #     req = request.jsonrequest
    #     status = request.env['hotel.room'].sudo().browse(rec['id']).write(req)
    #
    #     if status:
    #         room = request.env['hotel.room'].sudo().browse(rec['id'])
    #         return {
    #             "id": room.id,
    #             "name": room.name,
    #             "description": room.description,
    #             "room_type_id": room.room_type_id.id,
    #             "status": room.status,
    #         }
    #     else:
    #         return False
    #
    # @http.route('/rooms/<int:id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    # def delete_room(self, **rec):
    #     rul = request.env['hotel.room'].sudo().browse(rec['id']).unlink()
    #     return werkzeug.wrappers.Response(
    #         status=200,
    #         content_type='application/json;charset=utf-8',
    #         response=json.dumps(
    #             {
    #                 "jsonrpc": "2.0",
    #                 "result": "123",
    #             }
    #         ),
    #     )
