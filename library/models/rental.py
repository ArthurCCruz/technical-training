# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('res.partner', string='Customer')
    copy_id = fields.Many2one('library.copy', string="Book Copy")
    book_id = fields.Many2one('product.product', string='Book', related='copy_id.book_id', readonly=True)

    rental_date = fields.Date(default=fields.Date.context_today)
    return_date = fields.Date()
    rental_length = fields.Integer(
        'Rental Length (in days)',
        compute='_compute_rental_length',
        store=True
    )

    customer_address = fields.Text(compute='_compute_customer_address')
    customer_email = fields.Char(related='customer_id.email')

    book_authors = fields.Many2many(related='copy_id.author_ids')
    book_edition_date = fields.Date(related='copy_id.edition_date')
    book_publisher = fields.Many2one(related='copy_id.publisher_id')

    state = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('returned', 'Returned'),
            ('paid', 'Paid'),
        ],
        string='State',
        default='open',
        copy=False
    )

    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        related='book_id.currency_id'
    )

    rental_price = fields.Monetary(
        'Price for the rental',
        currency_field='currency_id',
        compute='_compute_rental_price',
        store=True
    )

    loss_fee = fields.Monetary(
        'Loss Fee',
        currency_field='currency_id',
    )

    total_price = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_total_price',
        store=True
    )

    @api.depends('customer_id')
    def _compute_customer_address(self):
        self.customer_address = self.customer_id.address_get()

    @api.depends('rental_date', 'return_date')
    def _compute_rental_length(self):
        for record in self:
            if not (record.return_date and record.rental_date):
                rental_length = 0
            else:
                rental_length = (record.return_date - record.rental_date).days
            if rental_length < 0:
                raise ValidationError(_('Return date can not be before the rental one.'))
            record.rental_length = rental_length

    @api.depends('rental_length', 'book_id')
    def _compute_rental_price(self):
        for record in self:
            record.rental_price = record.rental_length * record.book_id.lst_price

    @api.depends('rental_price', 'loss_fee')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.rental_price + record.loss_fee

    def button_apply_loss_fee(self):
        self._apply_loss_fee()

    def _apply_loss_fee(self):
        for record in self:
            record.write({
                'loss_fee': record.book_id.loss_fee
            })

    def button_register_return(self):
        self._register_return()
    
    def _register_return(self):
        self.write({
            'return_date': fields.Date.today(),
            'state': 'returned'
        })

    def button_register_payment(self):
        self._register_payment()
    
    def _register_payment(self):
        self.write({
            'state': 'paid'
        })