from handlers.handler import Handler
from helpers import *
from models.user import User


class Register(Handler):
    def get(self):
        self.render("register.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                 email = email)

        if not valid_username(username):
            params['error_username'] = "You've entered an invalid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "You've entered an invalid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Passwords do not match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "Email provided is invalid, you charlatan."
            have_error = True

        if have_error:
            self.render('register.html', **params)
        else:
            u = User.all()
            u.filter("username =", username)
            result = u.get()
            if result:
                msg = 'User already registered'
                self.render('register.html', error_username = msg)
            else:
                user = User(username=username,
                            password=make_hash(username, password),
                            email=email)
                user.put()
                self.render('welcomenew.html', username=username)
