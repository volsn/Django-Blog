import enum
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from miloblog import db, login_manager


class BlogCategory(enum.Enum):
    blank = None
    journey = 'Journey'
    work = 'Work'
    lifestyle = 'Lifestyle'
    photography = 'Photography'
    food_and_drinks = 'Food & Drinks'


class UserStatus(enum.Enum):
    active = 'active'
    banned = 'banned'
    admin = 'admin'


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), nullable=True, default='')
    last_name = db.Column(db.String(64), nullable=True, default='')
    status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.active)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('BlogPost', backref='author')
    comments = db.relationship('Comment', backref='author')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username


class BlogPost(db.Model):

    __tablename__ = 'blogpost'

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.String(140), nullable=False)
    main_image = db.Column(db.String(64), nullable=False, default='default_article.png')
    short_description = db.Column(db.Text, nullable=False)
    category = db.Column(db.Enum(BlogCategory), default=BlogCategory.blank, nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post ID: { self.id } -- Date: { self.date } --- { self.title }"


class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    blog = db.Column(db.Integer, db.ForeignKey('blogpost.id'), nullable=False)
    approved = db.Column(db.Boolean, default=0)
    reply_to = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True, default=-1)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    text = db.Column(db.Text(512), nullable=False)

    def __repr__(self):
        return f'{ self.user_id } - { self.text }'


class NewsletterSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))

    def __repr__(self):
        return self.email
