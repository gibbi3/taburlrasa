from google.appengine.ext import db

class Poetry(db.Model):
    title = db.StringProperty(required = True)
    poem = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    writer = db.StringProperty(required = True)
    username = db.StringProperty(required = True)
    likes = db.IntegerProperty(required = True)
    likers = db.ListProperty(str)
