from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_mail import Mail
from models import User, Comment, Community, Post
from .config import Config
from .auth import auth
from .communities import comms
from .community import community

# login manager and some of it's configuration
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.session_protection = "strong"

# for logging in the user. Pretty similar to the one in models.py 
# but i wanted to do one function for each purpose
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))




# whitelisting bootstrap styles and js url for talisman

csp = {
    'default-src': [
        '\'self\'',
        'cdnjs.cloudflare.com',
        'cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
        'cdn.jsdelivr.net',
        'bootstrap.bundle.min.js'
        'www.w3.org'
    ]
}


# creating the app and initializing the login manager as well as the bootstrap extension
def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    #mail.init_app(app)
    app.config.from_object(Config)
    talisman = Talisman(app, content_security_policy=csp)
    login_manager.init_app(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(comms)
    app.register_blueprint(community)
    return app

