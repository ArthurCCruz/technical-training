from odoo.http import Controller, route, request
from datetime import date, datetime
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class Rental(Controller):
    @route(
        '/rental',
        auth='user',
        website=True,
        methods=['GET', 'POST']
    )
    def create_rental(self, **kw):
        copy_id = kw.get('copy_id')
        if not copy_id:
            return request.redirect('/books')
        copy = request.env['library.copy'].browse(int(copy_id))
        if request.httprequest.method == 'POST':
            if not kw.get('return_date'):
                raise Exception('A return date need to be provided!')
            if copy.book_state == 'available':
                rental = request.env['library.rental'].create({
                    'customer_id': request.env.user.partner_id.id,
                    'copy_id': copy.id,
                    'rental_date': date.today(),
                    'return_date': datetime.strptime(kw.get('return_date'), ('%m/%d/%Y'))
                })
                rental.action_confirm()
                return request.render(
                    'library.successful_rental', {}
                )
            else:
                raise Exception('This copy is not available!')

        elif request.httprequest.method == 'GET':
            return request.render(
                'library.create_rental_view',
                {
                    'copy': copy,
                }
            )
