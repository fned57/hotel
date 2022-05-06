import json

import werkzeug.wrappers
from odoo import http, _
from odoo.http import request


class ServiceDetailController(http.Controller):

    @http.route('/servicing/<int:id>', type='http', auth='public', methods=['GET'])
    def index(self, **kwargs):
        domain = [
            ('reservation_id', '=', kwargs['id'])
        ]
        services = request.env['hotel.service.detail'].sudo().search(domain)
        service = []
        for r in services:
            service.append({
                "id": r.id,
                "service_id": r.service_id.id,
                "number_of_uses": str(r.number_of_uses),
                "amount": str(r.amount),
                "note": r.note,
            })
        return werkzeug.wrappers.Response(
            status=200,
            content_type='application/json;charset=utf-8',
            response=json.dumps({
                "rooms": service
                }
            )
        )

    @http.route('/booking/<int:id>', type='json', auth='public', methods=['POST'])
    def create(self, **rec):
        room_detail = request.jsonrequest
        room_detail['reservation_id'] = rec['id']
        new_room_detail = request.env['hotel.room.rental.detail'].sudo().create(room_detail)
        return {
            'room_id': new_room_detail.room_id.id
        }

    @http.route('/booking/<int:id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_avatar(self, **rec):
        room_detail = request.jsonrequest
        room_detail['reservation_id'] = rec['id']
        new_room_detail = request.env['hotel.room.rental.detail'].sudo().create(room_detail)
        return new_room_detail

    @http.route('/booking/<int:id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update(self, **rec):
        req = request.jsonrequest
        status = request.env['hotel.room'].sudo().browse(rec['id']).write(req)
        return status

    @http.route('/booking/<int:id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_room(self, **rec):
        rul = request.env['hotel.room'].sudo().browse(rec['id']).unlink()
        return rul
