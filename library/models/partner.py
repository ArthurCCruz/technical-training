# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryPartner(models.Model):
    _name = 'library.partner'
    _description = 'All People'

    is_editor = fields.Boolean()
    is_author = fields.Boolean()
    is_customer = fields.Boolean()

    name = fields.Char()
    email = fields.Char()
    
    phone_number = fields.Char()

    address = fields.Text()

    rent_ids = fields.One2many(
        'library.rent',
        'partner_id',
        'Rent Registry'
    )


    