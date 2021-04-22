from flask import render_template, Blueprint, request
from flask_login import current_user
from miloblog import db
from miloblog.models import BlogPost, Message
from miloblog.core.forms import GetInTouchForm

core = Blueprint('core', __name__)


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=6)
    return render_template('core/index.html',
                           blog_posts=blog_posts)


@core.route('/about')
def about():
    return render_template('core/about.html')


@core.route('/contact', methods=['GET', 'POST'])
def contact():
    form = GetInTouchForm()
    if form.validate_on_submit():

        message = Message(name=form.name.data,
                          company=form.company.data,
                          email=form.company.data,
                          message=form.message.data)
        db.session.add(message)
        db.session.commit()

        return render_template('core/message.html',
                               message='Thank you! Your message has been sent!')
    elif request.method == 'GET' and current_user.is_authenticated:
        form.name.data = current_user
        form.email.data = current_user.email

    return render_template('core/contact.html',
                           form=form)


@core.route('/editor')
def editor():
    return render_template('editor.html')
