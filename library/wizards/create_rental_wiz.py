from odoo import models, fields


class CreateRentalWiz(models.TransientModel):
    _name = 'create.rental.wiz'

    copy_ids = fields.Many2many(
        'library.copy',
        string="Copys"
    )

    partner_id = fields.Many2one('res.partner', 'Customer')
    return_date = fields.Date()
    rental_date = fields.Date(default=fields.Date.context_today)

    def button_submit(self):
        new_rental_ids = []
        for copy in self.copy_ids:
            new_rental = self.env['library.rental'].create({
                'copy_id': copy.id,
                'customer_id': self.partner_id.id,
                'return_date': self.return_date
            })
            new_rental_ids.append(new_rental.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.rental',
            'name': 'New Rentals',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', new_rental_ids)],
        }
