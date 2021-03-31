# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OASession(models.Model):
    _name = 'oa.session'
    _description = 'A class session'

    maester_id = fields.Many2one(
        'res.partner',
        'Maester',
        domain=[('is_maester', '=', True)]
    )

    class_id = fields.Many2one(
        'oa.class',
        'Class',
        required=True,
        ondelete='cascade'
    )

    attendees_ids = fields.Many2many(
        'res.partner',
        'session_attendee_rel',
        'session_id',
        'attendee_id'
    )
    state = fields.Selection(
        selection=[
            ('preparation', 'Preparation'),
            ('ready', 'Ready')
        ],
        string='State'
    )

    room_size = fields.Integer()

    start_date = fields.Datetime('Start date')
    end_date = fields.Datetime('End date')

    attendees_count = fields.Integer(
        'Quantity of Attendees',
        compute='_compute_attendees_count',
        store=True
    )

    room_percentage = fields.Float(
        'Quantity of Attendees',
        compute='_compute_attendees_count',
        store=True
    )
    
    @api.depends('attendees_ids', 'room_size')
    def _compute_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendees_ids)
            if record.room_size:
                record.room_percentage = len(record.attendees_ids) / record.room_size

    @api.constrains('attendees_count')
    def validate_attendees_count(self):
        for record in self:
            if record.attendees_count > record.room_size:
                raise ValidationError(
                    'Attendees count can not be greater than %s.' % record.room_size
                )
