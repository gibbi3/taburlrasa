from handlers.handler import Handler
from helpers import *
from models.user import User
from models.comments import Comments

class DeleteComment(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Comments', int(post_id))
        comment = db.get(key)
        if comment:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                if comment.writer == retrieve_username_hash(self, 'user_id'):
                    comment.delete()
                    self.redirect("/post/%s" % str(comment.post_id))
                else:
                    self.render("errordelete.html")
            else:
                self.redirect("/login")
