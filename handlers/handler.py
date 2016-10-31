import webapp2

from helpers import *
from models.user import User

class Handler(webapp2.RequestHandler):

# Helping functions for Jinja2.

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def logout(self):
        self.response.headers.add_header(
        'set-cookie', 'user_id=; Path=/')

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))
