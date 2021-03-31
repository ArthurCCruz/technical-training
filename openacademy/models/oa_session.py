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
            ('draft', 'Preparation'),
            ('ready', 'Ready'),
            ('confirmed', 'Confirmed')
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
            attendees_count = len(record.attendees_ids)
            room_size = record.room_size
            if room_size:
                room_percentage = (attendees_count / room_size) * 100
            else:
                room_percentage = 0
            record.attendees_count = attendees_count
            record.room_percentage = room_percentage
            if room_percentage >= 50:
                record.state = 'confirmed'
                

    @api.constrains('attendees_count')
    def validate_attendees_count(self):
        for record in self:
            if record.attendees_count > record.room_size:
                raise ValidationError(
                    'Attendees count can not be greater than %s.' % record.room_size
                )
