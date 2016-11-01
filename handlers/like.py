from handlers.handler import Handler
from helpers import *
from models.user import User
from models.poetry import Poetry

class Like(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)
        if post:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                liker = retrieve_username(self, 'user_id')
                if liker != post.username and liker not in post.likers:
                    post.likes += 1
                    post.likers.append(retrieve_username(self, 'user_id'))
                    post.put()
                    self.redirect("/post/%s" % str(post.key().id()))
                elif liker == post.username:
                    self.render("errorlikeuser.html")
                else:
                    self.render("errorlike.html")
            else:
                self.redirect("/login")
        else:
            self.render("errorexist.html")
