from handlers.handler import Handler
from helpers import *
from models.poetry import Poetry
from models.user import User


class EditPost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post_to_edit = db.get(key)
        if post_to_edit:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                if post_to_edit.writer == retrieve_username_hash(self,
                                                                'user_id'):
                    self.render("edit.html", title = post_to_edit.title,
                                             poem = post_to_edit.poem,
                                             post = post_to_edit)
                else:
                    self.render("errorpost.html")
            else:
                self.redirect("/login")
        else:
            self.render("errorexist.html")

    def post(self, post_id):
        edited_title = self.request.get("title")
        edited_poem = self.request.get("poem")
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post_to_edit = db.get(key)
        if post_to_edit:
            cookie = self.request.cookies.get('user_id')
            if cookie:
                if post_to_edit.writer == retrieve_username_hash(self,
                                                                    'user_id'):
                    if edited_title and edited_poem:
                        post_to_edit.title = edited_title
                        post_to_edit.poem = edited_poem
                        post_to_edit.put()
                        self.redirect('/post/%s' % str(post_to_edit.key().id()))
                    else:
                        self.redirect('/post/%s' % str(post_to_edit.key().id()))                        
                else:
                    self.render("errorpost.html")
            else:
                self.redirect("/login")
        else:
            self.render("errorexist.html")
