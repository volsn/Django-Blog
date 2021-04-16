import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# Login
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'


# Templates
from miloblog.models import UserStatus, BlogCategory, BlogPost
from miloblog.users.forms import SubscribeForm


@app.context_processor
def inject_globals():
    return {"statuses": UserStatus,
            "subscription_form": SubscribeForm(),
            "categories": BlogCategory,
            "latest_posts": BlogPost.query.order_by(BlogPost.date.desc()).limit(2)}


@app.template_filter()
def is_admin(user):
    return user.is_authenticated and user.status == UserStatus.admin


# Blueprints
from miloblog.core.views import core
from miloblog.blog_posts.views import blogs
from miloblog.users.views import users
from miloblog.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(blogs)
app.register_blueprint(users)
app.register_blueprint(error_pages)

# Start admin
from miloblog.admin import admin
