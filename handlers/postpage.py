from handlers.handler import Handler
from helpers import *
from models.poetry import Poetry
from models.comments import Comments

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)
        if post:
            commentary = db.GqlQuery("SELECT * FROM Comments WHERE post_id =:1 "
                                     " ORDER BY created ASC", post.key().id())
            self.render("post.html", post = post, commentary = commentary)
        else:
            self.render("errorexist.html")
