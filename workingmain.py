import os
import re
import random
import hashlib
import hmac
from string import letters
import webapp2
import jinja2

from google.appengine.ext import db

#Jinja2 configuration.

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'Ohweelittlesleekittimrouse'

# Helping funcitons for Jinja2.

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class Handler(webapp2.RequestHandler):

# Helping functions for Jinja2.

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

# Clears cookie.

    def logout(self):
        self.response.headers.add_header(
        'set-cookie', 'user_id=; Path=/')

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

# Verifies existence of necessary encoded cookie for site usage.

def read_secure_cookie(self, name):
    cookie_val = self.request.cookies.get(name)
    return cookie_val and check_secure_val(cookie_val)

# Retrieves the encoded username from user_id cookie. Used for validation.

def retrieve_username_hash(self, name):
    cookie_val = self.request.cookies.get(name)
    val = cookie_val.split('|')[1]
    return val

# Retrieves the username from user_id cookie. Used for display purposes.

def retrieve_username(self, name):
    cookie_val = self.request.cookies.get(name)
    val = cookie_val.split('|')[0]
    return val

def post_key(name = 'default'):
    return db.Key.from_path('posts', name)

def render_post(response, post):
    response.out.write('<b>' + poetry.title + '</b><br>')
    response.out.write(poetry.poem)

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

# Hashes password and stores salt.

def make_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


# Retrieves salt from cookie and uses it in conjunction with sha256 encoding
# to hash entered password. This hash is compared to that in the database.

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_hash(name, password, salt)

# Database models and the attributes found in each entity.

class Poetry(db.Model):
    title = db.StringProperty(required = True)
    poem = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    writer = db.StringProperty(required = True)
    username = db.StringProperty(required = True)
    likes = db.IntegerProperty(required = True)
    likers = db.ListProperty(str)

    def render(self):
        self._render_text = self.poem.replace('\n', '<br>')
        return render_str("post.html", p = self)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()

class Comments(db.Model):
    comment = db.TextProperty(required = True)
    username = db.StringProperty(required = True)
    writer = db.StringProperty(required = True)
    post_id = db.IntegerProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#Checking for the validity of entries for usernames, passwords, and emails.

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

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
                self.render('welcome.html', username=username)

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

class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')

class MainPage(Handler):
    def get(self):
        cookie = read_secure_cookie(self, 'user_id')
        if cookie:
            poems = db.GqlQuery("SELECT * FROM Poetry ORDER BY created DESC")
            self.render('index.html', poems = poems)
        else:
            self.redirect('/login')

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)

# This query searches all comments and returns those belonging to the given post.

        commentary = db.GqlQuery("SELECT * FROM Comments WHERE post_id =:1 ORDER BY created ASC", post.key().id())
        if not post:
            self.response.out.write("Post does not exist.")

        self.render("permalink.html", post = post, commentary = commentary)

class Muse(Handler):

    def get(self):
        cookie = read_secure_cookie(self, 'user_id')
        if cookie:
            self.render("muse.html")
        else:
            self.redirect('/login')

    def post(self):
        title = self.request.get("title")
        poem = self.request.get("poem")

        if title and poem:
            p = Poetry(parent = post_key(),
                       title=title, poem=poem,
                       writer=retrieve_username_hash(self, 'user_id'),
                       username=retrieve_username(self,'user_id'),
                       likes=0, likers = [])
            p.put()
            self.redirect('/post/%s' % str(p.key().id()))
        else:
            error = "Both title and content are required."
            self.render('muse.html', title=title, poem=poem, error=error)

class EditPost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post_to_edit = db.get(key)
        cookie = self.request.cookies.get('user_id')
        if cookie:
            if post_to_edit.writer == retrieve_username_hash(self, 'user_id'):
                self.render("edit.html", title = post_to_edit.title,
                                         poem = post_to_edit.poem,
                                         post = post_to_edit)
            else:
                self.render("errorpost.html")
        else:
            self.redirect("/login")

    def post(self, post_id):
        edited_title = self.request.get("title")
        edited_poem = self.request.get("poem")

        if edited_title and edited_poem:
            key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
            post_to_edit = db.get(key)
            post_to_edit.title = edited_title
            post_to_edit.poem = edited_poem
            post_to_edit.put()
            self.redirect('/post/%s' % str(post_to_edit.key().id()))


class DeletePost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post_to_delete = db.get(key)
        cookie = self.request.cookies.get('user_id')
        if cookie:
            if post_to_delete.writer == retrieve_username_hash(self, 'user_id'):
                post_to_delete.delete()
                self.redirect("/")
            else:
                self.render("errordelete.html")
        else:
            self.redirect("/login")

class Comment(Handler):
    def get(self, post_id):
        cookie = read_secure_cookie(self, 'user_id')
        if cookie:
            key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
            post = db.get(key)
            self.render("comment.html", post=post)
        else:
            self.redirect('/login')

    def post(self, post_id):
            comment = self.request.get("comment")

            if comment:
                key = db.Key.from_path('Poetry', int(post_id),
                                                 parent=post_key())
                post = db.get(key)
                c = Comments(username = retrieve_username(self, 'user_id'),
                    writer = retrieve_username_hash(self, 'user_id'),
                    comment = comment,
                    post_id=post.key().id())
                c.put()
                self.redirect('/post/%s' % str(post.key().id()))
            else:
                key = db.Key.from_path('Poetry',
                    int(post_id),
                    parent=post_key())
                post = db.get(key)
                self.redirect('/post/%s' % str(post.key().id()))

class EditComment(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Comments', int(post_id))
        comment_to_edit = db.get(key)
        cookie = self.request.cookies.get('user_id')
        if cookie:
            if comment_to_edit.writer == retrieve_username_hash(self,
                                                                'user_id'):
                self.render("edit-comment.html",
                resident_post = int(comment_to_edit.post_id))
            else:
                self.render("errorpost.html")
        else:
            self.redirect("/login")

    def post(self, post_id):
        edited_comment = self.request.get("comment")

        if edited_comment:
            key = db.Key.from_path('Comments', int(post_id))
            comment_to_edit = db.get(key)
            comment_to_edit.comment = edited_comment
            comment_to_edit.put()
            self.redirect("/post/%s" % str(comment_to_edit.post_id))
        else:
            self.redirect("/post/%s" % str(comment_to_edit.post_id))

class DeleteComment(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Comments', int(post_id))
        comment_to_delete = db.get(key)
        cookie = self.request.cookies.get('user_id')
        if cookie:
            if comment_to_delete.writer == retrieve_username_hash(self,
                                                                  'user_id'):
                comment_to_delete.delete()
                self.redirect("/post/%s" % str(comment_to_delete.post_id))
            else:
                self.render("errordelete.html")
        else:
            self.redirect("/login")


class Like(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Poetry', int(post_id), parent=post_key())
        post = db.get(key)
        cookie = self.request.cookies.get('user_id')
        if cookie:
            liker = retrieve_username(self, 'user_id')
            if liker != post.username and liker not in post.likers:
                if post:
                    post.likes += 1
                    post.likers.append(retrieve_username(self, 'user_id'))
                    post.put()
                    self.redirect("/")
                else:
                    self.response.out.write("Post not found.")
            elif liker == post.username:
                self.render("errorlikeuser.html")
            else:
                self.render("errorlike.html")
        else:
            self.redirect("/login")

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


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/muse', Muse),
                               ('/post/(\d+)', PostPage),
                               ('/register', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/post/edit/(\d+)', EditPost),
                               ('/post/delete/(\d+)', DeletePost),
                               ('/post/comment/(\d+)', Comment),
                               ('/post/comment/edit/(\d+)', EditComment),
                               ('/post/comment/delete/(\d+)', DeleteComment),
                               ('/post/(\d+)/like', Like),
                               ('/post/(\d+)/unlike', UnLike)
                               ], debug=True)
