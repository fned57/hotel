# -*- coding: utf-8 -*-
{
    "name": "Hotel",
    'summary': """Hotel manger""",
    'description': """""",
    'author': "Trần Đăng Tuấn",
    'website': "https://fb.com/tdthc",
    'version': '14.0.1.0.1',
    'depends': [
        'mail',
        'hr'
    ],
    'data': [
        'views/hotel.xml',
        'security/hotel_security.xml',
        'security/ir.model.access.csv',

        'wizard/hotel_pay_views.xml',
        'views/hotel_menu_root.xml',
        
        'views/hotel_reservation_form_view.xml',
        
        'views/hotel_room_view.xml',
        'views/hotel_room_type_view.xml',
        'views/hotel_promotion_view.xml',
        'views/hotel_service_view.xml',
        'views/hotel_service_detail_view.xml',
        'views/hotel_position_view.xml',
        'views/hotel_staff_view.xml',


        'reports/reports.xml',
        'reports/reservation_template.xml',
        'views/hotel_room_rental_details_view.xml',
        'data/mail_template.xml',
        'data/mail_activity_type.xml',
        'static/xml/home.xml'


    ],
    # 'qweb': [
    #     'static/src/xml/*.xml',
    #     'static/src/css/*.css',
    # ],
    'installable': True,
    'application': True,
}
