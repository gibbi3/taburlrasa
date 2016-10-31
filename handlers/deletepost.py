from handlers.handler import Handler
from helpers import *
from models.user import User
from models.poetry import Poetry

class DeletePost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)
        if post:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                if post.writer == retrieve_username_hash(self, 'user_id'):
                    post.delete()
                    self.redirect("/")
                else:
                    self.render("errordelete.html")
            else:
                self.redirect("/login")
        else:
            self.render("errorexist.html")
