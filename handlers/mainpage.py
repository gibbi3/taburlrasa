from handlers.handler import Handler
from helpers import *
from models.poetry import Poetry
from models.user import User

class MainPage(Handler):
    def get(self):
        cookie = read_secure_cookie(self, 'user_id')
        if cookie:
            poems = db.GqlQuery("SELECT * FROM Poetry ORDER BY created DESC")
            self.render('index.html', poems = poems)
        else:
            self.redirect('/login')
