from helpers import *

from models.poetry import Poetry
from models.user import User
from models.comments import Comments

from handlers.handler import Handler
from handlers.register import Register
from handlers.login import Login
from handlers.logout import Logout
from handlers.mainpage import MainPage
from handlers.postpage import PostPage
from handlers.muse import Muse
from handlers.editpost import EditPost
from handlers.deletepost import DeletePost
from handlers.comment import Comment
from handlers.editcomment import EditComment
from handlers.deletecomment import DeleteComment
from handlers.like import Like
from handlers.unlike import UnLike

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
