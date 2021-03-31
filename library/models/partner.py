# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_author = fields.Boolean(string="Is an Author", default=False)
    is_publisher = fields.Boolean(string="Is a Publisher", default=False)

    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
    total_due = fields.Float(compute="_compute_total_due", store=True)

    @api.depends('rental_ids.state', 'rental_ids.total_price')
    def _compute_total_due(self):
        for record in self:
            total_due = 0
            for rental in record.rental_ids:
                if rental.state != 'paid':
                    total_due += rental.total_price
            record.total_due = total_due