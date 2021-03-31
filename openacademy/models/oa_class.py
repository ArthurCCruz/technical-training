# -*- coding: utf-8 -*-
from odoo import models, fields

class OAClass(models.Model):
    _name = 'oa.class'
    _description = 'A course'

    name = fields.Char('Name')

    level = fields.Selection(
        [
            ('0', 'Easy'),
            ('1', 'Medium'),
            ('2', 'Hard'),
        ],
        'Level'
    )
    