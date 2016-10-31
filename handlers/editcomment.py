from handlers.handler import Handler
from helpers import *
from models.user import User
from models.poetry import Poetry
from models.comments import Comments

class EditComment(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Comments', int(post_id))
        comment = db.get(key)
        if comment:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                if comment.writer == retrieve_username_hash(self, 'user_id'):
                    self.render("edit-comment.html",
                    resident_post = int(comment.post_id))
                else:
                    self.render("errorpost.html")
            else:
                self.redirect("/login")
        else:
            self.render("errorexist.html")

    def post(self, post_id):
        key = db.Key.from_path('Comments', int(post_id))
        comment = db.get(key)
        if comment:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                if comment.writer == retrieve_username_hash(self, 'user_id'):
                    edited_comment = self.request.get("comment")
                    if edited_comment:
                        key = db.Key.from_path('Comments', int(post_id))
                        comment = db.get(key)
                        comment.comment = edited_comment
                        comment.put()
                        self.redirect("/post/%s" % str(comment.post_id))
                    else:
                        self.redirect("/post/%s" % str(comment.post_id))
                else:
                    self.render("errorpost.html")
            else:
                self.redirect("/login")
        else:
            self.render("errorexist.html")
