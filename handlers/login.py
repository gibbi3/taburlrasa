from models.user import User
from helpers import *
from handlers.handler import Handler

class Login(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = db.GqlQuery("SELECT * FROM User WHERE username= :1", username)
        result = u.get()
        if result:
            if valid_pw(username, password, result.password):
                self.set_secure_cookie('user_id', str(username))
                self.render('welcome.html', username=username)
            else:
                msg = 'Invalid password'
                self.render('login.html', error = msg)
        else:
            msg = 'User does not exist. '
            self.render('login.html', error_username = msg)
