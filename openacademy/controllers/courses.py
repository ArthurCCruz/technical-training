from odoo.http import Controller, route, request


class Courses(Controller):
    def _render_sessions(self, sessions):
        return request.render(
            'openacademy.website_sessions_list',
            {
                'sessions': sessions
            }
        )

    @route(
        '/courses',
        auth='public',
        website=True
    )
    def courses(self):
        courses = request.env['openacademy.course'].search([
        ])
        return request.render(
            'openacademy.website_courses_list',
            {
                'courses': courses
            }
        )

    @route(
        '/courses/<model("openacademy.course"):course>/',
        auth='public',
        website=True
    )
    def course_details(self, course):
        return request.render(
            'openacademy.website_course_details',
            {
                'course': course
            }
        )

    @route(
        '/courses/<model("openacademy.course"):course>/sessions',
        auth='public',
        website=True
    )
    def course_sessions(self, course):
        return self._render_sessions(course.session_ids)

    @route(
        '/sessions/<model("openacademy.session"):session>',
        auth='public',
        website=True
    )
    def session(self, session):
        return request.render(
            'openacademy.website_session_details',
            {
                'session': session
            }
        )

    @route(
        '/sessions',
        auth='public',
        website=True
    )
    def sessions(self):
        sessions = request.env['openacademy.session'].search([])
        return self._render_sessions(sessions)
        