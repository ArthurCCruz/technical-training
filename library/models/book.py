# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Books'

    name = fields.Char('Title')

    author_ids = fields.Many2many(
        'library.partner',
        'book_author_rel',
        'book_id',
        'author_id',
        'Authors',
        domain=[('is_author','=',True)]
    )

    editor_id = fields.Many2one(
        'library.partner',
    )

    ISBN = fields.Char('ISBN')

    copy_ids = fields.One2many(
        'library.book.unique',
        'book_id',
        'Copies'
    )


class LibraryBookUnique(models.Model):
    _name = 'library.book.unique'
    _inherits = {'library.book': 'book_id'}

    book_id = fields.Many2one(
        'library.book', 'Book',
        auto_join=True, ondelete="cascade", required=True)
    
    rent_ids = fields.One2many(
        'library.rent',
        'copy_id',
        'Rent Registry'
    )

    default_code = fields.Char('Internal Reference')
