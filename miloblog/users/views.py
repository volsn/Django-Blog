from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from miloblog import db
from miloblog.models import User, BlogPost, NewsletterSubscription, UserStatus
from miloblog.users.forms import RegistrationForm, LoginForm,\
    UpdateUserForm, SubscribeForm
from miloblog.utils.picture_handlers import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Log in Success!')

            next_ = request.args.get('next')
            if next_ is None or next_[0] != '/':
                next_ = url_for('core.index')

            return redirect(next_)
    return render_template('users/login.html', form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('users/account.html', profile_image=profile_image, form=form)


@users.route('/subscribe', methods=['POST'])
def subscribe():
    form = SubscribeForm()

    if form.validate_on_submit():
        email = form.email.data
        if NewsletterSubscription.query.filter_by(email=email).first():
            return render_template('core/message.html',
                                   message='You\'re already subscribed!')
        else:
            subscriber = NewsletterSubscription(email=email)
            db.session.add(subscriber)
            db.session.commit()
            return render_template('core/message.html',
                                   message='Thanks! You\'ve successfully subscribed to our newsletter!')

    return render_template('core/message.html',
                           message='Sorry! Something went wrong')


@users.route('/unsubscribe/<email>', methods=['GET', 'POST'])
def unsubscribe(email):
    subscriber = NewsletterSubscription.query.filter_by(email=email).first()
    if subscriber:
        db.session.delete(subscriber)
        db.session.commit()
    return render_template('core/message.html',
                           message='Sorry to see you leaving :( Hope you\'ll come back soon.')


@users.app_template_filter()
def is_subscribed(user):
    if user.is_authenticated:
        return NewsletterSubscription.query.filter_by(email=user.email).first()
    return False


@users.route('/ban/<pk>')
def ban(pk):

    if not current_user.is_authenticated or current_user.status != UserStatus.admin:
        abort(403)

    user = User.query.get_or_404(pk)
    user.status = UserStatus.banned
    db.session.commit()

    next_ = request.args.get('next', None)
    if not next_:
        next_ = url_for('core.index')

    return redirect(next_)


@users.route('/unban/<pk>')
def unban(pk):

    if not current_user.is_authenticated or current_user.status != UserStatus.admin:
        abort(403)

    user = User.query.get_or_404(pk)
    user.status = UserStatus.active
    db.session.commit()

    next_ = request.args.get('next', None)
    if not next_:
        next_ = url_for('core.index')

    return redirect(next_)
