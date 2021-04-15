from flask import render_template, Blueprint, request, flash
from flask_login import login_required, current_user
from miloblog.models import BlogPost, BlogCategory
from miloblog.core.forms import GetInTouchForm
from miloblog.users.forms import SubscribeForm

core = Blueprint('core', __name__)


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=6)
    selected_posts = BlogPost.query.order_by(BlogPost.date.desc()).limit(2)
    subscription_form = SubscribeForm()
    return render_template('core/index.html',
                           blog_posts=blog_posts,
                           selected_posts=selected_posts,
                           subscription_form=subscription_form,
                           categories=BlogCategory)


@core.route('/about')
def about():
    subscription_form = SubscribeForm()
    return render_template('core/about.html',
                           subscription_form=subscription_form)


@core.route('/contact', methods=['GET', 'POST'])
def contact():
    form = GetInTouchForm()
    subscription_form = SubscribeForm()
    if form.validate_on_submit():
        return render_template('core/message.html',
                               message='Thank you! Your message has been sent!')
    elif request.method == 'GET' and current_user.is_authenticated:
        form.name.data = current_user.first_name + ' ' + current_user.last_name
        form.email.data = current_user.email

    return render_template('core/contact.html',
                           form=form,
                           subscription_form=subscription_form)
