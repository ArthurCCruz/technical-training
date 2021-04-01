from odoo import models, fields, api


class PartnerToSessionWiz(models.TransientModel):
    _name = 'partner.to.session.wiz'

    partner_id = fields.Many2one('res.partner', 'Attendee')
    course_id = fields.Many2one('openacademy.course', 'Course')
    session_id = fields.Many2one('openacademy.session', 'Session')

    @api.onchange('course_id')
    def _handle_course_change(self):
        return {
            'domain': {
                'session_id': [
                    ('course_id', '=', self.course_id.id),
                    ('id', 'not in', self.partner_id.session_ids.ids)
                ]
            }
        }

    def button_add_partner_to_session(self):
        self.session_id.write({
            'attendee_ids': [(4, self.partner_id.id, 0)]
        })