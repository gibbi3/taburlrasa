from google.appengine.ext import db

class Comments(db.Model):
    comment = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    writer = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
