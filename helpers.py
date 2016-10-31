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
