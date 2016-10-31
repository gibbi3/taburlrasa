from handlers.handler import Handler
from helpers import *
from models.user import User
from models.poetry import Poetry

class UnLike(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)
        cookie = self.request.cookies.get('user_id')
        if cookie:
            unliker = retrieve_username(self, 'user_id')
            if unliker != post.username and unliker in post.likers:
                if post:
                    post.likes -= 1
                    post.likers.remove(retrieve_username(self, 'user_id'))
                    post.put()
                    self.redirect("/")
                else:
                    self.response.out.write("Post not found.")
            elif unliker == post.username:
                self.render("erroruserunlike.html")
            else:
                self.render("errorunlike.html")
        else:
            self.redirect("/login")
