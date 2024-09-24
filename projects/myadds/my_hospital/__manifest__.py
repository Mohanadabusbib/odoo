# -*- coding: utf-8 -*-
{
    'name': "Hospital Manager",
    'summary': "Product for hospitals and patients",
    'description': """
        using this module for complete manage your hospital and get good reports 
    """,
    'author': "alMohamady",
    'website': "https://www.alMohamady.com",
    'category': 'Uncategorized',
    'version': '0.1.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/templates.xml',
        'views/views.xml',
        'views/doctors.xml',
        'views/appointments.xml',
        'views/menus.xml',
    ],
}

