from handlers.handler import Handler
from helpers import *
from models.user import User
from models.poetry import Poetry
from models.comments import Comments

class Comment(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)
        if post:
            cookie = read_secure_cookie(self, 'user_id')
            if cookie:
                self.render("comment.html", post=post)
            else:
                self.redirect('/login')

    def post(self, post_id):
            key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
            post = db.get(key)
            if post:
                comment = self.request.get("comment")
                if comment:
                    c = Comments(username = retrieve_username(self, 'user_id'),
                                 writer = retrieve_username_hash(self,
                                                                 'user_id'),
                                 comment = comment,
                                 post_id=post.key().id())
                    c.put()
                    self.redirect('/post/%s' % str(post.key().id()))
                else:
                    key = db.Key.from_path('Poetry', int(post_id),
                                           parent=post_key())
                    post = db.get(key)
                    self.redirect('/post/%s' % str(post.key().id()))
            else:
                self.render("errorexist.html")
