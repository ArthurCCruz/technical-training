# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Books(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many("res.partner", string="Authors", domain=[('is_author', '=', True)])
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN', unique=True)
    publisher_id = fields.Many2one('res.partner', string='Publisher', domain=[('is_publisher', '=', True)])

    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")
    is_book = fields.Boolean(string='Is a Book', default=False)

    customers_count = fields.Integer(compute="_compute_customers_count")

    @api.depends('copy_ids.rental_ids.customer_id')
    def _compute_customers_count(self):
        for record in self:
            record.customers_count = len(record.copy_ids.mapped('rental_ids.customer_id'))

    def button_show_rental_customers(self):
        action = self.env.ref('library.partner_action').read()[0]
        action['domain'] = [
            ('id', 'in', self.copy_ids.mapped('rental_ids.customer_id.id'))
        ]
        return action


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('product.product', string="Book", domain=[('is_book', "=", True)], required=True, ondelete="cascade", delegate=True)
    reference = fields.Char(required=True, string="Ref")

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
    book_state = fields.Selection([('available', 'Available'), ('rented', 'Rented'), ('lost', 'Lost')], default="available")
