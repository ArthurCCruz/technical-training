from odoo import models, fields, api


class PartnerToSessionWiz(models.TransientModel):
    _name = 'partner.to.session.wiz'

    partner_ids = fields.Many2many('res.partner')
    course_id = fields.Many2one('openacademy.course', 'Course')
    session_id = fields.Many2one('openacademy.session', 'Session')

    @api.onchange('course_id')
    def _handle_course_change(self):
        return {
            'domain': {
                'session_id': [
                    ('course_id', '=', self.course_id.id),
                ]
            }
        }

    def button_add_partner_to_session(self):
        new_attendee_ids = [*dict.fromkeys(
            self.session_id.attendee_ids.ids +
            self.partner_ids.ids
        )]
        self.session_id.write({
            'attendee_ids': [(6, 0, new_attendee_ids)]
        })