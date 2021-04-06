from odoo import http

class Books(http.Controller):
    @http.route(
        '/books',
        auth='public',
        website=True
    )
    def books(self):
        return http.request.render(
            'library.books_list',
            {
                'books': http.request.env['product.product'].search([])
            }
        )

    @http.route(
        '/books/<model("product.product"):book>',
        auth='public',
        website=True
    )
    def book(self, book):
        return http.request.render(
            'library.book_view',
            {
                'book': book
            }
        )