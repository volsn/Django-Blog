from flask import request, redirect, url_for, render_template
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from miloblog import app, db
from miloblog.models import BlogPost, User, Comment,\
    NewsletterSubscription, UserStatus, Message


class MyAdminIndexView(AdminIndexView):

    extra_css = ['css/fontawesome.css']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.status == UserStatus.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('users.login', next=request.url))

    def render(self, template, **kwargs):
        kwargs['messages_count'] = Message.query.filter_by(read=False).count()
        return super().render(template, **kwargs)


class LoginRequiredModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.status == UserStatus.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('users.login', next=request.url))


class BlogPostModelView(LoginRequiredModelView):
    can_export = True
    column_exclude_list = ['text', 'author', 'users', 'main_image']
    column_filters = ['category']
    column_searchable_list = ['title', 'short_description', 'text']
    column_list = ['id', 'title', 'short_description', 'category', 'date']


class UserModelView(LoginRequiredModelView):
    column_exclude_list = ['profile_image', 'password_hash']
    column_filters = ['status']


class CommentModelView(LoginRequiredModelView):
    column_list = ['text', 'author', 'approved', 'date']
    column_filters = ['approved']


class MessageModelView(LoginRequiredModelView):
    can_view_details = True
    column_exclude_list = ['message']
    column_filters = ['read']


admin = Admin(app, name='Milø.admin', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(BlogPostModelView(BlogPost, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(CommentModelView(Comment, db.session))
admin.add_view(LoginRequiredModelView(NewsletterSubscription, db.session))
admin.add_view(MessageModelView(Message, db.session))
