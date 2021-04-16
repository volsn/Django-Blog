from flask import render_template, request, Blueprint, abort, url_for, redirect
from flask_login import current_user
from miloblog import db
from miloblog.models import BlogPost, Comment, UserStatus
from miloblog.blog_posts.forms import LeaveComment, EditCommentForm, LeaveReplyForm

blogs = Blueprint('blogs', __name__)


@blogs.route('/blogs/<pk>', methods=['GET', 'POST'])
def blog_post(pk):
    post = BlogPost.query.get_or_404(pk)

    form = LeaveComment()
    if form.validate_on_submit():
        if current_user.is_authenticated:

            if current_user.status == UserStatus.banned:
                abort(403)

            comment = Comment(user_id=current_user.id,
                              blog=post.id,
                              text=form.text.data)

            if current_user.status == UserStatus.admin:
                comment.approved = True

            db.session.add(comment)
            db.session.commit()

    elif request.method == 'GET' and current_user.is_authenticated:
        form.name.data = current_user
        form.email.data = current_user.email

    comments = Comment.query.filter_by(blog=post.id, reply_to=-1).order_by(Comment.date.asc()).all()
    edit_form = EditCommentForm()
    reply_form = LeaveReplyForm()

    return render_template('blog_posts/post.html',
                           post=post,
                           comments=comments,
                           form=form,
                           edit_form=edit_form,
                           reply_form=reply_form)


@blogs.route('/blogs/category/<cat>')
def posts_category(cat):
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category=cat).order_by(BlogPost.date.desc()) \
        .paginate(page=page, per_page=6)
    return render_template('blog_posts/posts_category.html',
                           blog_posts=blog_posts,
                           current_category=cat.replace('_and_', ' & '))


@blogs.app_template_filter()
def find_reply(comment):
    reply = Comment.query.filter(Comment.reply_to == comment.id).first()
    return reply


@blogs.route('/comment/approve/<pk>')
def approve(pk):
    if not current_user.is_authenticated or current_user.status != UserStatus.admin:
        abort(403)

    comment = Comment.query.get_or_404(pk)
    comment.approved = True
    db.session.commit()

    next_ = request.args.get('next', None)
    if not next_:
        next_ = url_for('core.index')

    return redirect(next_)


@blogs.route('/comment/remove/<pk>')
def remove(pk):
    if not current_user.is_authenticated or current_user.status != UserStatus.admin:
        abort(403)

    comment = Comment.query.get_or_404(pk)
    comment.approved = False
    db.session.commit()

    next_ = request.args.get('next', None)
    if not next_:
        next_ = url_for('core.index')

    return redirect(next_)


@blogs.app_template_filter()
def length_comments(comments):
    if current_user.is_authenticated and current_user.status == UserStatus.admin:
        return len(comments)
    return len([comment for comment in comments if comment.approved])


@blogs.route('/comment/delete/<pk>', methods=['GET', 'POST'])
def delete_comment(pk):
    comment = Comment.query.get_or_404(pk)
    if not current_user.is_authenticated or comment.author != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    next_ = request.args.get('next', None)
    if not next_:
        next_ = url_for('core.index')

    return redirect(next_)


@blogs.route('/comment/edit/<pk>', methods=['POST'])
def edit_comment(pk):
    comment = Comment.query.get_or_404(pk)
    if not current_user.is_authenticated or comment.author != current_user:
        abort(403)

    form = EditCommentForm()
    if form.validate_on_submit():
        comment.text = form.text.data
        db.session.commit()

        next_ = request.args.get('next', None)
        if not next_:
            next_ = url_for('core.index')
        return redirect(next_)

    return render_template('core/message.html',
                           message='Couldn\'t update your comment. Somethings went wrong.')


@blogs.route('/comment/leave_reply/<pk>', methods=['POST'])
def leave_reply(pk):
    comment = Comment.query.get_or_404(pk)
    if not current_user.is_authenticated or current_user.status != UserStatus.admin:
        abort(403)

    form = LeaveReplyForm()
    if form.validate_on_submit():
        reply = Comment(user_id=current_user.id,
                        blog=comment.blog,
                        text=form.text.data,
                        reply_to=comment.id,
                        approved=True)
        db.session.add(reply)
        db.session.commit()

        next_ = request.args.get('next', None)
        if not next_:
            next_ = url_for('core.index')
        return redirect(next_)

    return render_template('core/message.html',
                           message='Couldn\'t leave reply. Somethings went wrong.')
