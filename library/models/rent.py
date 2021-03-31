# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryRent(models.Model):
    _name = 'library.rent'
    _description = 'Rent Registry'

    partner_id = fields.Many2one(
        'library.partner',
        'Customer'
    )

    partner_email = fields.Char('Customer Email', related='partner_id.email')
    partner_phone = fields.Char('Customer Phone', related='partner_id.phone_number')

    copy_id = fields.Many2one('library.book.unique', 'Book')
    book_ISBN = fields.Char('Book ISBN', related='copy_id.ISBN')

    rental_date = fields.Datetime()
    return_date = fields.Datetime()

    state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('late', 'Late'),
            ('returned', 'Returned')
        ],
        string='State'
    )
