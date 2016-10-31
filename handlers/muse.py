from handlers.handler import Handler
from helpers import *
from models.poetry import Poetry


class Muse(Handler):
    def get(self):
        cookie = read_secure_cookie(self, 'user_id')
        if cookie:
            self.render("muse.html")
        else:
            self.redirect('/login')

    def post(self):
        title = self.request.get("title")
        poem = self.request.get("poem")

        if title and poem:
            p = Poetry(parent = post_key(),
                       title=title, poem=poem,
                       writer=retrieve_username_hash(self, 'user_id'),
                       username=retrieve_username(self,'user_id'),
                       likes=0, likers = [])
            p.put()
            self.redirect('/post/%s' % str(p.key().id()))
        else:
            error = "Both title and content are required."
            self.render('muse.html', title=title, poem=poem, error=error)
