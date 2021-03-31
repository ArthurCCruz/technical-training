# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_maester = fields.Boolean('Is Maester')

    session_ids = fields.Many2many(
        'oa.session',
        'session_attendee_rel',
        'attendee_id',
        'session_id',
    )
